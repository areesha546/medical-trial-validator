"""
Test FTP server for local development and testing.
Author: Areesha Anum

Uses pyftpdlib to create a local FTP server with sample data.
"""

import os
import sys
import threading
from pathlib import Path

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def start_test_ftp_server(host="127.0.0.1", port=2121, username="centrala",
                          password="medical2024", directory=None, blocking=True):
    """
    Start a test FTP server serving sample data files.

    Args:
        host: Server host
        port: Server port
        username: FTP username
        password: FTP password
        directory: Directory to serve (defaults to data/sample_files)
        blocking: If True, blocks until stopped. If False, runs in a thread.
    """
    # Allow overrides from environment variables
    host = os.environ.get("FTP_HOST", host)
    port = int(os.environ.get("FTP_PORT", port))

    if directory is None:
        directory = str(Path(__file__).parent.parent / "data" / "sample_files")

    # Ensure directory exists
    Path(directory).mkdir(parents=True, exist_ok=True)

    # Create authorizer
    authorizer = DummyAuthorizer()
    authorizer.add_user(username, password, directory, perm="elradfmw")

    # Create handler
    handler = FTPHandler
    handler.authorizer = authorizer
    handler.passive_ports = range(60000, 60100)
    handler.banner = "Centrala University Medical Trial FTP Server"

    # Create server
    server = FTPServer((host, port), handler)
    server.max_cons = 10

    print(f"=" * 60)
    print(f"Test FTP Server Starting")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"User: {username}")
    print(f"Directory: {directory}")
    print(f"=" * 60)

    if blocking:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nFTP server stopped.")
            server.close_all()
    else:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        return server

    return server


if __name__ == "__main__":
    # Generate sample data first
    try:
        from scripts.generate_sample_data import generate_all_samples
    except ImportError:
        from generate_sample_data import generate_all_samples

    print("Generating sample data for FTP server...\n")
    generate_all_samples()
    print()

    start_test_ftp_server()
