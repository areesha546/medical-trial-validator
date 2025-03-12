"""
Shared test fixtures and utilities.
Author: Areesha Anum
"""

import csv
import os
import pytest
import tempfile
from pathlib import Path


VALID_HEADERS = [
    "batch_id", "timestamp",
    "reading1", "reading2", "reading3", "reading4", "reading5",
    "reading6", "reading7", "reading8", "reading9", "reading10"
]


@pytest.fixture
def tmp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


@pytest.fixture
def valid_csv(tmp_dir):
    """Create a valid CSV file with correct filename and data."""
    filepath = tmp_dir / "MED_DATA_20230603140104.csv"
    rows = [
        {"batch_id": "55", "timestamp": "14:01:04",
         "reading1": "9.875", "reading2": "9.138", "reading3": "1.115",
         "reading4": "8.006", "reading5": "3.84", "reading6": "4.952",
         "reading7": "9.038", "reading8": "1.046", "reading9": "2.179",
         "reading10": "8.701"},
        {"batch_id": "64", "timestamp": "14:01:04",
         "reading1": "4.168", "reading2": "9.247", "reading3": "1.958",
         "reading4": "1.65", "reading5": "3.631", "reading6": "9.317",
         "reading7": "8.182", "reading8": "9.292", "reading9": "5.978",
         "reading10": "8.06"},
    ]
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=VALID_HEADERS)
        writer.writeheader()
        writer.writerows(rows)
    return filepath


@pytest.fixture
def make_csv(tmp_dir):
    """Factory fixture to create custom CSV files."""
    def _make_csv(filename, headers=None, rows=None, raw_content=None):
        filepath = tmp_dir / filename
        if raw_content is not None:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(raw_content)
        else:
            headers = headers or VALID_HEADERS
            rows = rows or []
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(rows)
        return filepath
    return _make_csv
