Centrala University Medical Trial Data Validation and Archival System

Author: Areesha Anum
Institution: Centrala University, School of Medicine
University: Big Academy, Riyadh.
Module: Unit 11, Advanced Programming
Date: April 2025

<img width="1600" height="695" alt="image" src="https://github.com/user-attachments/assets/9ebb08ce-1481-495a-8398-ec360f3c752d" />
<img width="1003" height="407" alt="image" src="https://github.com/user-attachments/assets/e4b84da4-cddf-4881-8c42-4df43bfeb208" />
<img width="1600" height="853" alt="image" src="https://github.com/user-attachments/assets/fcc73dd2-f7af-4e14-a768-40fea4797ed4" />
<img width="1600" height="751" alt="image" src="https://github.com/user-attachments/assets/e7a29585-40c9-4abf-8ca5-0dea2f15a78d" />
<img width="1432" height="381" alt="image" src="https://github.com/user-attachments/assets/d7a3ec0a-fd11-475b-bc5b-a09b2e12312f" />
<img width="1600" height="805" alt="image" src="https://github.com/user-attachments/assets/87d5f34c-0e94-4e7e-b6a0-e16f63d0e8a6" />

Table of Contents
What This Project Does
How the System Works
Screenshots and Demo
Key Features
Technology Stack
Project Structure
Setup Instructions
Running the Tests
Docker Containerisation
CI/CD Pipeline
Validation Rules
Design Pattern Used
API Endpoints
Version Control and Git Workflow
Agile Methodology
Author and Acknowledgements
What This Project Does

This project was developed to automate the validation and archival of medical trial data files for Centrala University. In a real healthcare or research environment, large volumes of trial readings are collected daily and stored as CSV files on a remote FTP server. Before that data can be trusted and used for research, every file must be checked carefully to make sure it is complete, accurate, and in the correct format.

This system handles that process automatically.

It connects to an FTP server, downloads CSV files, validates each one through a structured pipeline, and then decides what should happen next. If a file passes all checks, it is archived into a date-based folder structure. If it fails validation, it is moved to quarantine and a detailed error log is generated. Each error log also includes a unique identifier retrieved from an external GUID API. To avoid duplicate work, the system tracks every processed file in a SQLite database. A web dashboard is also included so the full workflow can be monitored in a simple and visual way.

This project was built using Test-Driven Development, which means the tests were written before the implementation, and it uses the Chain of Responsibility design pattern to keep the validation logic modular, maintainable, and easy to extend.

How the System Works

At a high level, the system follows a clear step-by-step process from file collection to final storage.

First, CSV files are placed on the FTP server. The application connects to that server and downloads any new files that have not already been processed. Once a file is downloaded, the system checks its processing history using SQLite to make sure the same file is not handled twice.

The file is then passed through a validation pipeline made up of five separate checks. The first validator checks whether the filename follows the required format: MED_DATA_YYYYMMDDHHMMSS.csv. The second confirms that all required headers are present. The third checks that no rows contain missing values. The fourth ensures that every batch_id is unique within the file. The fifth validates the numerical readings, making sure they are real numbers, do not exceed 9.9, and contain no more than three decimal places.

If the file passes every rule, it is archived into a structured folder path based on date, such as 2025/04/02/. If the file fails any validation step, it is moved into a rejected area and a JSON error log is created to record exactly what went wrong.

The entire process can be monitored through the web dashboard, which provides real-time visibility into file processing activity, history, and errors.

Screenshots and Demo
Main Dashboard

The dashboard provides a simple overview of the system. It shows processing statistics, allows the user to scan the FTP server or upload a file manually, and displays the full file processing history in one place.

Error Logs Viewer

If a file fails validation, the system records detailed information about the failure. The error viewer shows which rule failed, where the issue occurred, and the unique error ID associated with that failure.

Test Results

The system was developed using Test-Driven Development, and all 45 tests pass successfully. This demonstrates that the application is stable, reliable, and well covered by automated testing.

Key Features

This project includes a complete set of features needed to manage and validate medical trial CSV files in a structured and dependable way.

The system connects to an FTP server and downloads files automatically. It uses SQLite to track which files have already been processed so that duplicates are never handled twice. It validates filenames against a strict naming convention, checks CSV headers and row completeness, verifies that all batch_id values are unique, and ensures that all trial readings follow the required numeric rules.

