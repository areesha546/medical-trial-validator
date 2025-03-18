"""
Error logging module for rejected files.
Author: Areesha Anum

Creates structured JSON error logs for each rejected file.
"""

import json
import logging
from datetime import datetime
from pathlib import Path

from app.config import ERROR_LOGS_DIR
from app.guid_service import generate_error_id
from app.models import ValidationResult

logger = logging.getLogger(__name__)


def create_error_log(validation_result: ValidationResult, local_path: str) -> tuple[str, str]:
    """
    Create a structured error log for a rejected file.

    Args:
        validation_result: The validation result with errors
        local_path: Path where the downloaded file is stored

    Returns:
        tuple: (error_id, error_log_path)
    """
    error_id, used_api = generate_error_id()
    now = datetime.now()

    # Create date-based directory
    log_dir = ERROR_LOGS_DIR / now.strftime("%Y") / now.strftime("%m") / now.strftime("%d")
    log_dir.mkdir(parents=True, exist_ok=True)

    error_entry = {
        "error_id": error_id,
        "generated_via": "uuidtools_api" if used_api else "local_uuid_fallback",
        "datetime": now.isoformat(),
        "original_filename": validation_result.filename,
        "local_path": str(local_path),
        "failure_category": _categorize_errors(validation_result),
        "errors": [
            {
                "rule": err.rule,
                "message": err.message,
                "row_number": err.row_number
            }
            for err in validation_result.errors
        ],
        "total_errors": len(validation_result.errors),
        "quarantined": True
    }

    log_path = log_dir / f"error_{error_id}.json"
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(error_entry, f, indent=2, ensure_ascii=False)

    logger.info(f"Error log created: {log_path}")
    return error_id, str(log_path)


def _categorize_errors(result: ValidationResult) -> str:
    """Categorize the type of validation failure."""
    rules = {err.rule for err in result.errors}

    if 'filename_format' in rules or 'filename_timestamp' in rules:
        return "filename_validation_failure"
    elif 'csv_empty' in rules or 'csv_parse_error' in rules or 'csv_encoding_error' in rules:
        return "csv_structure_failure"
    elif 'missing_headers' in rules or 'misspelled_header' in rules:
        return "header_validation_failure"
    elif 'duplicate_batch_id' in rules:
        return "batch_validation_failure"
    elif any('reading' in r for r in rules):
        return "reading_validation_failure"
    elif 'missing_value' in rules:
        return "completeness_failure"
    else:
        return "general_validation_failure"


def get_recent_error_logs(limit: int = 50) -> list[dict]:
    """Retrieve recent error logs for display in the UI."""
    logs = []
    if not ERROR_LOGS_DIR.exists():
        return logs

    log_files = sorted(ERROR_LOGS_DIR.rglob("error_*.json"), reverse=True)

    for log_file in log_files[:limit]:
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                logs.append(json.load(f))
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to read error log {log_file}: {e}")

    return logs
