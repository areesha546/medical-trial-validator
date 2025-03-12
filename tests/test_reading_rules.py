"""
TDD Tests for reading validation rules.
Author: Areesha Anum

Tests numeric validation, max value, and decimal place rules.
"""

import pytest
from app.validator import validate_file


class TestReadingValidation:
    """Test suite for reading value validation."""

    def test_valid_readings_pass(self, valid_csv):
        """PASS: Valid numeric readings within range pass."""
        result = validate_file(valid_csv)
        reading_errors = [e for e in result.errors if 'reading' in e.rule]
        assert len(reading_errors) == 0

    def test_reading_over_max_fails(self, make_csv):
        """FAIL: Reading value exceeding 9.9 must be rejected."""
        content = "batch_id,timestamp,reading1,reading2,reading3,reading4,reading5,reading6,reading7,reading8,reading9,reading10\n"
        content += "1,14:01:04,10.5,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,1.0\n"
        filepath = make_csv("MED_DATA_20230603140104.csv", raw_content=content)
        result = validate_file(filepath)
        assert not result.is_valid
        assert any(e.rule == 'reading_exceeds_max' for e in result.errors)

    def test_reading_exactly_9_9_passes(self, make_csv):
        """PASS: Reading value of exactly 9.9 is acceptable."""
        content = "batch_id,timestamp,reading1,reading2,reading3,reading4,reading5,reading6,reading7,reading8,reading9,reading10\n"
        content += "1,14:01:04,9.9,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,1.0\n"
        filepath = make_csv("MED_DATA_20230603140104.csv", raw_content=content)
        result = validate_file(filepath)
        max_errors = [e for e in result.errors if e.rule == 'reading_exceeds_max']
        assert len(max_errors) == 0

    def test_text_instead_of_number_fails(self, make_csv):
        """FAIL: Non-numeric reading value must be rejected."""
        content = "batch_id,timestamp,reading1,reading2,reading3,reading4,reading5,reading6,reading7,reading8,reading9,reading10\n"
        content += "1,14:01:04,abc,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,1.0\n"
        filepath = make_csv("MED_DATA_20230603140104.csv", raw_content=content)
        result = validate_file(filepath)
        assert not result.is_valid
        assert any(e.rule == 'invalid_reading_type' for e in result.errors)

    def test_nil_value_fails(self, make_csv):
        """FAIL: 'nil' as a reading value must be rejected."""
        content = "batch_id,timestamp,reading1,reading2,reading3,reading4,reading5,reading6,reading7,reading8,reading9,reading10\n"
        content += "1,14:01:04,nil,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,1.0\n"
        filepath = make_csv("MED_DATA_20230603140104.csv", raw_content=content)
        result = validate_file(filepath)
        assert not result.is_valid
        assert any(e.rule == 'invalid_reading_type' for e in result.errors)

    def test_too_many_decimal_places_fails(self, make_csv):
        """FAIL: Reading with more than 3 decimal places must be rejected."""
        content = "batch_id,timestamp,reading1,reading2,reading3,reading4,reading5,reading6,reading7,reading8,reading9,reading10\n"
        content += "1,14:01:04,1.12345,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,1.0\n"
        filepath = make_csv("MED_DATA_20230603140104.csv", raw_content=content)
        result = validate_file(filepath)
        assert not result.is_valid
        assert any(e.rule == 'reading_decimal_places' for e in result.errors)

    def test_three_decimal_places_passes(self, make_csv):
        """PASS: Reading with exactly 3 decimal places is acceptable."""
        content = "batch_id,timestamp,reading1,reading2,reading3,reading4,reading5,reading6,reading7,reading8,reading9,reading10\n"
        content += "1,14:01:04,1.123,2.456,3.789,4.012,5.345,6.678,7.901,8.234,9.567,1.890\n"
        filepath = make_csv("MED_DATA_20230603140104.csv", raw_content=content)
        result = validate_file(filepath)
        decimal_errors = [e for e in result.errors if e.rule == 'reading_decimal_places']
        assert len(decimal_errors) == 0

    def test_multiple_invalid_readings_in_row(self, make_csv):
        """FAIL: Multiple invalid readings in one row are all detected."""
        content = "batch_id,timestamp,reading1,reading2,reading3,reading4,reading5,reading6,reading7,reading8,reading9,reading10\n"
        content += "1,14:01:04,15.0,nil,abc,N/A,5.0,6.0,7.0,8.0,9.0,1.0\n"
        filepath = make_csv("MED_DATA_20230603140104.csv", raw_content=content)
        result = validate_file(filepath)
        assert not result.is_valid
        reading_errors = [e for e in result.errors if 'reading' in e.rule]
        assert len(reading_errors) >= 4  # 15.0 exceeds max, nil/abc/N/A are invalid type

    def test_integer_reading_passes(self, make_csv):
        """PASS: Integer values (no decimal) should pass."""
        content = "batch_id,timestamp,reading1,reading2,reading3,reading4,reading5,reading6,reading7,reading8,reading9,reading10\n"
        content += "1,14:01:04,1,2,3,4,5,6,7,8,9,1\n"
        filepath = make_csv("MED_DATA_20230603140104.csv", raw_content=content)
        result = validate_file(filepath)
        reading_errors = [e for e in result.errors if 'reading' in e.rule]
        assert len(reading_errors) == 0
