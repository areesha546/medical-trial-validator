"""
Main processing pipeline for the Medical Trial Data Validation System.
Author: Areesha Anum

Orchestrates the full workflow: FTP download -> validation -> archive/reject.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import List

from app.ftp_service import FTPService
from app.validator import validate_file
from app.file_tracker import (
    init_database, is_already_processed, record_processed_file,
    compute_file_hash, get_processing_stats
)
from app.archive_service import archive_valid_file, quarantine_invalid_file
from app.error_logger import create_error_log
from app.models import ProcessingResult, FileRecord

logger = logging.getLogger(__name__)


def setup_logging():
    """Configure application logging."""
    from pathlib import Path
    Path('logs').mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('logs/application.log', mode='a')
        ]
    )


def process_single_file(filepath: Path, remote_path: str = "") -> ProcessingResult:
    """
    Process a single downloaded CSV file through the validation pipeline.

    Args:
        filepath: Path to the local CSV file
        remote_path: Original remote path on FTP server

    Returns:
        ProcessingResult with the outcome
    """
    filename = filepath.name
    result = ProcessingResult(filename=filename, status="pending")

    # Step 1: Check if already processed
    file_hash = compute_file_hash(filepath)
    if is_already_processed(filename, file_hash):
        result.status = "skipped"
        result.message = "File has already been processed"
        logger.info(f"Skipping already processed file: {filename}")
        return result

    # Step 2: Validate through the chain
    validation_result = validate_file(filepath)
    result.validation_result = validation_result

    # Step 3: Archive or reject
    if validation_result.is_valid:
        result.status = "valid"
        result.archive_path = archive_valid_file(filepath)
        result.message = f"Valid file archived successfully ({validation_result.row_count} rows)"
        logger.info(f"Valid file archived: {filename}")
    else:
        result.status = "invalid"
        result.rejected_path = quarantine_invalid_file(filepath)
        error_id, error_log_path = create_error_log(validation_result, str(filepath))
        result.error_id = error_id
        result.error_log_path = error_log_path
        error_summary = "; ".join([e.message for e in validation_result.errors[:5]])
        result.message = f"Invalid file rejected: {error_summary}"
        logger.warning(f"Invalid file rejected: {filename} ({len(validation_result.errors)} errors)")

    # Step 4: Record in database
    record = FileRecord(
        filename=filename,
        remote_path=remote_path,
        local_path=str(filepath),
        file_hash=file_hash,
        status=result.status,
        archive_path=result.archive_path or "",
        error_id=result.error_id or "",
        processed_at=datetime.now().isoformat(),
        validation_errors="; ".join([e.message for e in (validation_result.errors or [])])
    )
    record_processed_file(record)

    return result


def process_ftp_files(ftp_service: FTPService = None) -> List[ProcessingResult]:
    """
    Full pipeline: connect to FTP, download new files, validate, and archive.

    Returns:
        List of ProcessingResult for each file processed
    """
    results = []
    own_ftp = ftp_service is None

    if own_ftp:
        ftp_service = FTPService()

    try:
        # Connect
        if not ftp_service.is_connected():
            if not ftp_service.connect():
                return [ProcessingResult(
                    filename="",
                    status="error",
                    message="Failed to connect to FTP server"
                )]

        # List files
        csv_files = ftp_service.list_csv_files()
        if not csv_files:
            logger.info("No CSV files found on FTP server")
            return results

        # Process each file
        for remote_file in csv_files:
            # Quick check before downloading
            if is_already_processed(remote_file):
                results.append(ProcessingResult(
                    filename=remote_file,
                    status="skipped",
                    message="Already processed"
                ))
                continue

            # Download
            local_path = ftp_service.download_file(remote_file)
            if local_path is None:
                results.append(ProcessingResult(
                    filename=remote_file,
                    status="error",
                    message="Failed to download file"
                ))
                continue

            # Process
            result = process_single_file(local_path, remote_path=remote_file)
            results.append(result)

    except Exception as e:
        logger.error(f"Pipeline error: {str(e)}")
        results.append(ProcessingResult(
            filename="",
            status="error",
            message=f"Pipeline error: {str(e)}"
        ))
    finally:
        if own_ftp:
            ftp_service.disconnect()

    return results


# Initialise database on import
init_database()
