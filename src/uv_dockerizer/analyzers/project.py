"""Project analyzer to detect project configuration and dependencies."""

import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from uv_dockerizer.models import Framework, ProjectInfo, ProjectType


class ProjectAnalyzer:
    """Analyzes a Python project to extract configuration for Docker generation."""

    # Framework detection patterns
    FRAMEWORK_PATTERNS: dict[str, Framework] = {
        "fastapi": Framework.FASTAPI,
        "flask": Framework.FLASK,
        "django": Framework.DJANGO,
        "streamlit": Framework.STREAMLIT,
        "celery": Framework.CELERY,
        "typer": Framework.TYPER,
        "click": Framework.CLICK,
        "pandas": Framework.PANDAS,
        "numpy": Framework.NUMPY,
        "torch": Framework.PYTORCH,
        "tensorflow": Framework.TENSORFLOW,
    }

    # Default ports for frameworks
    FRAMEWORK_PORTS: dict[Framework, int] = {
        Framework.FASTAPI: 8000,
        Framework.FLASK: 5000,
        Framework.DJANGO: 8000,
        Framework.STREAMLIT: 8501,
    }

    def __init__(self, path: Path) -> None:
        """Initialize the analyzer with a project path.

        Args:
            path: Path to the project root directory.
        """
        self.path = Path(path).resolve()
        self.pyproject_path = self.path / "pyproject.toml"
        self.uv_lock_path = self.path / "uv.lock"
        self.requirements_path = self.path / "requirements.txt"
        self.python_version_path = self.path / ".python-version"

    def analyze(self) -> ProjectInfo:
        """Analyze the project and return project information.

        Returns:
            ProjectInfo with detected configuration.
        """
        # Start with basic info
        info = ProjectInfo(
            name=self.path.name,
            path=self.path,
            has_uv_lock=self.uv_lock_path.exists(),
            has_pyproject=self.pyproject_path.exists(),
            has_requirements=self.requirements_path.exists(),
        )

        # Parse pyproject.toml if exists
        if info.has_pyproject:
            self._parse_pyproject(info)

        # Detect Python version
        info.python_version = self._detect_python_version()

        # Detect frameworks from dependencies
        info.frameworks = self._detect_frameworks(info.dependencies)

        # Detect project type
        info.project_type = self._detect_project_type(info)

        # Determine recommended base image
        info.recommended_base_image = self._recommend_base_image(info)

        # Detect ports to expose
        info.exposed_ports = self._detect_ports(info)

        # Generate optimization recommendations
        info.recommended_optimizations = self._generate_optimizations(info)

        return info

    def _parse_pyproject(self, info: ProjectInfo) -> None:
        """Parse pyproject.toml and extract relevant information.

        Args:
            info: ProjectInfo to populate.
        """
        with open(self.pyproject_path, "rb") as f:
            data = tomllib.load(f)

        project = data.get("project", {})

        # Basic info
        info.name = project.get("name", info.name)
        info.version = project.get("version", info.version)

        # Python version from requires-python
        requires_python = project.get("requires-python", "")
        if requires_python:
            # Extract version like ">=3.12" -> "3.12"
            version = requires_python.replace(">=", "").replace("==", "").replace("~=", "")
            version = version.split(",")[0].strip()
            if version:
                info.python_version = version

        # Dependencies
        info.dependencies = project.get("dependencies", [])

        # Optional dependencies (dev)
        optional_deps = project.get("optional-dependencies", {})
        info.dev_dependencies = optional_deps.get("dev", [])

        # Scripts/entry points
        info.scripts = project.get("scripts", {})
        if info.scripts:
            # First script is likely the main entry point
            info.entry_point = list(info.scripts.keys())[0]

    def _detect_python_version(self) -> str:
        """Detect Python version from .python-version file or pyproject.toml.

        Returns:
            Python version string.
        """
        if self.python_version_path.exists():
            version = self.python_version_path.read_text().strip()
            # Handle versions like "3.12.1" -> "3.12"
            parts = version.split(".")
            if len(parts) >= 2:
                return f"{parts[0]}.{parts[1]}"
            return version
        return "3.12"  # Default

    def _detect_frameworks(self, dependencies: list[str]) -> list[Framework]:
        """Detect frameworks from dependencies.

        Args:
            dependencies: List of project dependencies.

        Returns:
            List of detected frameworks.
        """
        frameworks = []
        dep_names = {self._extract_package_name(dep).lower() for dep in dependencies}

        for pattern, framework in self.FRAMEWORK_PATTERNS.items():
            if pattern in dep_names:
                frameworks.append(framework)

        return frameworks

    def _extract_package_name(self, dependency: str) -> str:
        """Extract package name from dependency string.

        Args:
            dependency: Dependency string like "fastapi>=0.100.0".

        Returns:
            Package name.
        """
        # Handle various formats: "pkg", "pkg>=1.0", "pkg[extra]>=1.0"
        name = dependency.split(">=")[0].split("<=")[0].split("==")[0].split("~=")[0]
        name = name.split("[")[0]
        return name.strip()

    def _detect_project_type(self, info: ProjectInfo) -> ProjectType:
        """Detect project type from frameworks and structure.

        Args:
            info: ProjectInfo with detected frameworks.

        Returns:
            Detected ProjectType.
        """
        frameworks = set(info.frameworks)

        # API projects
        if Framework.FASTAPI in frameworks or Framework.FLASK in frameworks:
            return ProjectType.API

        if Framework.DJANGO in frameworks:
            return ProjectType.APP

        # Worker/task projects
        if Framework.CELERY in frameworks:
            return ProjectType.WORKER

        # CLI projects
        if Framework.TYPER in frameworks or Framework.CLICK in frameworks:
            return ProjectType.CLI

        # Check for scripts
        if info.scripts:
            return ProjectType.CLI

        # Check for src layout
        if (self.path / "src").exists():
            return ProjectType.LIB

        return ProjectType.UNKNOWN

    def _recommend_base_image(self, info: ProjectInfo) -> str:
        """Recommend the best base image for the project.

        Args:
            info: ProjectInfo with detected configuration.

        Returns:
            Recommended base image string.
        """
        version = info.python_version
        frameworks = set(info.frameworks)

        # Data science / ML projects need more libraries
        if frameworks & {Framework.PANDAS, Framework.NUMPY, Framework.PYTORCH, Framework.TENSORFLOW}:
            return f"python:{version}-bookworm"

        # Default to slim for most projects
        return f"python:{version}-slim"

    def _detect_ports(self, info: ProjectInfo) -> list[int]:
        """Detect ports to expose based on frameworks.

        Args:
            info: ProjectInfo with detected frameworks.

        Returns:
            List of ports to expose.
        """
        ports = []
        for framework in info.frameworks:
            if framework in self.FRAMEWORK_PORTS:
                ports.append(self.FRAMEWORK_PORTS[framework])
        return list(set(ports))  # Remove duplicates

    def _generate_optimizations(self, info: ProjectInfo) -> list[str]:
        """Generate optimization recommendations.

        Args:
            info: ProjectInfo with detected configuration.

        Returns:
            List of optimization recommendations.
        """
        optimizations = []

        if info.has_uv_lock:
            optimizations.append("Use uv.lock for reproducible builds")
        else:
            optimizations.append("Consider creating uv.lock for reproducible builds")

        optimizations.append("Multi-stage build to reduce final image size")
        optimizations.append("Non-root user for security")
        optimizations.append("Leverage Docker layer caching for dependencies")

        if info.project_type == ProjectType.API:
            optimizations.append("Add healthcheck endpoint")

        frameworks = set(info.frameworks)
        if frameworks & {Framework.PANDAS, Framework.NUMPY}:
            optimizations.append("Consider using slim base with pre-compiled wheels")

        return optimizations
