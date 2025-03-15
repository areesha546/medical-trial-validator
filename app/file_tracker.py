"""
File tracking module using SQLite.
Author: Areesha Anum

Tracks processed files to prevent duplicate processing.
Stores filename, hash, status, and processing metadata.
"""

import hashlib
import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.config import DATABASE_PATH
from app.models import FileRecord

logger = logging.getLogger(__name__)


def _get_connection() -> sqlite3.Connection:
    """Get a SQLite connection, creating the database if needed."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DATABASE_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialise the database schema."""
    conn = _get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS processed_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                remote_path TEXT DEFAULT '',
                local_path TEXT DEFAULT '',
                file_hash TEXT DEFAULT '',
                status TEXT NOT NULL,
                archive_path TEXT DEFAULT '',
                error_id TEXT DEFAULT '',
                processed_at TEXT NOT NULL,
                validation_errors TEXT DEFAULT ''
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_filename ON processed_files(filename)
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_file_hash ON processed_files(file_hash)
        """)
        conn.commit()
        logger.info("Database initialised successfully")
    finally:
        conn.close()


def compute_file_hash(filepath: Path) -> str:
    """Compute SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def is_already_processed(filename: str, file_hash: Optional[str] = None) -> bool:
    """
    Check if a file has already been processed.
    Checks by filename and optionally by file hash.
    """
    conn = _get_connection()
    try:
        if file_hash:
            row = conn.execute(
                "SELECT id FROM processed_files WHERE filename = ? OR file_hash = ?",
                (filename, file_hash)
            ).fetchone()
        else:
            row = conn.execute(
                "SELECT id FROM processed_files WHERE filename = ?",
                (filename,)
            ).fetchone()
        return row is not None
    finally:
        conn.close()


def record_processed_file(record: FileRecord):
    """Record a processed file in the database."""
    conn = _get_connection()
    try:
        conn.execute("""
            INSERT INTO processed_files
            (filename, remote_path, local_path, file_hash, status, archive_path,
             error_id, processed_at, validation_errors)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record.filename, record.remote_path, record.local_path,
            record.file_hash, record.status, record.archive_path,
            record.error_id, record.processed_at or datetime.now().isoformat(),
            record.validation_errors
        ))
        conn.commit()
        logger.info(f"Recorded file: {record.filename} (status: {record.status})")
    finally:
        conn.close()


def get_all_records() -> list[FileRecord]:
    """Retrieve all processed file records."""
    conn = _get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM processed_files ORDER BY processed_at DESC"
        ).fetchall()
        return [
            FileRecord(
                id=row['id'],
                filename=row['filename'],
                remote_path=row['remote_path'],
                local_path=row['local_path'],
                file_hash=row['file_hash'],
                status=row['status'],
                archive_path=row['archive_path'],
                error_id=row['error_id'],
                processed_at=row['processed_at'],
                validation_errors=row['validation_errors']
            )
            for row in rows
        ]
    finally:
        conn.close()


def get_processing_stats() -> dict:
    """Get summary statistics of processed files."""
    conn = _get_connection()
    try:
        total = conn.execute("SELECT COUNT(*) FROM processed_files").fetchone()[0]
        valid = conn.execute("SELECT COUNT(*) FROM processed_files WHERE status='valid'").fetchone()[0]
        invalid = conn.execute("SELECT COUNT(*) FROM processed_files WHERE status='invalid'").fetchone()[0]
        skipped = conn.execute("SELECT COUNT(*) FROM processed_files WHERE status='skipped'").fetchone()[0]
        return {
            "total": total,
            "valid": valid,
            "invalid": invalid,
            "skipped": skipped
        }
    finally:
        conn.close()


def clear_all_records():
    """Clear all records from the database. Used for testing."""
    conn = _get_connection()
    try:
        conn.execute("DELETE FROM processed_files")
        conn.commit()
    finally:
        conn.close()
