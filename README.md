
# Survey Builder Application (Model Project)

This is a **model project** for the course *Zarządzanie projektami IT*. 
It demonstrates a lightweight agile workflow, CI/CD, quality checks, and documentation structure for a web-based survey creation platform.

## Quickstart
1. Create a new repository and copy these files.
2. (Optional) Set `SONAR_TOKEN` and `SONAR_HOST_URL` as repository secrets if you use SonarQube/SonarCloud.
3. Run locally:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   pytest -q
   ```
4. Push to main — CI will run tests and linters.

## Vision
Deliver a minimal **Survey Builder Application** that lets a user:
- create surveys with multiple question types (text, multiple choice, scale),
- publish surveys and generate shareable links,
- collect responses from participants,
- view basic statistics and export results as CSV.

## Tech Stack
- Backend: Python (Flask/FastAPI)
- Storage: In-memory with JSON persistence
- Testing: pytest, flake8, black, bandit
- CI/CD: GitHub Actions

## Project Structure
```
survey_builder_project/
├── src/                    # Source code
├── tests/                  # Unit tests
├── docs/                   # Documentation
├── .github/workflows/      # CI/CD configuration
├── BACKLOG.csv            # Product backlog
├── PROJECT_CHARTER.md     # Project charter
├── SPRINT1_PLAN.md        # Sprint planning
├── RISK_REGISTER.csv      # Risk management
└── requirements.txt       # Python dependencies
```
