"""
Archive service for organising valid and rejected files.
Author: Areesha Anum

Moves valid files to date-based archive structure.
Moves invalid files to rejected/quarantine area.
"""

import shutil
import logging
from datetime import datetime
from pathlib import Path

from app.config import ARCHIVE_DIR, REJECTED_DIR

logger = logging.getLogger(__name__)


def archive_valid_file(filepath: Path) -> str:
    """
    Archive a valid file into the date-based directory structure.
    Structure: archive/YYYY/MM/DD/HHMMSS_filename.csv

    Returns the archive path as a string.
    """
    now = datetime.now()
    timestamp_prefix = now.strftime("%H%M%S")

    archive_subdir = ARCHIVE_DIR / now.strftime("%Y") / now.strftime("%m") / now.strftime("%d")
    archive_subdir.mkdir(parents=True, exist_ok=True)

    archive_filename = f"{timestamp_prefix}_{filepath.name}"
    archive_path = archive_subdir / archive_filename

    shutil.copy2(str(filepath), str(archive_path))
    logger.info(f"Archived valid file: {filepath.name} -> {archive_path}")

    return str(archive_path)


def quarantine_invalid_file(filepath: Path) -> str:
    """
    Move an invalid file to the rejected/quarantine directory.
    Structure: rejected/YYYY/MM/DD/filename.csv

    Returns the rejected path as a string.
    """
    now = datetime.now()

    rejected_subdir = REJECTED_DIR / now.strftime("%Y") / now.strftime("%m") / now.strftime("%d")
    rejected_subdir.mkdir(parents=True, exist_ok=True)

    rejected_path = rejected_subdir / filepath.name
    # Handle duplicate filenames in rejected
    if rejected_path.exists():
        stem = filepath.stem
        suffix = filepath.suffix
        counter = 1
        while rejected_path.exists():
            rejected_path = rejected_subdir / f"{stem}_{counter}{suffix}"
            counter += 1

    shutil.copy2(str(filepath), str(rejected_path))
    logger.info(f"Quarantined invalid file: {filepath.name} -> {rejected_path}")

    return str(rejected_path)
