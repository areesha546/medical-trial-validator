"""
Validation module using Chain of Responsibility pattern.
Author: Areesha Anum

Each validator in the chain checks one specific rule. If it fails,
the error is recorded and the chain continues to find all errors.
"""

import csv
import io
import re
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.config import (
    REQUIRED_HEADERS, FILENAME_PREFIX, FILENAME_EXTENSION,
    MAX_READING_VALUE, MAX_DECIMAL_PLACES, READING_COUNT
)
from app.models import ValidationResult


class BaseValidator(ABC):
    """
    Base class for the Chain of Responsibility pattern.
    Each validator has a reference to the next validator in the chain.
    """

    def __init__(self):
        self._next_validator: Optional['BaseValidator'] = None

    def set_next(self, validator: 'BaseValidator') -> 'BaseValidator':
        """Set the next validator in the chain and return it for chaining."""
        self._next_validator = validator
        return validator

    def validate(self, filepath: Path, result: ValidationResult) -> ValidationResult:
        """Run this validator then pass to the next in the chain."""
        self._do_validate(filepath, result)
        if self._next_validator:
            return self._next_validator.validate(filepath, result)
        return result

    @abstractmethod
    def _do_validate(self, filepath: Path, result: ValidationResult):
        """Perform the actual validation check."""
        pass


class FilenameValidator(BaseValidator):
    """Validates filename matches MED_DATA_YYYYMMDDHHMMSS.csv pattern."""

    FILENAME_PATTERN = re.compile(
        r'^MED_DATA_(\d{14})\.csv$'
    )

    def _do_validate(self, filepath: Path, result: ValidationResult):
        filename = filepath.name
        match = self.FILENAME_PATTERN.match(filename)

        if not match:
            result.add_error(
                rule="filename_format",
                message=f"Filename '{filename}' does not match required pattern MED_DATA_YYYYMMDDHHMMSS.csv"
            )
            return

        # Validate the timestamp portion is a real date/time
        timestamp_str = match.group(1)
        try:
            datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
        except ValueError:
            result.add_error(
                rule="filename_timestamp",
                message=f"Timestamp '{timestamp_str}' in filename is not a valid datetime"
            )


