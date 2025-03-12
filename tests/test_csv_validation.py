"""
TDD Tests for CSV structure validation.
Author: Areesha Anum

Tests header validation and CSV parsing.
"""

import pytest
from app.validator import validate_file


class TestCSVValidation:
    """Test suite for CSV structure and header validation."""

    def test_valid_csv_passes(self, valid_csv):
        """PASS: Properly structured CSV passes validation."""
        result = validate_file(valid_csv)
        header_errors = [e for e in result.errors if 'header' in e.rule or 'csv' in e.rule]
        assert len(header_errors) == 0

    def test_empty_file_fails(self, make_csv):
        """FAIL: Empty CSV file must be rejected."""
        filepath = make_csv("MED_DATA_20230603140104.csv", raw_content="")
        result = validate_file(filepath)
        assert not result.is_valid
        assert any(e.rule == 'csv_empty' for e in result.errors)

    def test_missing_header_fails(self, make_csv):
        """FAIL: CSV missing a required header must be rejected."""
        # Missing reading10
        bad_headers = [
            "batch_id", "timestamp",
            "reading1", "reading2", "reading3", "reading4", "reading5",
            "reading6", "reading7", "reading8", "reading9"
        ]
        filepath = make_csv("MED_DATA_20230603140104.csv", headers=bad_headers, rows=[
            {"batch_id": "1", "timestamp": "14:01:04",
             "reading1": "1.0", "reading2": "2.0", "reading3": "3.0",
             "reading4": "4.0", "reading5": "5.0", "reading6": "6.0",
             "reading7": "7.0", "reading8": "8.0", "reading9": "9.0"}
        ])
        result = validate_file(filepath)
        assert not result.is_valid
        assert any(e.rule == 'missing_headers' for e in result.errors)

    def test_misspelled_header_fails(self, make_csv):
        """FAIL: Header 'batch' instead of 'batch_id' must be detected."""
        content = "batch,timestamp,reading1,reading2,reading3,reading4,reading5,reading6,reading7,reading8,reading9,reading10\n"
        content += "1,14:01:04,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,1.0\n"
        filepath = make_csv("MED_DATA_20230603140104.csv", raw_content=content)
        result = validate_file(filepath)
        assert not result.is_valid
        assert any(e.rule == 'missing_headers' for e in result.errors)

    def test_all_required_headers_present(self, valid_csv):
        """PASS: File with all 12 required headers passes."""
        result = validate_file(valid_csv)
        header_errors = [e for e in result.errors if 'header' in e.rule]
        assert len(header_errors) == 0

    def test_missing_value_in_row_fails(self, make_csv):
        """FAIL: Row with missing column value must be rejected."""
        content = "batch_id,timestamp,reading1,reading2,reading3,reading4,reading5,reading6,reading7,reading8,reading9,reading10\n"
        content += "1,14:01:04,1.0,2.0,3.0,,5.0,6.0,7.0,8.0,9.0,1.0\n"
        filepath = make_csv("MED_DATA_20230603140104.csv", raw_content=content)
        result = validate_file(filepath)
        assert not result.is_valid
        assert any(e.rule == 'missing_value' for e in result.errors)

    def test_header_only_csv_passes(self, make_csv):
        """PASS: CSV with only headers and no data rows is structurally valid."""
        filepath = make_csv("MED_DATA_20230603140104.csv", rows=[])
        result = validate_file(filepath)
        header_errors = [e for e in result.errors if 'header' in e.rule]
        assert len(header_errors) == 0
