"""
CLI Commands - Model Registration

Commands for registering models in the registry.
"""

import typer
from rich.console import Console
from rich.panel import Panel
from typing import Optional, List
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from registry.core.model_manager import ModelManager

app = typer.Typer(help="Model registration commands")
console = Console()


@app.command("create")
def create_model(
    name: str = typer.Argument(..., help="Model name"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Model description"),
):
    """Create a new registered model."""
    try:
        manager = ModelManager()
        manager.create_registered_model(
            name=name,
            description=description,
        )
        
        console.print(f"[bold green]✓[/bold green] Created registered model: [bold]{name}[/bold]")
        
    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Error: {e}")
        raise typer.Exit(code=1)


@app.command("from-run")
def register_from_run(
    run_id: str = typer.Argument(..., help="MLflow run ID"),
    model_name: str = typer.Argument(..., help="Model name to register"),
    artifact_path: str = typer.Option("model", "--artifact-path", "-a", help="Artifact path in run"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Version description"),
):
    """Register a model from an existing MLflow run."""
    try:
        manager = ModelManager()
        
        model_uri = f"runs:/{run_id}/{artifact_path}"
        
        model_version = manager.register_model(
            model_uri=model_uri,
            model_name=model_name,
            description=description,
        )
        
        console.print(
            f"[bold green]✓[/bold green] Registered [bold]{model_name}[/bold] "
            f"version [bold]{model_version.version}[/bold]"
        )
        console.print(f"  Run ID: {run_id}")
        console.print(f"  Stage: {model_version.current_stage}")
        
    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Error: {e}")
        raise typer.Exit(code=1)


@app.command("delete")
def delete_model(
    name: str = typer.Argument(..., help="Model name"),
    version: Optional[str] = typer.Option(None, "--version", "-v", help="Specific version to delete"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Delete a registered model or specific version."""
    try:
        manager = ModelManager()
        
        if version:
            # Delete specific version
            if not force:
                confirm = typer.confirm(
                    f"Delete {name} version {version}?"
                )
                if not confirm:
                    console.print("[yellow]Cancelled[/yellow]")
                    raise typer.Exit()
            
            manager.delete_model_version(name, version)
            console.print(
                f"[bold green]✓[/bold green] Deleted [bold]{name}[/bold] version {version}"
            )
        else:
            # Delete entire model
            if not force:
                confirm = typer.confirm(
                    f"Delete entire model '{name}' and ALL its versions?"
                )
                if not confirm:
                    console.print("[yellow]Cancelled[/yellow]")
                    raise typer.Exit()
            
            manager.delete_registered_model(name)
            console.print(
                f"[bold green]✓[/bold green] Deleted registered model: [bold]{name}[/bold]"
            )
        
    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Error: {e}")
        raise typer.Exit(code=1)