"""
CLI Commands - Model Promotion

Commands for promoting models between stages.
"""

import typer
from rich.console import Console
from typing import Optional
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from registry.core.stage_manager import StageManager
from config.settings import STAGE_STAGING, STAGE_PRODUCTION, STAGE_DEV, STAGE_ARCHIVED

app = typer.Typer(help="Model promotion commands")
console = Console()


@app.command("staging")
def promote_to_staging(
    model_name: str = typer.Argument(..., help="Model name"),
    version: str = typer.Argument(..., help="Version to promote"),
    archive_existing: bool = typer.Option(True, "--archive/--no-archive", help="Archive existing staging versions"),
):
    """Promote a model from Development to Staging."""
    try:
        manager = StageManager()
        
        console.print(
            f"Promoting [bold]{model_name}[/bold] version [bold]{version}[/bold] to Staging..."
        )
        
        manager.promote_to_staging(
            model_name=model_name,
            version=version,
            archive_existing=archive_existing,
        )
        
        console.print(
            f"[bold green]✓[/bold green] Successfully promoted to Staging"
        )
        
    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Error: {e}")
        raise typer.Exit(code=1)


@app.command("production")
def promote_to_production(
    model_name: str = typer.Argument(..., help="Model name"),
    version: str = typer.Argument(..., help="Version to promote"),
    archive_existing: bool = typer.Option(True, "--archive/--no-archive", help="Archive existing production versions"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Promote a model from Staging to Production."""
    try:
        if not force:
            confirm = typer.confirm(
                f"Promote {model_name} v{version} to PRODUCTION?"
            )
            if not confirm:
                console.print("[yellow]Cancelled[/yellow]")
                raise typer.Exit()
        
        manager = StageManager()
        
        console.print(
            f"Promoting [bold]{model_name}[/bold] version [bold]{version}[/bold] to Production..."
        )
        
        manager.promote_to_production(
            model_name=model_name,
            version=version,
            archive_existing=archive_existing,
        )
        
        console.print(
            f"[bold green]✓[/bold green] Successfully promoted to Production"
        )
        
    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Error: {e}")
        raise typer.Exit(code=1)


@app.command("archive")
def archive_model(
    model_name: str = typer.Argument(..., help="Model name"),
    version: str = typer.Argument(..., help="Version to archive"),
):
    """Archive a model version."""
    try:
        manager = StageManager()
        
        manager.archive_model(
            model_name=model_name,
            version=version,
        )
        
        console.print(
            f"[bold green]✓[/bold green] Archived [bold]{model_name}[/bold] version {version}"
        )
        
    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Error: {e}")
        raise typer.Exit(code=1)


@app.command("rollback")
def rollback_production(
    model_name: str = typer.Argument(..., help="Model name"),
    version: str = typer.Argument(..., help="Version to rollback to"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Rollback production to a previous version."""
    try:
        if not force:
            confirm = typer.confirm(
                f"Rollback {model_name} production to v{version}?"
            )
            if not confirm:
                console.print("[yellow]Cancelled[/yellow]")
                raise typer.Exit()
        
        manager = StageManager()
        
        console.print(
            f"Rolling back [bold]{model_name}[/bold] to version [bold]{version}[/bold]..."
        )
        
        manager.rollback_production(
            model_name=model_name,
            target_version=version,
        )
        
        console.print(
            f"[bold green]✓[/bold green] Successfully rolled back to v{version}"
        )
        
    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Error: {e}")
        raise typer.Exit(code=1)


@app.command("status")
def stage_status(
    model_name: str = typer.Argument(..., help="Model name"),
):
    """Show current stage status for all versions of a model."""
    try:
        manager = StageManager()
        
        stage_info = manager.get_stage_info(model_name)
        
        console.print(f"\n[bold cyan]Stage Status for {model_name}[/bold cyan]\n")
        
        for stage, versions in stage_info.items():
            if versions:
                versions_str = ", ".join(f"v{v}" for v in versions)
                console.print(f"[bold]{stage}:[/bold] {versions_str}")
            else:
                console.print(f"[bold]{stage}:[/bold] [dim]-[/dim]")
        
    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Error: {e}")
        raise typer.Exit(code=1)