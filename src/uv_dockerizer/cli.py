"""CLI interface for uv-dockerizer."""

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel

from uv_dockerizer import __version__

app = typer.Typer(
    name="uv-dockerizer",
    help="🐳 Generate optimized Docker configurations for uv-based Python projects.",
    add_completion=True,
    rich_markup_mode="rich",
)
console = Console()


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        console.print(f"[bold blue]uv-dockerizer[/bold blue] version [green]{__version__}[/green]")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            "-V",
            help="Show version and exit.",
            callback=version_callback,
            is_eager=True,
        ),
    ] = None,
) -> None:
    """🐳 uv-dockerizer: Automatically generate optimized Docker configurations for uv-based Python projects."""
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())


@app.command()
def init(
    path: Annotated[
        Path,
        typer.Argument(
            help="Path to the Python project (defaults to current directory).",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
        ),
    ] = Path("."),
    output: Annotated[
        Path,
        typer.Option(
            "--output",
            "-o",
            help="Output directory for generated files.",
        ),
    ] = Path("."),
    base_image: Annotated[
        str,
        typer.Option(
            "--base-image",
            "-b",
            help="Base Docker image to use (e.g., python:3.12-slim, python:3.12-alpine).",
        ),
    ] = "auto",
    compose: Annotated[
        bool,
        typer.Option(
            "--compose",
            "-c",
            help="Generate Docker Compose file.",
        ),
    ] = False,
    ci: Annotated[
        str | None,
        typer.Option(
            "--ci",
            help="Generate CI/CD configuration (github, gitlab, none).",
        ),
    ] = None,
    iac: Annotated[
        str | None,
        typer.Option(
            "--iac",
            help="Generate Infrastructure as Code templates (terraform, pulumi, none).",
        ),
    ] = None,
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            "-f",
            help="Overwrite existing files.",
        ),
    ] = False,
) -> None:
    """🚀 Initialize Docker configuration for a uv-based Python project.

    Analyzes your project and generates optimized:
    - Dockerfile with multi-stage builds
    - .dockerignore
    - Docker Compose (optional)
    - CI/CD pipelines (optional)
    - IaC templates (optional)
    """
    from uv_dockerizer.analyzers.project import ProjectAnalyzer
    from uv_dockerizer.generators.dockerfile import DockerfileGenerator

    console.print(
        Panel(
            f"[bold]Analyzing project at[/bold] [cyan]{path}[/cyan]",
            title="🔍 uv-dockerizer",
            border_style="blue",
        )
    )

    # Analyze project
    analyzer = ProjectAnalyzer(path)
    project_info = analyzer.analyze()

    console.print(f"\n[green]✓[/green] Detected project: [bold]{project_info.name}[/bold]")
    console.print(f"[green]✓[/green] Python version: [bold]{project_info.python_version}[/bold]")
    console.print(f"[green]✓[/green] Project type: [bold]{project_info.project_type}[/bold]")
    console.print(f"[green]✓[/green] Dependencies: [bold]{len(project_info.dependencies)}[/bold]")

    # Generate Dockerfile
    generator = DockerfileGenerator(project_info, base_image=base_image)
    dockerfile_content = generator.generate()

    output_path = output / "Dockerfile"
    if output_path.exists() and not force:
        console.print(
            "\n[yellow]⚠[/yellow] Dockerfile already exists. Use [bold]--force[/bold] to overwrite."
        )
        raise typer.Exit(1)

    output_path.write_text(dockerfile_content)
    console.print("\n[green]✓[/green] Generated [bold]Dockerfile[/bold]")

    # Generate .dockerignore
    dockerignore_path = output / ".dockerignore"
    if not dockerignore_path.exists() or force:
        dockerignore_content = generator.generate_dockerignore()
        dockerignore_path.write_text(dockerignore_content)
        console.print("[green]✓[/green] Generated [bold].dockerignore[/bold]")

    # Generate Docker Compose if requested
    if compose:
        from uv_dockerizer.generators.compose import ComposeGenerator

        compose_gen = ComposeGenerator(project_info)
        compose_content = compose_gen.generate()
        compose_path = output / "docker-compose.yml"
        if not compose_path.exists() or force:
            compose_path.write_text(compose_content)
            console.print("[green]✓[/green] Generated [bold]docker-compose.yml[/bold]")

    # Generate CI/CD if requested
    if ci:
        from uv_dockerizer.generators.ci import CIGenerator

        ci_gen = CIGenerator(project_info, provider=ci)
        ci_gen.generate(output, force=force)
        console.print(f"[green]✓[/green] Generated [bold]{ci}[/bold] CI/CD configuration")

    # Generate IaC if requested
    if iac:
        from uv_dockerizer.iac import IaCGenerator

        iac_gen = IaCGenerator(project_info, provider=iac)
        iac_gen.generate(output, force=force)
        console.print(f"[green]✓[/green] Generated [bold]{iac}[/bold] IaC templates")

    console.print(
        Panel(
            "[green]✨ Docker configuration generated successfully![/green]\n\n"
            "Next steps:\n"
            "  1. Review the generated files\n"
            "  2. Build: [bold]docker build -t myapp .[/bold]\n"
            "  3. Run: [bold]docker run myapp[/bold]",
            title="🎉 Done",
            border_style="green",
        )
    )


