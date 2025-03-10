"""
Data models for the Medical Trial Data Validation System.
Author: Areesha Anum

Defines dataclasses used throughout the application.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class ValidationError:
    """Represents a single validation failure."""
    rule: str
    message: str
    row_number: Optional[int] = None


@dataclass
class ValidationResult:
    """Result of validating a single CSV file."""
    filename: str
    is_valid: bool
    errors: List[ValidationError] = field(default_factory=list)
    row_count: int = 0
    batch_ids: List[str] = field(default_factory=list)

    def add_error(self, rule: str, message: str, row_number: Optional[int] = None):
        self.errors.append(ValidationError(rule=rule, message=message, row_number=row_number))
        self.is_valid = False


@dataclass
class ProcessingResult:
    """Result of processing a file through the full pipeline."""
    filename: str
    status: str  # 'valid', 'invalid', 'skipped', 'error'
    validation_result: Optional[ValidationResult] = None
    archive_path: Optional[str] = None
    rejected_path: Optional[str] = None
    error_id: Optional[str] = None
    error_log_path: Optional[str] = None
    message: str = ""


@dataclass
class FileRecord:
    """Record of a processed file stored in the database."""
    id: Optional[int] = None
    filename: str = ""
    remote_path: str = ""
    local_path: str = ""
    file_hash: str = ""
    status: str = ""  # 'valid', 'invalid', 'skipped'
    archive_path: str = ""
    error_id: str = ""
    processed_at: str = ""
    validation_errors: str = ""
