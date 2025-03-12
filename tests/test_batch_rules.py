"""
TDD Tests for batch validation rules.
Author: Areesha Anum

Tests batch_id uniqueness and related rules.
"""

import pytest
from app.validator import validate_file


class TestBatchValidation:
    """Test suite for batch_id validation."""

    def test_unique_batch_ids_pass(self, valid_csv):
        """PASS: File with unique batch IDs passes."""
        result = validate_file(valid_csv)
        batch_errors = [e for e in result.errors if 'batch' in e.rule]
        assert len(batch_errors) == 0

    def test_duplicate_batch_id_fails(self, make_csv):
        """FAIL: Duplicate batch_id within same file must be rejected."""
        content = "batch_id,timestamp,reading1,reading2,reading3,reading4,reading5,reading6,reading7,reading8,reading9,reading10\n"
        content += "55,14:01:04,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,1.0\n"
        content += "55,14:01:05,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,1.5\n"
        filepath = make_csv("MED_DATA_20230603140104.csv", raw_content=content)
        result = validate_file(filepath)
        assert not result.is_valid
        assert any(e.rule == 'duplicate_batch_id' for e in result.errors)

    def test_multiple_duplicates_detected(self, make_csv):
        """FAIL: Multiple duplicate batch IDs are all flagged."""
        content = "batch_id,timestamp,reading1,reading2,reading3,reading4,reading5,reading6,reading7,reading8,reading9,reading10\n"
        content += "55,14:01:04,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,1.0\n"
        content += "55,14:01:05,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,1.5\n"
        content += "55,14:01:06,1.1,2.1,3.1,4.1,5.1,6.1,7.1,8.1,9.1,1.1\n"
        filepath = make_csv("MED_DATA_20230603140104.csv", raw_content=content)
        result = validate_file(filepath)
        dup_errors = [e for e in result.errors if e.rule == 'duplicate_batch_id']
        assert len(dup_errors) == 2  # Rows 3 and 4 are duplicates

    def test_different_batch_ids_pass(self, make_csv):
        """PASS: File with all unique batch IDs passes batch validation."""
        content = "batch_id,timestamp,reading1,reading2,reading3,reading4,reading5,reading6,reading7,reading8,reading9,reading10\n"
        for i in range(1, 6):
            content += f"{i},14:01:0{i},1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,1.0\n"
        filepath = make_csv("MED_DATA_20230603140104.csv", raw_content=content)
        result = validate_file(filepath)
        batch_errors = [e for e in result.errors if 'batch' in e.rule]
        assert len(batch_errors) == 0

    def test_same_timestamp_different_batch_id_passes(self, make_csv):
        """PASS: Same timestamps with different batch IDs are acceptable."""
        content = "batch_id,timestamp,reading1,reading2,reading3,reading4,reading5,reading6,reading7,reading8,reading9,reading10\n"
        content += "1,14:01:04,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,1.0\n"
        content += "2,14:01:04,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,1.5\n"
        filepath = make_csv("MED_DATA_20230603140104.csv", raw_content=content)
        result = validate_file(filepath)
        batch_errors = [e for e in result.errors if 'batch' in e.rule]
        assert len(batch_errors) == 0
