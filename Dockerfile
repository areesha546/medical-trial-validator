# Areesha Anum - Centrala University Medical Trial Data Validation System
# Dockerfile for containerised deployment

FROM python:3.11-slim

# Set metadata
LABEL maintainer="Areesha Anum"
LABEL description="Centrala University Medical Trial Data Validation and Archival System"

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_DEBUG=false
ENV FLASK_PORT=5000
ENV DATABASE_PATH=data/tracker.db

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create required directories
RUN mkdir -p data/downloads data/archive data/rejected data/sample_files logs/errors

# Generate sample data for testing
RUN python scripts/generate_sample_data.py

# Expose the Flask port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/')" || exit 1

# Run the application
CMD ["python", "run.py"]
