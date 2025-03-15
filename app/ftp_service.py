"""
FTP Service for connecting to the remote FTP server.
Author: Areesha Anum

Handles connection, directory listing, and file downloads.
"""

import ftplib
import logging
from pathlib import Path
from typing import List, Optional

from app.config import (
    FTP_HOST, FTP_PORT, FTP_USERNAME, FTP_PASSWORD,
    FTP_REMOTE_DIR, DOWNLOADS_DIR
)

logger = logging.getLogger(__name__)


class FTPService:
    """Service for interacting with the remote FTP server."""

    def __init__(self, host=None, port=None, username=None, password=None, remote_dir=None):
        self.host = host or FTP_HOST
        self.port = port or FTP_PORT
        self.username = username or FTP_USERNAME
        self.password = password or FTP_PASSWORD
        self.remote_dir = remote_dir or FTP_REMOTE_DIR
        self.connection: Optional[ftplib.FTP] = None

    def connect(self) -> bool:
        """Establish FTP connection. Returns True on success."""
        try:
            self.connection = ftplib.FTP()
            self.connection.connect(self.host, self.port, timeout=10)
            self.connection.login(self.username, self.password)
            logger.info(f"Connected to FTP server {self.host}:{self.port}")
            return True
        except ftplib.all_errors as e:
            logger.error(f"FTP connection failed: {str(e)}")
            self.connection = None
            return False

    def disconnect(self):
        """Close FTP connection safely."""
        if self.connection:
            try:
                self.connection.quit()
            except ftplib.all_errors:
                try:
                    self.connection.close()
                except Exception:
                    pass
            self.connection = None
            logger.info("Disconnected from FTP server")

    def list_csv_files(self) -> List[str]:
        """List CSV files in the remote directory."""
        if not self.connection:
            logger.error("Not connected to FTP server")
            return []

        try:
            self.connection.cwd(self.remote_dir)
            files = self.connection.nlst()
            csv_files = [f for f in files if f.lower().endswith('.csv')]
            logger.info(f"Found {len(csv_files)} CSV files on server")
            return csv_files
        except ftplib.all_errors as e:
            logger.error(f"Failed to list files: {str(e)}")
            return []

    def download_file(self, remote_filename: str) -> Optional[Path]:
        """
        Download a file from the FTP server.
        Returns the local path or None on failure.
        """
        if not self.connection:
            logger.error("Not connected to FTP server")
            return None

        DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
        local_path = DOWNLOADS_DIR / remote_filename

        try:
            with open(local_path, 'wb') as f:
                self.connection.retrbinary(f"RETR {remote_filename}", f.write)
            logger.info(f"Downloaded: {remote_filename} -> {local_path}")

            # Check for empty files
            if local_path.stat().st_size == 0:
                logger.warning(f"Downloaded file is empty: {remote_filename}")

            return local_path
        except ftplib.all_errors as e:
            logger.error(f"Failed to download {remote_filename}: {str(e)}")
            if local_path.exists():
                local_path.unlink()
            return None

    def is_connected(self) -> bool:
        """Check if FTP connection is active."""
        if not self.connection:
            return False
        try:
            self.connection.voidcmd("NOOP")
            return True
        except ftplib.all_errors:
            return False