When a file fails validation, the system creates a structured JSON error log and generates a unique ID using an external GUID API. Valid files are archived into a date-based folder structure, while invalid files are quarantined for further review. The application also includes a Flask-based dashboard for monitoring the process, along with sample data generation scripts, Docker support, and a GitHub Actions CI/CD pipeline.

Technology Stack

This project was built using Python 3.11 because it is a strong and widely used language for backend development, data handling, and automation. Flask was selected for the web interface because it is lightweight and well suited for dashboard-style applications. SQLite was used for file tracking because it is simple, reliable, and does not require any separate database setup.

Testing was done with pytest, which made it easier to create a clean and maintainable TDD workflow. FTP functionality was handled using ftplib and pyftpdlib, while Docker and Docker Compose were used to containerise the application and create a reproducible deployment environment. GitHub Actions was used to automate testing and Docker builds through CI/CD. The external GUID API from uuidtools.com was used to generate unique identifiers for error logging.

From a design perspective, the Chain of Responsibility pattern was chosen because it fits the validation workflow naturally and allows each validation rule to be kept separate and focused.

Project Structure
Areesha/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── validator.py
│   ├── ftp_service.py
│   ├── file_tracker.py
│   ├── archive_service.py
│   ├── error_logger.py
│   ├── guid_service.py
│   ├── main.py
│   ├── ui/
│   │   ├── __init__.py
│   │   └── routes.py
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       └── errors.html
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_filename_validation.py
│   ├── test_csv_validation.py
│   ├── test_batch_rules.py
│   ├── test_reading_rules.py
│   ├── test_error_logging.py
│   └── test_tracker.py
├── scripts/
│   ├── generate_sample_data.py
│   └── start_test_ftp.py
├── data/
│   ├── downloads/
│   ├── archive/
│   ├── rejected/
│   └── sample_files/
├── logs/
│   └── errors/
├── docs/
│   ├── screenshots/
│   ├── task1_paradigms.md
│   └── agile_evaluation.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.py
├── .env.example
├── .gitignore
└── README.md

The structure was organised to keep the project clean and easy to navigate. Core logic is placed inside the app package, tests are grouped separately, helper scripts are placed in the scripts folder, and data, logs, and documentation each have dedicated directories.

Setup Instructions
Prerequisites

Before running the project, the following tools should be installed:

Python 3.11 or higher
pip
Docker Desktop
Git
Clone the Repository
git clone <repository-url>
cd Areesha
Create a Virtual Environment
python -m venv venv

On Windows:

venv\Scripts\activate

On Linux or Mac:

source venv/bin/activate
Install Dependencies
pip install -r requirements.txt
Configure Environment Variables
copy .env.example .env

Then update the .env file with the required FTP credentials:

FTP_HOST=localhost
FTP_PORT=2121
FTP_USERNAME=centrala
FTP_PASSWORD=medical2024
FTP_REMOTE_DIR=/trial_data

The .env file contains sensitive information and should never be shared publicly. It is excluded from version control through .gitignore.

Run the Application
python run.py

After starting the application, open a browser and go to:

http://localhost:5000

Start the Test FTP Server

In a separate terminal, run:

python scripts/start_test_ftp.py
Generate Sample Data
python scripts/generate_sample_data.py

This creates sample CSV files that can be used to test both valid and invalid scenarios.

Running the Tests

This project was developed using Test-Driven Development, so automated tests were a core part of the implementation from the beginning. The test suite contains 45 tests across multiple modules and covers the key parts of the system.

To run all tests:

pytest tests/ -v

To run tests with coverage:

pytest tests/ -v --cov=app --cov-report=term-missing

To run a specific file:

pytest tests/test_filename_validation.py -v

The tests cover filename validation, CSV structure checks, batch validation, reading validation, error logging, and file tracking. This helps ensure the system behaves correctly and remains stable as it grows.

Docker Containerisation

The application is fully containerised using Docker so it can run consistently across different environments.

The Dockerfile uses Python 3.11 slim as the base image and installs only the required dependencies. It sets up the project, creates the necessary directories, and runs the Flask application on port 5000.

To build the Docker image:

docker build -t medical-trial-validator .

To run the container:

docker run -p 5000:5000 --name medical-validator medical-trial-validator

Docker Compose is also included for running the full setup more easily. It starts both the web application and a test FTP server together.

