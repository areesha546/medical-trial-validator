"""
TDD Tests for error logging.
Author: Areesha Anum

Tests error log creation and GUID generation.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from app.models import ValidationResult, ValidationError
from app.error_logger import create_error_log, _categorize_errors
from app.guid_service import generate_error_id


class TestErrorLogging:
    """Test suite for error log creation."""

    def test_error_log_creates_json_file(self, tmp_dir):
        """Error log must create a valid JSON file."""
        result = ValidationResult(
            filename="test.csv",
            is_valid=False,
            errors=[ValidationError(rule="test_rule", message="Test error")]
        )

        with patch('app.error_logger.ERROR_LOGS_DIR', tmp_dir):
            error_id, log_path = create_error_log(result, "/tmp/test.csv")

        assert Path(log_path).exists()
        with open(log_path, 'r') as f:
            data = json.load(f)
        assert data['error_id'] == error_id
        assert data['original_filename'] == "test.csv"
        assert len(data['errors']) == 1

    def test_error_log_contains_required_fields(self, tmp_dir):
        """Error log must contain all required fields."""
        result = ValidationResult(
            filename="bad.csv",
            is_valid=False,
            errors=[ValidationError(rule="missing_headers", message="Missing reading10")]
        )

        with patch('app.error_logger.ERROR_LOGS_DIR', tmp_dir):
            error_id, log_path = create_error_log(result, "/downloads/bad.csv")

        with open(log_path, 'r') as f:
            data = json.load(f)

        required_fields = [
            'error_id', 'datetime', 'original_filename',
            'local_path', 'failure_category', 'errors',
            'total_errors', 'quarantined', 'generated_via'
        ]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

    def test_error_log_quarantined_flag(self, tmp_dir):
        """Error log must mark the file as quarantined."""
        result = ValidationResult(
            filename="test.csv",
            is_valid=False,
            errors=[ValidationError(rule="test_rule", message="Error")]
        )

        with patch('app.error_logger.ERROR_LOGS_DIR', tmp_dir):
            _, log_path = create_error_log(result, "/tmp/test.csv")

        with open(log_path, 'r') as f:
            data = json.load(f)
        assert data['quarantined'] is True

    def test_categorize_filename_errors(self):
        """Error category for filename issues should be correct."""
        result = ValidationResult(
            filename="bad.csv",
            is_valid=False,
            errors=[ValidationError(rule="filename_format", message="Bad name")]
        )
        assert _categorize_errors(result) == "filename_validation_failure"

    def test_categorize_header_errors(self):
        """Error category for header issues should be correct."""
        result = ValidationResult(
            filename="test.csv",
            is_valid=False,
            errors=[ValidationError(rule="missing_headers", message="Missing col")]
        )
        assert _categorize_errors(result) == "header_validation_failure"


class TestGUIDService:
    """Test suite for GUID generation with API fallback."""

    def test_guid_api_success(self):
        """API call should return a valid UUID string."""
        mock_response = MagicMock()
        mock_response.json.return_value = ["550e8400-e29b-41d4-a716-446655440000"]
        mock_response.raise_for_status = MagicMock()

        with patch('app.guid_service.requests.get', return_value=mock_response):
            error_id, used_api = generate_error_id()

        assert used_api is True
        assert error_id == "550e8400-e29b-41d4-a716-446655440000"

    def test_guid_api_fallback_on_failure(self):
        """When API fails, a local UUID must be generated."""
        with patch('app.guid_service.requests.get', side_effect=Exception("Network error")):
            error_id, used_api = generate_error_id()

        assert used_api is False
        assert len(error_id) == 36  # UUID format
        assert '-' in error_id

    def test_guid_api_fallback_records_method(self, tmp_dir):
        """Error log must indicate whether API or fallback was used."""
        result = ValidationResult(
            filename="test.csv",
            is_valid=False,
            errors=[ValidationError(rule="test", message="Error")]
        )

        with patch('app.guid_service.requests.get', side_effect=Exception("Down")):
            with patch('app.error_logger.ERROR_LOGS_DIR', tmp_dir):
                _, log_path = create_error_log(result, "/tmp/test.csv")

        with open(log_path, 'r') as f:
            data = json.load(f)
        assert data['generated_via'] == "local_uuid_fallback"