@app.command()
def analyze(
    path: Annotated[
        Path,
        typer.Argument(
            help="Path to the Python project.",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
        ),
    ] = Path("."),
) -> None:
    """🔍 Analyze a Python project and show detected configuration."""
    from uv_dockerizer.analyzers.project import ProjectAnalyzer

    console.print(
        Panel(
            f"[bold]Analyzing project at[/bold] [cyan]{path}[/cyan]",
            title="🔍 Project Analysis",
            border_style="blue",
        )
    )

    analyzer = ProjectAnalyzer(path)
    project_info = analyzer.analyze()

    console.print(f"\n[bold]Project Name:[/bold] {project_info.name}")
    console.print(f"[bold]Python Version:[/bold] {project_info.python_version}")
    console.print(f"[bold]Project Type:[/bold] {project_info.project_type}")
    console.print(f"[bold]Has uv.lock:[/bold] {project_info.has_uv_lock}")
    console.print(f"[bold]Entry Point:[/bold] {project_info.entry_point or 'Not detected'}")

    if project_info.dependencies:
        console.print(f"\n[bold]Dependencies ({len(project_info.dependencies)}):[/bold]")
        for dep in project_info.dependencies[:10]:
            console.print(f"  • {dep}")
        if len(project_info.dependencies) > 10:
            console.print(f"  ... and {len(project_info.dependencies) - 10} more")

    if project_info.frameworks:
        console.print("\n[bold]Detected Frameworks:[/bold]")
        for framework in project_info.frameworks:
            console.print(f"  • {framework}")

    # Show recommended optimizations
    console.print("\n[bold]Recommended Optimizations:[/bold]")
    for opt in project_info.recommended_optimizations:
        console.print(f"  [green]✓[/green] {opt}")


@app.command()
def build(
    path: Annotated[
        Path,
        typer.Argument(
            help="Path to the Python project.",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
        ),
    ] = Path("."),
    tag: Annotated[
        str,
        typer.Option(
            "--tag",
            "-t",
            help="Tag for the Docker image.",
        ),
    ] = "latest",
    push: Annotated[
        bool,
        typer.Option(
            "--push",
            help="Push the image after building.",
        ),
    ] = False,
) -> None:
    """🔨 Build Docker image for the project."""
    import subprocess

    from uv_dockerizer.analyzers.project import ProjectAnalyzer

    analyzer = ProjectAnalyzer(path)
    project_info = analyzer.analyze()

    image_name = f"{project_info.name}:{tag}"

    console.print(f"[bold]Building image:[/bold] {image_name}")

    result = subprocess.run(
        ["docker", "build", "-t", image_name, str(path)],
        capture_output=False,
    )

    if result.returncode == 0:
        console.print(f"\n[green]✓[/green] Successfully built [bold]{image_name}[/bold]")
        if push:
            console.print("[bold]Pushing image...[/bold]")
            subprocess.run(["docker", "push", image_name])
    else:
        console.print("\n[red]✗[/red] Build failed")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
