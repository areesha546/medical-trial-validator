"""
Flask web UI routes for the Medical Trial Data Validation System.
Author: Areesha Anum

Provides a web dashboard for monitoring and controlling the pipeline.
"""

import os
import logging
from pathlib import Path

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash

from app.main import process_ftp_files, process_single_file, setup_logging
from app.ftp_service import FTPService
from app.file_tracker import get_all_records, get_processing_stats, init_database
from app.error_logger import get_recent_error_logs
from app.config import (
    FLASK_SECRET_KEY, FLASK_DEBUG, FLASK_PORT,
    FTP_HOST, FTP_PORT, FTP_USERNAME, DOWNLOADS_DIR, ARCHIVE_DIR, REJECTED_DIR
)

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(
        __name__,
        template_folder=str(Path(__file__).parent.parent.parent / 'app' / 'templates'),
        static_folder=str(Path(__file__).parent.parent.parent / 'app' / 'static')
    )
    app.secret_key = FLASK_SECRET_KEY

    # Setup logging
    setup_logging()

    # Initialise database
    init_database()

    @app.route('/')
    def dashboard():
        """Main dashboard page."""
        stats = get_processing_stats()
        records = get_all_records()
        return render_template('dashboard.html',
                               stats=stats,
                               records=records,
                               ftp_host=FTP_HOST,
                               ftp_port=FTP_PORT,
                               ftp_user=FTP_USERNAME)

    @app.route('/scan', methods=['POST'])
    def scan_ftp():
        """Scan FTP server and process new files."""
        try:
            results = process_ftp_files()

            valid_count = sum(1 for r in results if r.status == 'valid')
            invalid_count = sum(1 for r in results if r.status == 'invalid')
            skipped_count = sum(1 for r in results if r.status == 'skipped')
            error_count = sum(1 for r in results if r.status == 'error')

            if not results:
                flash('No new CSV files found on FTP server.', 'info')
            else:
                flash(
                    f'Processed {len(results)} file(s): '
                    f'{valid_count} valid, {invalid_count} invalid, '
                    f'{skipped_count} skipped, {error_count} errors.',
                    'success' if error_count == 0 else 'warning'
                )

        except Exception as e:
            flash(f'Error during FTP scan: {str(e)}', 'danger')
            logger.error(f"Scan error: {e}")

        return redirect(url_for('dashboard'))

    @app.route('/upload', methods=['POST'])
    def upload_file():
        """Upload and process a local CSV file (for testing)."""
        if 'file' not in request.files:
            flash('No file selected.', 'warning')
            return redirect(url_for('dashboard'))

        file = request.files['file']
        if file.filename == '':
            flash('No file selected.', 'warning')
            return redirect(url_for('dashboard'))

        if file:
            DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
            filepath = DOWNLOADS_DIR / file.filename
            file.save(str(filepath))

            result = process_single_file(filepath)

            if result.status == 'valid':
                flash(f'✓ {file.filename}: Valid and archived successfully.', 'success')
            elif result.status == 'invalid':
                flash(f'✗ {file.filename}: Invalid - {result.message}', 'danger')
            elif result.status == 'skipped':
                flash(f'⊘ {file.filename}: Already processed, skipped.', 'info')
            else:
                flash(f'⚠ {file.filename}: {result.message}', 'warning')

        return redirect(url_for('dashboard'))

    @app.route('/check-ftp')
    def check_ftp():
        """Check FTP connection status."""
        ftp = FTPService()
        connected = ftp.connect()
        files = []
        if connected:
            files = ftp.list_csv_files()
            ftp.disconnect()
        return jsonify({
            'connected': connected,
            'host': FTP_HOST,
            'port': FTP_PORT,
            'files_found': len(files),
            'files': files
        })

    @app.route('/errors')
    def error_logs():
        """View recent error logs."""
        logs = get_recent_error_logs()
        return render_template('errors.html', logs=logs)

    @app.route('/api/stats')
    def api_stats():
        """API endpoint for processing statistics."""
        return jsonify(get_processing_stats())

    @app.route('/api/records')
    def api_records():
        """API endpoint for all processed records."""
        records = get_all_records()
        return jsonify([{
            'filename': r.filename,
            'status': r.status,
            'processed_at': r.processed_at,
            'archive_path': r.archive_path,
            'error_id': r.error_id,
            'validation_errors': r.validation_errors
        } for r in records])

    return app


def run_app():
    """Run the Flask application."""
    app = create_app()
    app.run(host='0.0.0.0', port=FLASK_PORT, debug=FLASK_DEBUG)


if __name__ == '__main__':
    run_app()