docker-compose up --build

To run it in detached mode:

docker-compose up --build -d

To stop all services:

docker-compose down

This setup makes the system easier to deploy, test, and demonstrate in a consistent way.

CI/CD Pipeline

This project includes a GitHub Actions CI/CD pipeline that runs automatically whenever code is pushed or a pull request is opened.

The pipeline is split into three stages. The first stage runs the test suite and checks that all functionality works correctly. The second stage performs code quality checks to make sure the project is syntactically valid and properly structured. The final stage builds the Docker image, but only if the earlier stages succeed.

This setup helps ensure that only stable and tested code reaches the main branch. It also reflects good engineering practice by automating validation and reducing the risk of broken deployments.

A simplified view of the pipeline is shown below:

name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
  lint:
  docker:
Validation Rules

Every file must pass all validation rules before it can be archived.

The first rule checks the filename format. Each file must follow the exact pattern MED_DATA_YYYYMMDDHHMMSS.csv. If the name is incorrect, the file is rejected immediately.

The second rule checks the CSV headers. The file must contain all required columns: batch_id, timestamp, and reading1 through reading10.

The third rule checks for missing values. Every row must be complete and no field can be left blank.

The fourth rule checks that every batch_id is unique within the file. Duplicate IDs suggest corrupted or unreliable data.

The fifth rule validates the reading values. Each reading must be numeric, must not be greater than 9.9, and must contain no more than three decimal places.

This rule-based approach keeps the system strict and reliable, which is especially important for medical and research data.

Design Pattern Used

The main design pattern used in this project is the Chain of Responsibility pattern.

This pattern was a good fit because the validation process naturally happens in stages. Each validator is responsible for one specific rule, such as checking the filename, validating the headers, or inspecting the readings. After completing its task, each validator passes the file to the next one in the chain.

This approach keeps the code clean and easier to maintain. It also makes the system easy to extend. If a new validation rule needs to be added later, a new validator can simply be inserted into the chain without changing the existing ones. That makes the design modular, testable, and aligned with good software engineering practice.

API Endpoints

The application includes both web routes and JSON endpoints.

HTML Routes
Endpoint	Method	Description
/	GET	Displays the main dashboard with processing statistics and file history
/errors	GET	Displays the error logs and failure details
Action Routes
Endpoint	Method	Description
/scan	POST	Scans the FTP server and processes all new CSV files
/upload	POST	Uploads and validates a single CSV file manually
JSON API Routes
Endpoint	Method	Description
/check-ftp	GET	Checks FTP connection status and returns the number of files available
/api/stats	GET	Returns processing statistics in JSON format
/api/records	GET	Returns processed file records in JSON format
Version Control and Git Workflow

Git was used for version control throughout the project, with GitHub acting as the remote repository.

The project followed a simple but effective branching strategy. The main branch was used for stable production-ready code, while develop was used as an integration branch during active development. Feature branches were used for individual tasks so that work could be developed in isolation before being merged.

The project was built incrementally through meaningful commits, covering stages such as project setup, validation logic, FTP integration, duplicate tracking, error logging, dashboard development, Docker support, CI/CD setup, and documentation.

Some of the main Git commands used during development included:

git init
git add .
git commit -m "descriptive message"
git remote add origin <repository-url>
git push -u origin main
git log --oneline

Using Git in this way helped keep the work organised and made the development process more structured and traceable.

Agile Methodology

This project was developed using Agile principles.

Work was divided into manageable stages, with features planned and implemented step by step. User stories helped define the system from the perspective of real use cases, while regular reviews made it easier to check progress and improve the project over time. Sprint-style thinking also helped break down the workload into smaller and more realistic deliverables.

Practices such as planning, review, iteration, and reflection were all part of the development process. A visual task board was also used to track progress from work still to do, to work in progress, and finally to completed tasks.

Using Agile in this project helped maintain clarity, improve organisation, and make the overall development process more manageable.

Author and Acknowledgements

Areesha Anum
Centrala University, School of Medicine
Unit 11, Advanced Programming

Acknowledgements

I would like to acknowledge Centrala University for providing the project brief and academic guidance for this work. I would also like to recognise the Python Software Foundation for the libraries and tools that supported development, the Flask team for the web framework, and uuidtools.com for the GUID generation API used in the error logging process.
