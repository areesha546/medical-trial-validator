# Agile Evaluation Document

**Author:** Areesha Anum  
**Project:** Medical Trial Data Validation and Archival System  
**Institution:** Centrala University – School of Medicine  
**Date:** 2024

---

## 1. Introduction

This document evaluates the contribution of Agile techniques, ceremonies, and asset creation to the development of the Medical Trial Data Validation System. It examines which practices helped, which could have hindered, and provides a justified overall judgement.

---

## 2. Agile Techniques Applied

### 2.1 Test-Driven Development (TDD)

**Applied:** Yes – all validation rules were developed using a red-green-refactor cycle.

**How it helped:**
- Failing tests were written first for each validation rule (filename format, header checks, batch uniqueness, reading limits)
- Implementation was then written to make tests pass
- This ensured every business rule was covered before any code was written
- Refactoring was safe because tests caught regressions immediately

**Evidence:**
- `tests/test_filename_validation.py` – 8 test cases for filename rules
- `tests/test_csv_validation.py` – 7 test cases for CSV structure
- `tests/test_batch_rules.py` – 5 test cases for batch_id rules
- `tests/test_reading_rules.py` – 9 test cases for reading values
- `tests/test_error_logging.py` – 8 test cases for error logs and GUID
- `tests/test_tracker.py` – 8 test cases for duplicate detection

**Verdict:** TDD **helped significantly**. It reduced debugging time and gave confidence that validation rules worked correctly.

### 2.2 Iterative Development

**Applied:** Yes – the project was built in phases.

**Phases followed:**
1. Core validation logic (validators and models)
2. FTP integration and file tracking
3. Archival and error logging
4. Web UI dashboard
5. Docker containerisation
6. CI/CD pipeline
7. Documentation

**How it helped:**
- Each phase produced a working increment
- Problems were discovered early rather than at the end
- The web UI could be tested with sample data before FTP was connected

**Verdict:** Iterative development **helped** by reducing risk and allowing early feedback.

### 2.3 User Stories

**Applied:** Yes – requirements were captured as user stories.

**Examples:**
- *"As Areesha Anum, I want every file to be validated against strict rules so that only high-quality data is archived."*
- *"As Areesha Anum, I want invalid files to be quarantined and logged so that they can be investigated later."*

**How it helped:**
- Kept focus on what the user actually needs
- Provided clear acceptance criteria for each feature
- Made it easy to verify completeness

**Verdict:** User stories **helped** by keeping the development user-focused and measurable.

---

## 3. Agile Ceremonies Evaluation

### 3.1 Sprint Planning

**Would it help?** Partially.

For a solo project, formal sprint planning ceremonies are unnecessary. However, the concept of planning work in short iterations was valuable. Breaking the project into phases (as described above) served the same purpose.

**Verdict:** The concept helped; the formal ceremony would have been **unnecessary overhead** for a solo project.

### 3.2 Daily Stand-ups

**Would it help?** No.

Daily stand-ups are designed for team communication. As a solo developer, there is no team to synchronise with. Time would be better spent working on the project.

**Verdict:** Would have **hindered** by consuming time with no benefit.

### 3.3 Sprint Reviews / Demos

**Would it help?** Yes, partially.

Demonstrating progress to a tutor or peer at the end of each phase would have provided valuable feedback. This is similar to showing assignment progress to a tutor during development.

**Verdict:** Would have **helped** if a reviewer was available.

### 3.4 Retrospectives

**Would it help?** Marginally.

Reflecting on what went well and what could improve is always useful. However, for a short-duration solo project, this can be done informally rather than as a structured ceremony.

**Verdict:** The practice of reflection **helped**; a formal ceremony would have been **neutral**.

---

## 4. Agile Asset Creation Evaluation

### 4.1 Product Backlog

**Created:** Yes – the full requirements document served as the product backlog, listing all features with priority.

**Value:** High. Having a clear list of everything to build prevented missing features and allowed prioritisation.

### 4.2 Test Cases

**Created:** Yes – 45+ automated test cases covering all validation rules.

**Value:** Very high. Automated tests caught bugs early and served as living documentation of business rules.

### 4.3 CI/CD Pipeline

**Created:** Yes – GitHub Actions pipeline running tests, syntax checks, and Docker build.

**Value:** High. Automated quality checks on every push prevent broken code from being merged.

### 4.4 Documentation

**Created:** Yes – README, Task 1 paradigms document, and this Agile evaluation.

**Value:** High. Documentation ensures the project is understandable, maintainable, and ready for submission.

### 4.5 Kanban/Task Board

**Applied:** Informally – tasks were tracked through the phased development approach.

**Value:** Moderate. A visual board would have helped track progress but was not essential for a solo project of this size.

---

## 5. Overall Judgement

### Did Agile techniques help or hinder this project?

**Overall verdict: Agile techniques mostly HELPED.**

| Technique | Impact |
|---|---|
| TDD | ✅ Strongly helped |
| Iterative development | ✅ Helped |
| User stories | ✅ Helped |
| Sprint planning (concept) | ✅ Helped |
| Daily stand-ups | ❌ Would hinder (solo project) |
| Sprint reviews | ⚠️ Would help if reviewer available |
| Retrospectives (informal) | ✅ Marginally helped |
| Product backlog | ✅ Helped |
| Automated test suite | ✅ Strongly helped |
| CI/CD pipeline | ✅ Helped |
| Documentation | ✅ Helped |

### Key Insight

Agile is designed for teams working on evolving products. For a solo university project with fixed requirements, **the technical practices** (TDD, CI/CD, iterative development) provide clear value, while **the collaborative ceremonies** (stand-ups, formal retrospectives) provide little benefit without a team.

The most effective approach for this project was to adopt Agile's **engineering practices** while using a **simplified project management** approach – essentially a hybrid of Agile principles with practical solo development.

---

## 6. Conclusion

Agile techniques, when selectively applied, significantly improved the quality and reliability of the Medical Trial Data Validation System. TDD ensured comprehensive test coverage. Iterative development reduced risk. CI/CD automated quality assurance. The key lesson is that Agile practices should be adapted to the project context – a solo academic project benefits most from Agile's engineering discipline while simplifying its collaborative ceremonies.

---

**Author:** Areesha Anum  
**Centrala University – School of Medicine**
