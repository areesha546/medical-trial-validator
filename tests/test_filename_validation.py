"""
TDD Tests for filename validation.
Author: Areesha Anum

Tests the FilenameValidator component of the Chain of Responsibility.
These tests were written FIRST following TDD methodology.
"""

import pytest
from pathlib import Path
from app.validator import validate_file


class TestFilenameValidation:
    """Test suite for filename format validation."""

    def test_valid_filename_passes(self, valid_csv):
        """PASS: MED_DATA_YYYYMMDDHHMMSS.csv is accepted."""
        result = validate_file(valid_csv)
        filename_errors = [e for e in result.errors if 'filename' in e.rule]
        assert len(filename_errors) == 0, f"Valid filename should pass: {filename_errors}"

    def test_wrong_prefix_fails(self, make_csv):
        """FAIL: Filename without MED_DATA_ prefix must be rejected."""
        filepath = make_csv("BAD_DATA_20230603140104.csv", rows=[
            {"batch_id": "1", "timestamp": "14:01:04",
             "reading1": "1.0", "reading2": "2.0", "reading3": "3.0",
             "reading4": "4.0", "reading5": "5.0", "reading6": "6.0",
             "reading7": "7.0", "reading8": "8.0", "reading9": "9.0",
             "reading10": "1.0"}
        ])
        result = validate_file(filepath)
        assert not result.is_valid
        assert any(e.rule == 'filename_format' for e in result.errors)

    def test_wrong_extension_fails(self, make_csv):
        """FAIL: Non-.csv extension must be rejected."""
        filepath = make_csv("MED_DATA_20230603140104.txt", rows=[
            {"batch_id": "1", "timestamp": "14:01:04",
             "reading1": "1.0", "reading2": "2.0", "reading3": "3.0",
             "reading4": "4.0", "reading5": "5.0", "reading6": "6.0",
             "reading7": "7.0", "reading8": "8.0", "reading9": "9.0",
             "reading10": "1.0"}
        ])
        result = validate_file(filepath)
        assert not result.is_valid
        assert any(e.rule == 'filename_format' for e in result.errors)

    def test_short_timestamp_fails(self, make_csv):
        """FAIL: Timestamp with fewer than 14 digits must be rejected."""
        filepath = make_csv("MED_DATA_2023060314.csv", rows=[
            {"batch_id": "1", "timestamp": "14:01:04",
             "reading1": "1.0", "reading2": "2.0", "reading3": "3.0",
             "reading4": "4.0", "reading5": "5.0", "reading6": "6.0",
             "reading7": "7.0", "reading8": "8.0", "reading9": "9.0",
             "reading10": "1.0"}
        ])
        result = validate_file(filepath)
        assert not result.is_valid

    def test_invalid_date_in_timestamp_fails(self, make_csv):
        """FAIL: Invalid date (month 13) in timestamp must be rejected."""
        filepath = make_csv("MED_DATA_20231303140104.csv", rows=[
            {"batch_id": "1", "timestamp": "14:01:04",
             "reading1": "1.0", "reading2": "2.0", "reading3": "3.0",
             "reading4": "4.0", "reading5": "5.0", "reading6": "6.0",
             "reading7": "7.0", "reading8": "8.0", "reading9": "9.0",
             "reading10": "1.0"}
        ])
        result = validate_file(filepath)
        assert not result.is_valid
        assert any(e.rule == 'filename_timestamp' for e in result.errors)

    def test_no_underscore_separator_fails(self, make_csv):
        """FAIL: Missing underscore in prefix must be rejected."""
        filepath = make_csv("MEDDATA20230603140104.csv", rows=[])
        result = validate_file(filepath)
        assert not result.is_valid

    def test_letters_in_timestamp_fails(self, make_csv):
        """FAIL: Letters in timestamp portion must be rejected."""
        filepath = make_csv("MED_DATA_2023060314ABCD.csv", rows=[])
        result = validate_file(filepath)
        assert not result.is_valid

    def test_valid_filename_various_dates(self, make_csv):
        """PASS: Various valid dates should all pass filename validation."""
        valid_dates = [
            "20230101000000",
            "20231231235959",
            "20240229120000",  # Leap year
        ]
        for date_str in valid_dates:
            filepath = make_csv(f"MED_DATA_{date_str}.csv", rows=[
                {"batch_id": "1", "timestamp": "14:01:04",
                 "reading1": "1.0", "reading2": "2.0", "reading3": "3.0",
                 "reading4": "4.0", "reading5": "5.0", "reading6": "6.0",
                 "reading7": "7.0", "reading8": "8.0", "reading9": "9.0",
                 "reading10": "1.0"}
            ])
            result = validate_file(filepath)
            filename_errors = [e for e in result.errors if 'filename' in e.rule]
            assert len(filename_errors) == 0, f"Date {date_str} should be valid"
