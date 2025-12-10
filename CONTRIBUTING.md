# Contributing Guidelines

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Create a branch: `git checkout -b feature/your-feature`
4. Set up development environment (see QUICKSTART.md)

## Code Standards

### Python Style Guide
- Follow PEP 8
- Use meaningful variable and function names
- Maximum line length: 127 characters
- Use type hints where applicable

### Code Quality Checks
Before committing, ensure:
```bash
# Format code
black src tests

# Check linting
flake8 src tests

# Security check
bandit -r src

# Run tests
pytest
```

### Documentation
- All public functions must have docstrings
- Use Google-style docstrings
- Update README.md if adding new features

Example docstring:
```python
def create_survey(title: str, description: str = "") -> Survey:
    """
    Create a new survey.
    
    Args:
        title: The survey title
        description: Optional survey description
        
    Returns:
        Survey: The created survey object
        
    Raises:
        ValueError: If title is empty
    """
    pass
```

## Testing

### Writing Tests
- Test file naming: `test_<module>.py`
- Test class naming: `Test<Feature>`
- Test function naming: `test_<what_it_does>`
- Aim for >= 80% code coverage

### Test Structure
```python
def test_feature_name():
    # Arrange
    setup_data()
    
    # Act
    result = perform_action()
    
    # Assert
    assert result == expected
```

## Git Workflow

### Commit Messages
Format: `<type>: <subject>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `style`: Formatting changes
- `chore`: Maintenance

Examples:
```
feat: add export to PDF functionality
fix: resolve validation error for scale questions
docs: update API documentation
test: add tests for survey publishing
```

### Pull Request Process

1. **Update your branch**
   ```bash
   git checkout main
   git pull origin main
   git checkout feature/your-feature
   git rebase main
   ```

2. **Create PR**
   - Write clear title and description
   - Reference related issues (#123)
   - Ensure CI passes
   - Request review from team members

3. **PR Checklist**
   - [ ] Code follows style guidelines
   - [ ] Tests added/updated
   - [ ] Documentation updated
   - [ ] All tests pass
   - [ ] No merge conflicts
   - [ ] Code review approved

## Code Review Guidelines

### For Authors
- Keep PRs focused and small
- Respond to feedback promptly
- Be open to suggestions

### For Reviewers
- Review within 24 hours
- Be constructive and specific
- Test the changes locally
- Approve only if DoD is met

## Definition of Ready (DoR)

Before starting work:
- [ ] Story has clear description
- [ ] Acceptance criteria defined
- [ ] Story points estimated
- [ ] No blocking dependencies

## Definition of Done (DoD)

Before marking as complete:
- [ ] Code written and tested
- [ ] Code coverage >= 80%
- [ ] All tests pass
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] No linting errors
- [ ] Security scan clean
- [ ] Merged to main

## Common Tasks

### Adding a New Endpoint
1. Add route in `src/app.py`
2. Add business logic in appropriate module
3. Write tests in `tests/test_app.py`
4. Update API documentation
5. Test manually with curl/Postman

### Adding a New Question Type
1. Create class in `src/models.py`
2. Update `_create_question()` in `src/storage.py`
3. Update `_restore_question()` in `src/storage.py`
4. Write tests in `tests/test_models.py`
5. Update documentation

## Getting Help

- Create an issue for bugs or features
- Ask in team chat for quick questions
- Tag relevant team members in PRs
- Check existing issues and PRs first

## License

By contributing, you agree that your contributions will be licensed under the project license.
