"""
TDD Tests for file tracker (duplicate detection).
Author: Areesha Anum

Tests the SQLite-based file tracking system.
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch
from datetime import datetime

from app.file_tracker import (
    init_database, is_already_processed, record_processed_file,
    compute_file_hash, get_all_records, get_processing_stats,
    clear_all_records
)
from app.models import FileRecord


@pytest.fixture(autouse=True)
def use_temp_database(tmp_path):
    """Use a temporary database for each test."""
    temp_db = tmp_path / "test_tracker.db"
    with patch('app.file_tracker.DATABASE_PATH', temp_db):
        init_database()
        yield


class TestFileTracker:
    """Test suite for file tracking and duplicate detection."""

    def test_new_file_not_processed(self):
        """New file should not be marked as already processed."""
        assert is_already_processed("brand_new_file.csv") is False

    def test_recorded_file_is_processed(self):
        """After recording, file should be detected as processed."""
        record = FileRecord(
            filename="MED_DATA_20230603140104.csv",
            status="valid",
            processed_at=datetime.now().isoformat()
        )
        record_processed_file(record)
        assert is_already_processed("MED_DATA_20230603140104.csv") is True

    def test_file_hash_tracking(self, tmp_path):
        """Files should be trackable by hash."""
        test_file = tmp_path / "test.csv"
        test_file.write_text("test content")
        file_hash = compute_file_hash(test_file)

        record = FileRecord(
            filename="test.csv",
            file_hash=file_hash,
            status="valid",
            processed_at=datetime.now().isoformat()
        )
        record_processed_file(record)
        assert is_already_processed("different_name.csv", file_hash) is True

    def test_get_all_records(self):
        """Should retrieve all processed records."""
        for i in range(3):
            record = FileRecord(
                filename=f"file_{i}.csv",
                status="valid",
                processed_at=datetime.now().isoformat()
            )
            record_processed_file(record)

        records = get_all_records()
        assert len(records) == 3

    def test_processing_stats(self):
        """Stats should correctly count valid, invalid, skipped."""
        for status in ["valid", "valid", "invalid", "skipped"]:
            record = FileRecord(
                filename=f"file_{status}_{id(status)}.csv",
                status=status,
                processed_at=datetime.now().isoformat()
            )
            record_processed_file(record)

        stats = get_processing_stats()
        assert stats['total'] == 4
        assert stats['valid'] == 2
        assert stats['invalid'] == 1
        assert stats['skipped'] == 1

    def test_compute_file_hash_consistent(self, tmp_path):
        """Same file content should produce same hash."""
        file1 = tmp_path / "file1.csv"
        file2 = tmp_path / "file2.csv"
        content = "batch_id,timestamp\n1,14:01:04\n"
        file1.write_text(content)
        file2.write_text(content)

        assert compute_file_hash(file1) == compute_file_hash(file2)

    def test_different_content_different_hash(self, tmp_path):
        """Different file content should produce different hashes."""
        file1 = tmp_path / "file1.csv"
        file2 = tmp_path / "file2.csv"
        file1.write_text("content A")
        file2.write_text("content B")

        assert compute_file_hash(file1) != compute_file_hash(file2)

    def test_clear_all_records(self):
        """Clear should remove all records."""
        record = FileRecord(
            filename="test.csv",
            status="valid",
            processed_at=datetime.now().isoformat()
        )
        record_processed_file(record)
        assert get_processing_stats()['total'] == 1
        clear_all_records()
        assert get_processing_stats()['total'] == 0
