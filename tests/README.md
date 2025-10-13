# Running Tests

This directory contains tests for the cvasl-gui application.

## Setup

Install test dependencies:

```bash
poetry install --with dev
```

## Running Tests

Run all tests:

```bash
poetry run pytest
```

Run tests with verbose output:

```bash
poetry run pytest -v
```

Run tests with coverage report:

```bash
poetry run pytest --cov=src/cvasl_gui --cov-report=html
```

Run specific test file:

```bash
poetry run pytest tests/test_app.py
```

Run specific test:

```bash
poetry run pytest tests/test_app.py::test_app_imports
```

## Test Coverage

After running tests with coverage, view the HTML report:

```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Test Structure

- `test_app.py` - Basic application tests (imports, structure, configuration)
- `conftest.py` - Shared fixtures and configuration
- `pytest.ini` - Pytest configuration

## Writing Tests

When adding new tests:

1. Create test files with the prefix `test_`
2. Name test functions with the prefix `test_`
3. Use fixtures from `conftest.py` for common setup
4. Follow the existing test patterns

Example:

```python
def test_my_feature(dash_app):
    """Test description"""
    # Arrange
    expected = "some value"
    
    # Act
    result = dash_app.some_method()
    
    # Assert
    assert result == expected
```
