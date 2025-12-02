<p align="center">
  <img src="https://raw.githubusercontent.com/carlosferreyra/uv-dockerizer/main/assets/logo.svg" alt="uv-dockerizer logo" width="200">
</p>

<h1 align="center">🐳 uv-dockerizer</h1>

<p align="center">
  <strong>Automatically generate optimized Dockerfiles, Docker Compose, and IaC templates for uv-based Python projects</strong>
</p>

<p align="center">
  <a href="https://github.com/carlosferreyra/uv-dockerizer/actions/workflows/ci.yml">
    <img src="https://github.com/carlosferreyra/uv-dockerizer/actions/workflows/ci.yml/badge.svg" alt="CI">
  </a>
  <a href="https://pypi.org/project/uv-dockerizer/">
    <img src="https://img.shields.io/pypi/v/uv-dockerizer?color=blue&logo=pypi&logoColor=white" alt="PyPI version">
  </a>
  <a href="https://pypi.org/project/uv-dockerizer/">
    <img src="https://img.shields.io/pypi/pyversions/uv-dockerizer?logo=python&logoColor=white" alt="Python versions">
  </a>
  <a href="https://github.com/carlosferreyra/uv-dockerizer/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/carlosferreyra/uv-dockerizer?color=blue" alt="License">
  </a>
  <a href="https://github.com/carlosferreyra/uv-dockerizer/stargazers">
    <img src="https://img.shields.io/github/stars/carlosferreyra/uv-dockerizer?style=social" alt="GitHub stars">
  </a>
</p>

<p align="center">
  <a href="https://github.com/carlosferreyra/uv-dockerizer">
    <img src="https://img.shields.io/github/forks/carlosferreyra/uv-dockerizer?style=social" alt="GitHub forks">
  </a>
  <a href="https://github.com/carlosferreyra/uv-dockerizer/issues">
    <img src="https://img.shields.io/github/issues/carlosferreyra/uv-dockerizer" alt="GitHub issues">
  </a>
  <a href="https://github.com/carlosferreyra/uv-dockerizer/pulls">
    <img src="https://img.shields.io/github/issues-pr/carlosferreyra/uv-dockerizer" alt="GitHub pull requests">
  </a>
  <a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/badge/uv-powered-blueviolet?logo=astral" alt="uv powered">
  </a>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-supported-frameworks">Frameworks</a> •
  <a href="#-contributing">Contributing</a>
</p>

---

## 🎯 Why uv-dockerizer?

Building Docker images for Python projects can be tedious and error-prone. **uv-dockerizer** analyzes your project and generates production-ready Docker configurations with:

- ⚡ **Multi-stage builds** for minimal image sizes
- 🔒 **Security best practices** out of the box
- 🎯 **Framework-specific optimizations** (FastAPI, Django, Flask, etc.)
- 🚀 **CI/CD pipelines** ready to use
- ☁️ **Infrastructure as Code** templates for cloud deployment

