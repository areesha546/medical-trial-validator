# Task 1: Programming Paradigms Briefing Document

**Author:** Areesha Anum  
**For:** Luzo Okake, CEO – Centrala University Software Development Studio  
**Project:** Medical Trial Data Validation and Archival System  
**Date:** 2024

---

## 1. Overview of Common Programming Paradigms

### 1.1 Procedural Programming

Procedural programming follows a top-down, step-by-step approach where the program is structured as a sequence of procedures (functions) that operate on data. Each function performs a specific task, and the program flows through these functions in order.

**Key characteristics:**
- Linear, step-by-step execution
- Functions that take inputs and produce outputs
- Shared state through global or passed variables
- Easy to follow for sequential workflows

**Languages:** C, Pascal, Fortran, early BASIC

**Example use case:** A simple script that reads a file, processes each line, and writes output – each step is a function called in sequence.

### 1.2 Object-Oriented Programming (OOP)

Object-oriented programming organises code around objects – self-contained units that combine data (attributes) and behaviour (methods). Objects interact through defined interfaces, promoting encapsulation, inheritance, and polymorphism.

**Key characteristics:**
- Encapsulation – bundling data and methods together
- Inheritance – creating specialised classes from general ones
- Polymorphism – same interface, different implementations
- Abstraction – hiding complexity behind simple interfaces

**Languages:** Python, Java, C#, C++, Ruby

**Example use case:** A validation system where different validator classes share a common interface but each implements its own validation logic.

### 1.3 Functional Programming

Functional programming treats computation as the evaluation of mathematical functions. It emphasises immutability (data that doesn't change), pure functions (no side effects), and function composition.

**Key characteristics:**
- Pure functions with no side effects
- Immutable data
- Higher-order functions (functions as arguments)
- Declarative style

**Languages:** Haskell, Erlang, Clojure, Scala, F#

**Example use case:** Data transformation pipelines where each step transforms data without modifying the original.

### 1.4 Event-Driven Programming

Event-driven programming structures the program around events – user actions, system signals, or messages. The program waits for events and responds with appropriate handlers.

**Key characteristics:**
- Event listeners and handlers
- Asynchronous processing
- Callback functions
- Reactive to external inputs

**Languages:** JavaScript, C# (GUI frameworks), Python (with GUI libraries)

**Example use case:** A web application that responds to button clicks, form submissions, and API requests.

---

## 2. Selected Paradigm for This Project

### Primary: Object-Oriented Programming (OOP)

### Supporting: Procedural elements where appropriate

---

## 3. Justification for the Selected Paradigm

### 3.1 Why Object-Oriented Programming?

The Medical Trial Data Validation System has clearly defined components that map naturally to objects:

| Component | Object/Class |
|---|---|
| FTP connection handling | `FTPService` class |
| File validation rules | `BaseValidator`, `FilenameValidator`, `HeaderValidator`, etc. |
| File tracking | `FileTracker` with SQLite operations |
| Error logging | `ErrorLogger` service |
| Processing results | `ValidationResult`, `ProcessingResult` dataclasses |

**Encapsulation** allows each service to manage its own data and logic independently. The `FTPService` class encapsulates connection details and methods, making it testable in isolation.

**Polymorphism** is demonstrated through the Chain of Responsibility pattern, where each validator shares the same interface (`BaseValidator`) but implements different validation logic. New validators can be added without modifying existing code.

**Abstraction** hides implementation complexity. The main pipeline simply calls `validate_file()` without knowing the details of each validation step.

### 3.2 Why Procedural Elements?

Some parts of the system are naturally sequential:
- The main processing pipeline follows a clear order: download → validate → archive/reject
- Configuration loading is a straightforward setup task
- Sample data generation scripts are procedural by nature

Using procedural code where it makes sense keeps the solution simple and avoids unnecessary complexity.

### 3.3 Why Not Pure Functional?

While functional programming concepts like pure functions are used in validation logic, a fully functional approach would add unnecessary complexity for this project. The system needs to manage state (database records, file system operations, FTP connections), which is more natural in OOP.

### 3.4 Why Not Event-Driven?

The Flask web UI uses event-driven patterns (responding to HTTP requests), but the core processing logic is not event-driven. The system processes files in batches through a defined pipeline, not in response to real-time events.

---

## 4. Language Selection: Python

### 4.1 Why Python?

| Criterion | Python Advantage |
|---|---|
| FTP support | Built-in `ftplib` module |
| CSV processing | Built-in `csv` module |
| Testing | Excellent `pytest` framework |
| Web UI | Flask – lightweight and well-documented |
| Containerisation | Simple Dockerfile, small image possible |
| Learning curve | Readable syntax aids development speed |
| Libraries | Rich ecosystem for all project requirements |
| OOP support | Full class-based OOP with clear syntax |

### 4.2 Alternatives Considered

- **Java:** Strong OOP but heavier setup, slower development cycle for this scope
- **JavaScript/Node.js:** Good for web but FTP and CSV handling are less mature
- **C#:** Excellent .NET support but less portable for Docker deployment

### 4.3 Final Decision

Python 3.11+ provides the best balance of development speed, library support, testing tools, and containerisation simplicity for this university medical trial data project.

---

## 5. Conclusion

The Medical Trial Data Validation System uses **Object-Oriented Programming with modular procedural elements**. This approach is justified because:

1. The project has clearly defined components (FTP, validation, archival, logging) that map directly to classes
2. The Chain of Responsibility design pattern requires polymorphic validator objects
3. Each module can be developed and tested independently
4. The procedural pipeline orchestration keeps the overall flow simple and readable
5. Python's OOP features, combined with its strong standard library, make it the ideal implementation language

This combination delivers a maintainable, testable, and extensible solution that meets all assignment requirements.

---

**Author:** Areesha Anum  
**Centrala University – School of Medicine**
