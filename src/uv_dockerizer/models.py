"""Data models for uv-dockerizer."""

from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class ProjectType(str, Enum):
    """Type of Python project."""

    APP = "app"
    LIB = "lib"
    API = "api"
    WORKER = "worker"
    CLI = "cli"
    UNKNOWN = "unknown"


class BaseImage(str, Enum):
    """Supported base Docker images."""

    SLIM = "python:{version}-slim"
    ALPINE = "python:{version}-alpine"
    BOOKWORM = "python:{version}-bookworm"
    DISTROLESS = "gcr.io/distroless/python3-debian12"


class Framework(str, Enum):
    """Detected frameworks."""

    FASTAPI = "fastapi"
    FLASK = "flask"
    DJANGO = "django"
    STREAMLIT = "streamlit"
    CELERY = "celery"
    TYPER = "typer"
    CLICK = "click"
    PANDAS = "pandas"
    NUMPY = "numpy"
    PYTORCH = "pytorch"
    TENSORFLOW = "tensorflow"


class ProjectInfo(BaseModel):
    """Information about the analyzed project."""

    name: str = Field(description="Project name")
    version: str = Field(default="0.1.0", description="Project version")
    python_version: str = Field(default="3.12", description="Python version")
    project_type: ProjectType = Field(default=ProjectType.UNKNOWN, description="Type of project")
    path: Path = Field(description="Project path")

    # Dependencies
    dependencies: list[str] = Field(default_factory=list, description="Project dependencies")
    dev_dependencies: list[str] = Field(default_factory=list, description="Dev dependencies")

    # Detection results
    has_uv_lock: bool = Field(default=False, description="Has uv.lock file")
    has_pyproject: bool = Field(default=False, description="Has pyproject.toml")
    has_requirements: bool = Field(default=False, description="Has requirements.txt")
    frameworks: list[Framework] = Field(default_factory=list, description="Detected frameworks")

    # Entry points
    entry_point: Optional[str] = Field(default=None, description="Main entry point")
    scripts: dict[str, str] = Field(default_factory=dict, description="Project scripts")

    # Optimizations
    recommended_optimizations: list[str] = Field(
        default_factory=list, description="Recommended optimizations"
    )
    recommended_base_image: str = Field(
        default="python:3.12-slim", description="Recommended base image"
    )

    # Build configuration
    build_args: dict[str, str] = Field(default_factory=dict, description="Build arguments")
    env_vars: dict[str, str] = Field(default_factory=dict, description="Environment variables")
    exposed_ports: list[int] = Field(default_factory=list, description="Ports to expose")


class DockerConfig(BaseModel):
    """Docker configuration options."""

    base_image: str = Field(default="python:3.12-slim", description="Base Docker image")
    multi_stage: bool = Field(default=True, description="Use multi-stage build")
    use_uv: bool = Field(default=True, description="Use uv for package installation")
    non_root_user: bool = Field(default=True, description="Run as non-root user")
    healthcheck: bool = Field(default=True, description="Include healthcheck")
    labels: dict[str, str] = Field(default_factory=dict, description="Docker labels")


class ComposeConfig(BaseModel):
    """Docker Compose configuration."""

    version: str = Field(default="3.9", description="Compose file version")
    services: dict = Field(default_factory=dict, description="Services configuration")
    volumes: dict = Field(default_factory=dict, description="Volumes configuration")
    networks: dict = Field(default_factory=dict, description="Networks configuration")
