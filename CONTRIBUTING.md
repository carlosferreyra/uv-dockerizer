# Contributing to uv-dockerizer

First off, thank you for considering contributing to uv-dockerizer! 🎉

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Code Style](#code-style)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Release Process](#release-process)

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code.
Please report unacceptable behavior to the maintainers.

## Getting Started

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Git
- Docker (for testing generated files)

### Development Setup

1. **Fork and clone the repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/uv-dockerizer.git
   cd uv-dockerizer
   ```

2. **Install dependencies**

   ```bash
   uv sync --all-extras
   ```

3. **Install pre-commit hooks**

   ```bash
   uv run pre-commit install
   ```

4. **Verify your setup**

   ```bash
   uv run pytest
   uv run uv-dockerizer --version
   ```

## Making Changes

### Branch Naming

- `feature/` - New features (e.g., `feature/kubernetes-support`)
- `fix/` - Bug fixes (e.g., `fix/dockerfile-path-issue`)
- `docs/` - Documentation updates (e.g., `docs/update-readme`)
- `refactor/` - Code refactoring (e.g., `refactor/analyzer-module`)

### Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (no code change)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**

```bash
feat(dockerfile): add support for Alpine base images
fix(analyzer): handle missing pyproject.toml gracefully
docs(readme): update installation instructions
```

## Code Style

This project uses strict code quality tools:

### Linting and Formatting

```bash
# Check linting
uv run ruff check .

# Auto-fix linting issues
uv run ruff check --fix .

# Check formatting
uv run ruff format --check .

# Apply formatting
uv run ruff format .
```

### Type Checking

```bash
uv run mypy src
```

### Pre-commit Hooks

All checks run automatically on commit:

```bash
# Run manually on all files
uv run pre-commit run --all-files
```

### Code Guidelines

- Use type hints for all function signatures
- Write docstrings for all public functions and classes
- Keep functions focused and small
- Use meaningful variable names
- Add comments for complex logic

## Testing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/uv_dockerizer --cov-report=html

# Run specific test file
uv run pytest tests/test_analyzer.py

# Run tests matching a pattern
uv run pytest -k "test_dockerfile"

# Run with verbose output
uv run pytest -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files as `test_*.py`
- Name test functions as `test_*`
- Use fixtures for common setup
- Aim for high coverage on critical paths

```python
# Example test
import pytest
from uv_dockerizer.analyzers.project import ProjectAnalyzer

def test_analyzer_detects_fastapi(tmp_path):
    """Test that FastAPI framework is detected from dependencies."""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""
[project]
name = "test-project"
dependencies = ["fastapi>=0.100.0"]
""")

    analyzer = ProjectAnalyzer(tmp_path)
    info = analyzer.analyze()

    assert "fastapi" in [f.value for f in info.frameworks]
```

## Submitting Changes

### Pull Request Process

1. **Update your fork**

   ```bash
   git checkout main
   git pull upstream main
   ```

2. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature
   ```

3. **Make your changes**

   - Write code
   - Add tests
   - Update documentation

4. **Run quality checks**

   ```bash
   uv run ruff check .
   uv run ruff format .
   uv run mypy src
   uv run pytest
   ```

5. **Commit and push**

   ```bash
   git add .
   git commit -m "feat: add your feature"
   git push origin feature/your-feature
   ```

6. **Open a Pull Request**

   - Fill out the PR template
   - Link related issues
   - Request reviews

### PR Requirements

- [ ] All CI checks pass
- [ ] Tests added for new functionality
- [ ] Documentation updated if needed
- [ ] No merge conflicts
- [ ] Approved by at least one maintainer

## Release Process

Releases are automated via GitHub Actions:

1. Update version in `pyproject.toml` and `src/uv_dockerizer/__init__.py`
2. Create and push a tag:

   ```bash
   git tag -a v0.2.0 -m "Release v0.2.0"
   git push origin v0.2.0
   ```

3. GitHub Actions will:
   - Run all tests
   - Build the package
   - Publish to PyPI
   - Create a GitHub Release

## Questions?

- Open an [issue](https://github.com/carlosferreyra/uv-dockerizer/issues) for bugs or features
- Start a [discussion](https://github.com/carlosferreyra/uv-dockerizer/discussions) for questions

Thank you for contributing! 🚀
