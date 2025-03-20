"""
Sample data generator for testing the validation system.
Author: Areesha Anum

Generates various valid and invalid CSV files for comprehensive testing.
"""

import csv
import os
import random
from datetime import datetime
from pathlib import Path


def get_output_dir():
    """Get the sample data output directory."""
    output_dir = Path(__file__).parent.parent / "data" / "sample_files"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


VALID_HEADERS = [
    "batch_id", "timestamp",
    "reading1", "reading2", "reading3", "reading4", "reading5",
    "reading6", "reading7", "reading8", "reading9", "reading10"
]


def _random_reading(max_val=9.9):
    """Generate a valid random reading."""
    return round(random.uniform(0.1, max_val), 3)


def _random_timestamp():
    """Generate a random timestamp string."""
    return f"14:01:0{random.randint(0, 9)}"


def generate_valid_file():
    """Generate a valid CSV file with correct format and data."""
    output_dir = get_output_dir()
    filename = "MED_DATA_20230603140104.csv"
    filepath = output_dir / filename

    rows = []
    for i in range(1, 11):
        row = {
            "batch_id": str(i * 10 + random.randint(1, 9)),
            "timestamp": _random_timestamp(),
        }
        for j in range(1, 11):
            row[f"reading{j}"] = str(_random_reading())
        rows.append(row)

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=VALID_HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Generated valid file: {filepath}")
    return filepath


def generate_invalid_filename():
    """Generate a CSV with invalid filename."""
    output_dir = get_output_dir()
    filename = "BAD_FILENAME_2023.csv"
    filepath = output_dir / filename

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=VALID_HEADERS)
        writer.writeheader()
        row = {"batch_id": "1", "timestamp": "14:01:04"}
        for j in range(1, 11):
            row[f"reading{j}"] = str(_random_reading())
        writer.writerow(row)

    print(f"✓ Generated invalid filename file: {filepath}")
    return filepath


def generate_duplicate_batch_id():
    """Generate a CSV with duplicate batch IDs."""
    output_dir = get_output_dir()
    filename = "MED_DATA_20230604100000.csv"
    filepath = output_dir / filename

    rows = []
    for i in range(5):
        row = {"batch_id": "55", "timestamp": _random_timestamp()}  # Same batch_id
        for j in range(1, 11):
            row[f"reading{j}"] = str(_random_reading())
        rows.append(row)

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=VALID_HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Generated duplicate batch_id file: {filepath}")
    return filepath


def generate_missing_header():
    """Generate a CSV with a missing required header."""
    output_dir = get_output_dir()
    filename = "MED_DATA_20230605120000.csv"
    filepath = output_dir / filename

    # Missing 'reading10'
    bad_headers = VALID_HEADERS[:-1]
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=bad_headers)
        writer.writeheader()
        row = {"batch_id": "1", "timestamp": "14:01:04"}
        for j in range(1, 10):
            row[f"reading{j}"] = str(_random_reading())
        writer.writerow(row)

    print(f"✓ Generated missing header file: {filepath}")
    return filepath


def generate_misspelled_header():
    """Generate a CSV with misspelled header (batch instead of batch_id)."""
    output_dir = get_output_dir()
    filename = "MED_DATA_20230606130000.csv"
    filepath = output_dir / filename

    bad_headers = ["batch", "timestamp"] + [f"reading{i}" for i in range(1, 11)]
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(bad_headers)
        row = ["1", "14:01:04"] + [str(_random_reading()) for _ in range(10)]
        writer.writerow(row)

    print(f"✓ Generated misspelled header file: {filepath}")
    return filepath


def generate_missing_readings():
    """Generate a CSV with missing reading values."""
    output_dir = get_output_dir()
    filename = "MED_DATA_20230607140000.csv"
    filepath = output_dir / filename

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(VALID_HEADERS)
        # Row with missing readings (empty values)
        row = ["1", "14:01:04", "1.5", "2.3", "", "", "5.1", "6.2", "", "8.0", "9.1", ""]
        writer.writerow(row)

    print(f"✓ Generated missing readings file: {filepath}")
    return filepath


def generate_value_over_max():
    """Generate a CSV with reading values exceeding 9.9."""
    output_dir = get_output_dir()
    filename = "MED_DATA_20230608150000.csv"
    filepath = output_dir / filename

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(VALID_HEADERS)
        row = ["1", "14:01:04", "1.5", "10.5", "2.3", "15.0", "5.1", "6.2", "7.3", "8.0", "9.1", "9.9"]
        writer.writerow(row)

    print(f"✓ Generated value over max file: {filepath}")
    return filepath


def generate_invalid_text_reading():
    """Generate a CSV with text instead of numeric readings."""
    output_dir = get_output_dir()
    filename = "MED_DATA_20230609160000.csv"
    filepath = output_dir / filename

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(VALID_HEADERS)
        row = ["1", "14:01:04", "1.5", "nil", "abc", "N/A", "5.1", "6.2", "7.3", "8.0", "9.1", "9.0"]
        writer.writerow(row)

    print(f"✓ Generated invalid text reading file: {filepath}")
    return filepath


def generate_malformed_csv():
    """Generate a malformed CSV file."""
    output_dir = get_output_dir()
    filename = "MED_DATA_20230610170000.csv"
    filepath = output_dir / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(','.join(VALID_HEADERS) + '\n')
        f.write('1,14:01:04,1.5,2.3,3.4,4.5,5.6,6.7,7.8,8.9,9.0,1.1\n')
        f.write('2,14:01:05,broken row with "unclosed quote\n')
        f.write('3,14:01:06,1.5,2.3\n')  # Too few columns

    print(f"✓ Generated malformed CSV file: {filepath}")
    return filepath


def generate_empty_file():
    """Generate an empty 0-byte CSV file."""
    output_dir = get_output_dir()
    filename = "MED_DATA_20230611180000.csv"
    filepath = output_dir / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        pass  # Empty file

    print(f"✓ Generated empty file: {filepath}")
    return filepath


def generate_all_samples():
    """Generate all sample data files."""
    print("=" * 60)
    print("Generating Sample Data Files")
    print("Author: Areesha Anum")
    print("=" * 60)

    files = [
        generate_valid_file(),
        generate_invalid_filename(),
        generate_duplicate_batch_id(),
        generate_missing_header(),
        generate_misspelled_header(),
        generate_missing_readings(),
        generate_value_over_max(),
        generate_invalid_text_reading(),
        generate_malformed_csv(),
        generate_empty_file(),
    ]

    print(f"\n{'=' * 60}")
    print(f"Generated {len(files)} sample files in: {get_output_dir()}")
    print("=" * 60)
    return files


if __name__ == "__main__":
    generate_all_samples()
