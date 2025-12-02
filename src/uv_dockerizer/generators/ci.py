"""CI/CD configuration generators."""

from pathlib import Path

from uv_dockerizer.models import ProjectInfo


class CIGenerator:
    """Generates CI/CD configuration files."""

    def __init__(self, project_info: ProjectInfo, provider: str = "github") -> None:
        """Initialize the generator.

        Args:
            project_info: Analyzed project information.
            provider: CI provider (github, gitlab).
        """
        self.project = project_info
        self.provider = provider.lower()

    def generate(self, output_path: Path, force: bool = False) -> None:
        """Generate CI configuration files.

        Args:
            output_path: Output directory.
            force: Overwrite existing files.
        """
        if self.provider == "github":
            self._generate_github_actions(output_path, force)
        elif self.provider == "gitlab":
            self._generate_gitlab_ci(output_path, force)

    def _generate_github_actions(self, output_path: Path, force: bool) -> None:
        """Generate GitHub Actions workflow."""
        workflow_dir = output_path / ".github" / "workflows"
        workflow_dir.mkdir(parents=True, exist_ok=True)

        workflow_path = workflow_dir / "docker.yml"
        if workflow_path.exists() and not force:
            return

        content = f'''name: Docker Build & Push

on:
  push:
    branches: [main, master]
    tags: ['v*']
  pull_request:
    branches: [main, master]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{{{ github.repository }}}}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          registry: ${{{{ env.REGISTRY }}}}
          username: ${{{{ github.actor }}}}
          password: ${{{{ secrets.GITHUB_TOKEN }}}}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{{{ env.REGISTRY }}}}/${{{{ env.IMAGE_NAME }}}}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{{{version}}}}
            type=semver,pattern={{{{major}}}}.{{{{minor}}}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{{{ github.event_name != 'pull_request' }}}}
          tags: ${{{{ steps.meta.outputs.tags }}}}
          labels: ${{{{ steps.meta.outputs.labels }}}}
          cache-from: type=gha
          cache-to: type=gha,mode=max
'''

        workflow_path.write_text(content)

    def _generate_gitlab_ci(self, output_path: Path, force: bool) -> None:
        """Generate GitLab CI configuration."""
        ci_path = output_path / ".gitlab-ci.yml"
        if ci_path.exists() and not force:
            return

        content = f'''stages:
  - build
  - test
  - deploy

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE

.docker-build:
  image: docker:24
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY

build:
  extends: .docker-build
  stage: build
  script:
    - docker build -t $DOCKER_IMAGE:$CI_COMMIT_SHA .
    - docker push $DOCKER_IMAGE:$CI_COMMIT_SHA
  rules:
    - if: $CI_COMMIT_BRANCH

build-release:
  extends: .docker-build
  stage: build
  script:
    - docker build -t $DOCKER_IMAGE:$CI_COMMIT_TAG -t $DOCKER_IMAGE:latest .
    - docker push $DOCKER_IMAGE:$CI_COMMIT_TAG
    - docker push $DOCKER_IMAGE:latest
  rules:
    - if: $CI_COMMIT_TAG

test:
  image: python:3.12
  stage: test
  before_script:
    - pip install uv
    - uv sync --dev
  script:
    - uv run pytest
  rules:
    - if: $CI_COMMIT_BRANCH
'''

        ci_path.write_text(content)
