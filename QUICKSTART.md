# Quick Start Guide

## Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd survey_builder_project
```

### 2. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

### Start the Flask server
```bash
python src/app.py
```

The API will be available at `http://localhost:5000`

## Testing

### Run all tests
```bash
pytest
```

### Run with coverage
```bash
pytest --cov=src --cov-report=html
```

### Run specific test file
```bash
pytest tests/test_models.py
```

## API Examples

### 1. Create a Survey
```bash
curl -X POST http://localhost:5000/surveys \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Customer Satisfaction Survey",
    "description": "Annual feedback survey"
  }'
```

### 2. Add Questions
```bash
# Text Question
curl -X POST http://localhost:5000/surveys/{survey_id}/questions \
  -H "Content-Type: application/json" \
  -d '{
    "type": "text",
    "text": "What is your name?"
  }'

# Multiple Choice Question
curl -X POST http://localhost:5000/surveys/{survey_id}/questions \
  -H "Content-Type: application/json" \
  -d '{
    "type": "multiple_choice",
    "text": "How did you hear about us?",
    "options": ["Social Media", "Friend", "Advertisement", "Other"]
  }'

# Scale Question
curl -X POST http://localhost:5000/surveys/{survey_id}/questions \
  -H "Content-Type: application/json" \
  -d '{
    "type": "scale",
    "text": "How satisfied are you with our service?",
    "min_value": 1,
    "max_value": 5
  }'
```

### 3. Publish Survey
```bash
curl -X POST http://localhost:5000/surveys/{survey_id}/publish
```

### 4. Submit Response
```bash
curl -X POST http://localhost:5000/surveys/{survey_id}/responses \
  -H "Content-Type: application/json" \
  -d '{
    "responses": [
      {"question_id": "q1_id", "answer": "John Doe"},
      {"question_id": "q2_id", "answer": "Social Media"},
      {"question_id": "q3_id", "answer": 5}
    ]
  }'
```

### 5. View Results
```bash
curl http://localhost:5000/surveys/{survey_id}/results
```

### 6. Export to CSV
```bash
curl http://localhost:5000/surveys/{survey_id}/export > results.csv
```

## Development Workflow

### 1. Create a new branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make changes and test
```bash
# Run tests
pytest

# Check code style
flake8 src tests
black --check src tests

# Security scan
bandit -r src
```

### 3. Commit and push
```bash
git add .
git commit -m "Description of changes"
git push origin feature/your-feature-name
```

### 4. Create Pull Request
- Ensure CI passes
- Request code review
- Merge after approval

## Troubleshooting

### Port already in use
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>
```

### Tests failing
```bash
# Clear cache
pytest --cache-clear

# Verbose output
pytest -v -s
```

### Import errors
```bash
# Ensure you're in virtual environment
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [pytest Documentation](https://docs.pytest.org/)
- [REST API Best Practices](https://restfulapi.net/)