class HeaderValidator(BaseValidator):
    """Validates CSV has required headers."""

    def _do_validate(self, filepath: Path, result: ValidationResult):
        try:
            with open(filepath, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                try:
                    headers = next(reader)
                except StopIteration:
                    result.add_error(
                        rule="csv_empty",
                        message="CSV file is empty, no header row found"
                    )
                    return

            # Strip whitespace from headers
            headers = [h.strip() for h in headers]

            # Check for missing headers
            missing = [h for h in REQUIRED_HEADERS if h not in headers]
            if missing:
                result.add_error(
                    rule="missing_headers",
                    message=f"Missing required headers: {', '.join(missing)}"
                )

            # Check for extra/misspelled headers that look like required ones
            expected_set = set(REQUIRED_HEADERS)
            actual_set = set(headers)
            extra = actual_set - expected_set
            if extra:
                for h in extra:
                    # Check if it might be a misspelling
                    for req in REQUIRED_HEADERS:
                        if h.lower().replace('_', '') == req.lower().replace('_', '') and h != req:
                            result.add_error(
                                rule="misspelled_header",
                                message=f"Header '{h}' appears to be a misspelling of '{req}'"
                            )
        except csv.Error as e:
            result.add_error(
                rule="csv_parse_error",
                message=f"Failed to parse CSV file: {str(e)}"
            )
        except UnicodeDecodeError as e:
            result.add_error(
                rule="csv_encoding_error",
                message=f"File encoding error: {str(e)}"
            )


class RowCompletenessValidator(BaseValidator):
    """Validates every row has all required column values."""

    def _do_validate(self, filepath: Path, result: ValidationResult):
        try:
            with open(filepath, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames:
                    return  # Already caught by HeaderValidator

                headers = [h.strip() for h in reader.fieldnames]
                # Only proceed if we have the required headers
                if not all(h in headers for h in REQUIRED_HEADERS):
                    return  # Header validation already failed

                for row_num, row in enumerate(reader, start=2):
                    # Strip keys
                    row = {k.strip(): v for k, v in row.items()}
                    for header in REQUIRED_HEADERS:
                        value = row.get(header, None)
                        if value is None or str(value).strip() == '':
                            result.add_error(
                                rule="missing_value",
                                message=f"Missing value for '{header}'",
                                row_number=row_num
                            )
                    result.row_count = row_num - 1
        except csv.Error as e:
            result.add_error(
                rule="csv_row_parse_error",
                message=f"Error parsing CSV rows: {str(e)}"
            )


class BatchValidator(BaseValidator):
    """Validates batch_id uniqueness within the file."""

    def _do_validate(self, filepath: Path, result: ValidationResult):
        try:
            with open(filepath, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames:
                    return

                headers = [h.strip() for h in reader.fieldnames]
                if 'batch_id' not in headers:
                    return

                seen_ids = {}
                for row_num, row in enumerate(reader, start=2):
                    row = {k.strip(): v for k, v in row.items()}
                    batch_id = row.get('batch_id', '').strip()

                    if batch_id == '':
                        continue  # Already caught by RowCompletenessValidator

                    if batch_id in seen_ids:
                        result.add_error(
                            rule="duplicate_batch_id",
                            message=f"Duplicate batch_id '{batch_id}' (first seen at row {seen_ids[batch_id]})",
                            row_number=row_num
                        )
                    else:
                        seen_ids[batch_id] = row_num
                        result.batch_ids.append(batch_id)

        except csv.Error:
            pass  # Already handled


class ReadingValidator(BaseValidator):
    """Validates reading1-reading10 values."""

    def _do_validate(self, filepath: Path, result: ValidationResult):
        reading_headers = [f"reading{i}" for i in range(1, READING_COUNT + 1)]

        try:
            with open(filepath, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames:
                    return

                headers = [h.strip() for h in reader.fieldnames]
                available_readings = [h for h in reading_headers if h in headers]

                if len(available_readings) != READING_COUNT:
                    return  # Header validation will catch this

                for row_num, row in enumerate(reader, start=2):
                    row = {k.strip(): v for k, v in row.items()}

                    for reading_col in reading_headers:
                        value = row.get(reading_col, '').strip()
                        if value == '':
                            continue  # Already caught by completeness validator

                        # Check if numeric
                        try:
                            num_value = float(value)
                        except (ValueError, TypeError):
                            result.add_error(
                                rule="invalid_reading_type",
                                message=f"'{reading_col}' value '{value}' is not a valid number",
                                row_number=row_num
                            )
                            continue

                        # Check max value
                        if num_value > MAX_READING_VALUE:
                            result.add_error(
                                rule="reading_exceeds_max",
                                message=f"'{reading_col}' value {num_value} exceeds maximum {MAX_READING_VALUE}",
                                row_number=row_num
                            )

                        # Check decimal places
                        if '.' in value:
                            decimal_part = value.split('.')[1]
                            if len(decimal_part) > MAX_DECIMAL_PLACES:
                                result.add_error(
                                    rule="reading_decimal_places",
                                    message=f"'{reading_col}' value '{value}' has more than {MAX_DECIMAL_PLACES} decimal places",
                                    row_number=row_num
                                )

        except csv.Error:
            pass  # Already handled


def build_validation_chain() -> BaseValidator:
    """
    Constructs the Chain of Responsibility for file validation.
    Each validator checks one aspect and passes to the next.
    """
    filename_validator = FilenameValidator()
    header_validator = HeaderValidator()
    row_validator = RowCompletenessValidator()
    batch_validator = BatchValidator()
    reading_validator = ReadingValidator()

    # Build chain: filename -> headers -> rows -> batches -> readings
    filename_validator.set_next(header_validator)
    header_validator.set_next(row_validator)
    row_validator.set_next(batch_validator)
    batch_validator.set_next(reading_validator)

    return filename_validator


def validate_file(filepath: Path) -> ValidationResult:
    """
    Validate a CSV file through the full chain of responsibility.
    Returns a ValidationResult with all errors found.
    """
    result = ValidationResult(
        filename=filepath.name,
        is_valid=True
    )

    chain = build_validation_chain()
    chain.validate(filepath, result)

    return result
