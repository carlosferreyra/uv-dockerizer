"""uv-dockerizer: Generate optimized Docker configurations for uv-based Python projects."""

__version__ = "0.1.0"
__author__ = "Carlos Eduardo Ferreyra"

from uv_dockerizer.cli import app

__all__ = ["app", "__version__"]
