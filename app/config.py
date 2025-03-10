"""
Configuration module for the Medical Trial Data Validation System.
Author: Areesha Anum
Loads settings from environment variables with sensible defaults.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# FTP Configuration
FTP_HOST = os.getenv("FTP_HOST", "localhost")
FTP_PORT = int(os.getenv("FTP_PORT", "2121"))
FTP_USERNAME = os.getenv("FTP_USERNAME", "centrala")
FTP_PASSWORD = os.getenv("FTP_PASSWORD", "medical2024")
FTP_REMOTE_DIR = os.getenv("FTP_REMOTE_DIR", "/trial_data")

# GUID API
GUID_API_URL = os.getenv("GUID_API_URL", "https://www.uuidtools.com/api/generate/v1")

# Flask
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "true").lower() == "true"
FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))

# Paths
DATA_DIR = BASE_DIR / "data"
DOWNLOADS_DIR = DATA_DIR / "downloads"
ARCHIVE_DIR = DATA_DIR / "archive"
REJECTED_DIR = DATA_DIR / "rejected"
LOGS_DIR = BASE_DIR / "logs"
ERROR_LOGS_DIR = LOGS_DIR / "errors"
DATABASE_PATH = BASE_DIR / os.getenv("DATABASE_PATH", "data/tracker.db")

# Ensure directories exist
for d in [DOWNLOADS_DIR, ARCHIVE_DIR, REJECTED_DIR, ERROR_LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Validation constants
REQUIRED_HEADERS = [
    "batch_id", "timestamp",
    "reading1", "reading2", "reading3", "reading4", "reading5",
    "reading6", "reading7", "reading8", "reading9", "reading10"
]
FILENAME_PREFIX = "MED_DATA_"
FILENAME_EXTENSION = ".csv"
MAX_READING_VALUE = 9.9
MAX_DECIMAL_PLACES = 3
READING_COUNT = 10
