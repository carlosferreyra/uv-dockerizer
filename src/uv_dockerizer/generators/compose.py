"""Docker Compose generator."""

import yaml

from uv_dockerizer.models import Framework, ProjectInfo


class ComposeGenerator:
    """Generates Docker Compose files for projects."""

    def __init__(self, project_info: ProjectInfo) -> None:
        """Initialize the generator.

        Args:
            project_info: Analyzed project information.
        """
        self.project = project_info

    def generate(self) -> str:
        """Generate docker-compose.yml content.

        Returns:
            Docker Compose YAML content.
        """
        compose = {
            "services": self._generate_services(),
        }

        # Add volumes if needed
        volumes = self._generate_volumes()
        if volumes:
            compose["volumes"] = volumes

        # Add networks
        compose["networks"] = {
            "default": {
                "name": f"{self.project.name}-network",
            }
        }

        return yaml.dump(compose, default_flow_style=False, sort_keys=False)

    def _generate_services(self) -> dict:
        """Generate services configuration."""
        services = {}

        # Main application service
        app_service = {
            "build": {
                "context": ".",
                "dockerfile": "Dockerfile",
            },
            "container_name": self.project.name,
            "restart": "unless-stopped",
        }

        # Add ports
        if self.project.exposed_ports:
            app_service["ports"] = [f"{p}:{p}" for p in self.project.exposed_ports]

        # Add environment variables
        app_service["environment"] = {
            "PYTHONUNBUFFERED": "1",
        }

        # Add volumes for development
        app_service["volumes"] = [
            "./src:/app/src:ro",
        ]

        services["app"] = app_service

        # Add additional services based on frameworks
        frameworks = set(self.project.frameworks)

        # Add Redis for Celery
        if Framework.CELERY in frameworks:
            services["redis"] = {
                "image": "redis:7-alpine",
                "container_name": f"{self.project.name}-redis",
                "ports": ["6379:6379"],
                "volumes": ["redis-data:/data"],
            }
            services["app"]["depends_on"] = ["redis"]
            services["app"]["environment"]["REDIS_URL"] = "redis://redis:6379/0"

            # Add Celery worker
            services["worker"] = {
                "build": {
                    "context": ".",
                    "dockerfile": "Dockerfile",
                },
                "container_name": f"{self.project.name}-worker",
                "command": ["celery", "-A", self.project.name.replace("-", "_"), "worker", "--loglevel=info"],
                "depends_on": ["redis"],
                "environment": {
                    "REDIS_URL": "redis://redis:6379/0",
                },
            }

        # Add database services based on common patterns
        # This is a placeholder - could be enhanced with project analysis

        return services

    def _generate_volumes(self) -> dict:
        """Generate volumes configuration."""
        volumes = {}
        frameworks = set(self.project.frameworks)

        if Framework.CELERY in frameworks:
            volumes["redis-data"] = {}

        return volumes