Stop writing boilerplate Docker configurations. Let uv-dockerizer do it for you!

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Smart Detection** | Automatically analyzes your Python project to detect frameworks, dependencies, and optimal configurations |
| 🏗️ **Multi-stage Builds** | Generates optimized Dockerfiles with multi-stage builds for minimal image sizes (up to 80% smaller) |
| 🔒 **Security First** | Non-root user, health checks, minimal base images, and security best practices |
| 📦 **Docker Compose** | Optional Docker Compose generation with service dependencies |
| 🚀 **CI/CD Ready** | GitHub Actions and GitLab CI templates for automated builds and deployments |
| ☁️ **Infrastructure as Code** | Terraform and Pulumi templates for AWS, GCP, and Azure deployment |
| ⚡ **uv Powered** | Built for the modern Python ecosystem with [uv](https://github.com/astral-sh/uv) support |

---

## 📦 Installation

### Using uv (Recommended)

```bash
# Install as a tool
uv tool install uv-dockerizer

# Or run directly without installation
uvx uv-dockerizer
```

### Using pip

```bash
pip install uv-dockerizer
```

### Using pipx

```bash
pipx install uv-dockerizer
```

### From Source

```bash
git clone https://github.com/carlosferreyra/uv-dockerizer.git
cd uv-dockerizer
uv sync
```

---

## 🚀 Quick Start

```bash
# Navigate to your uv-based Python project
cd my-python-project

# Generate Docker configuration (analyzes project automatically)
uvx uv-dockerizer init

# Or with all the bells and whistles
uvx uv-dockerizer init --compose --ci github --iac terraform
```

That's it! You now have a production-ready Docker setup. 🎉

---

## 📖 Usage

### Show Help

```bash
uv-dockerizer              # Shows help by default
uv-dockerizer --help       # Explicit help
uv-dockerizer --version    # Show version
```

### Initialize Docker Configuration

The \`init\` command analyzes your project and generates optimized Docker files:

```bash
# Basic usage - generates Dockerfile and .dockerignore
uv-dockerizer init

# Generate with Docker Compose
uv-dockerizer init --compose

# Generate with CI/CD configuration
uv-dockerizer init --ci github      # GitHub Actions
uv-dockerizer init --ci gitlab      # GitLab CI

# Generate with Infrastructure as Code
uv-dockerizer init --iac terraform  # Terraform templates
uv-dockerizer init --iac pulumi     # Pulumi templates

# Full generation with all options
uv-dockerizer init \\
  --compose \\
  --ci github \\
  --iac terraform \\
  --base-image python:3.12-slim

# Overwrite existing files
uv-dockerizer init --force
```

### Analyze Project

Inspect your project without generating files:

```bash
uv-dockerizer analyze

# Example output:
# Project Name: my-awesome-api
# Python Version: 3.12
# Project Type: api
# Has uv.lock: True
# Detected Frameworks:
#   • fastapi
#   • pydantic
# Recommended Optimizations:
#   ✓ Multi-stage build for smaller images
#   ✓ Use uvicorn with multiple workers
```

### Build Docker Image

Build your Docker image directly:

```bash
# Build with auto-detected name
uv-dockerizer build

# Build with custom tag
uv-dockerizer build --tag v1.0.0

# Build and push to registry
uv-dockerizer build --tag v1.0.0 --push
```

---

## 🔍 Supported Frameworks

uv-dockerizer automatically detects and optimizes for popular Python frameworks:

| Framework | Detection | Default Port | Optimizations |
|-----------|:---------:|:------------:|---------------|
| **FastAPI** | ✅ | 8000 | Uvicorn with workers, async-ready |
| **Flask** | ✅ | 5000 | Gunicorn configuration |
| **Django** | ✅ | 8000 | Static files, migrations, Gunicorn |
| **Streamlit** | ✅ | 8501 | Browser configuration, server settings |
| **Celery** | ✅ | - | Redis broker, worker setup |
| **Typer/Click** | ✅ | - | CLI entrypoint optimization |
| **Data Science** | ✅ | - | NumPy, Pandas, PyTorch optimizations |

---

## 📁 Generated Files

```
my-project/
├── 📄 Dockerfile              # Optimized multi-stage Dockerfile
├── 📄 .dockerignore           # Docker ignore patterns
├── 📄 docker-compose.yml      # Docker Compose (with --compose)
├── 📁 .github/
│   └── 📁 workflows/
│       └── 📄 docker.yml      # GitHub Actions (with --ci github)
└── 📁 infrastructure/
    ├── 📁 terraform/          # Terraform templates (with --iac terraform)
    │   ├── 📄 main.tf
    │   ├── 📄 variables.tf
    │   └── 📄 outputs.tf
    └── 📁 pulumi/             # Pulumi templates (with --iac pulumi)
        ├── 📄 Pulumi.yaml
        ├── 📄 __main__.py
        └── 📄 requirements.txt
```

---

## 🐳 Example Generated Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
# Generated by uv-dockerizer v0.1.0

# ============================================
# Builder stage - Install dependencies
# ============================================
FROM python:3.12-slim AS builder

# Install uv for fast dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Optimize for reproducible builds
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install dependencies first (better layer caching)
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \\
    uv sync --frozen --no-install-project --no-dev

# Install the project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \\
    uv sync --frozen --no-dev

# ============================================
# Runtime stage - Minimal production image
# ============================================
FROM python:3.12-slim AS runtime

# Create non-root user for security
RUN groupadd --gid 1000 appgroup && \\
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

WORKDIR /app

# Copy virtual environment and application
COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appgroup /app /app

# Configure environment
ENV PATH="/app/.venv/bin:\$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose port and set user
EXPOSE 8000
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the application
CMD ["uvicorn", "myapp.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🔧 Configuration

### CLI Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| \`--output\` | \`-o\` | Output directory for generated files | \`.\` |
| \`--base-image\` | \`-b\` | Base Docker image | \`auto\` |
| \`--compose\` | \`-c\` | Generate Docker Compose file | \`false\` |
| \`--ci\` | | CI/CD provider (\`github\`, \`gitlab\`) | \`none\` |
| \`--iac\` | | IaC provider (\`terraform\`, \`pulumi\`) | \`none\` |
| \`--force\` | \`-f\` | Overwrite existing files | \`false\` |

### Environment Variables

| Variable | Description |
|----------|-------------|
| \`UV_DOCKERIZER_BASE_IMAGE\` | Default base image |
| \`UV_DOCKERIZER_OUTPUT\` | Default output directory |

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/carlosferreyra/uv-dockerizer.git
cd uv-dockerizer

# Install dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Run linting
uv run ruff check .
uv run ruff format --check .

# Run type checking
uv run mypy src
```

### Code Quality

This project uses:
- **[Ruff](https://github.com/astral-sh/ruff)** - Fast Python linter and formatter
- **[mypy](https://mypy.readthedocs.io/)** - Static type checking
- **[pytest](https://pytest.org/)** - Testing framework
- **[pre-commit](https://pre-commit.com/)** - Git hooks for code quality

---

## 📊 Roadmap

- [x] Basic Dockerfile generation
- [x] Multi-stage build optimization
- [x] Framework detection
- [x] Docker Compose support
- [x] GitHub Actions CI/CD
- [ ] GitLab CI/CD templates
- [ ] Terraform AWS deployment
- [ ] Pulumi support
- [ ] Kubernetes manifests
- [ ] Azure Container Apps
- [ ] Google Cloud Run
- [ ] Devcontainer support

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with love using these amazing tools:

- **[uv](https://github.com/astral-sh/uv)** - An extremely fast Python package and project manager
- **[Typer](https://typer.tiangolo.com/)** - Build great CLIs with Python
- **[Rich](https://rich.readthedocs.io/)** - Rich text and beautiful formatting in the terminal
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation using Python type annotations

---

## ⭐ Star History

<p align="center">
  <a href="https://star-history.com/#carlosferreyra/uv-dockerizer&Date">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=carlosferreyra/uv-dockerizer&type=Date&theme=dark" />
      <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=carlosferreyra/uv-dockerizer&type=Date" />
      <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=carlosferreyra/uv-dockerizer&type=Date" />
    </picture>
  </a>
</p>

---

<p align="center">
  <sub>Made with ❤️ by <a href="https://github.com/carlosferreyra">Carlos Eduardo Ferreyra</a></sub>
</p>

<p align="center">
  <a href="https://github.com/carlosferreyra/uv-dockerizer">
    <img src="https://img.shields.io/badge/⭐_Star_this_repo-yellow?style=for-the-badge" alt="Star this repo">
  </a>
</p>
