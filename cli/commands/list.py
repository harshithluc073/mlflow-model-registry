"""
CLI Commands - Listing Models

Commands for listing and viewing models.
"""

import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from registry.core.model_manager import ModelManager

app = typer.Typer(help="List and view models")
console = Console()


@app.command("models")
def list_models():
    """List all registered models."""
    try:
        manager = ModelManager()
        models = manager.list_models()
        
        if not models:
            console.print("[yellow]No registered models found[/yellow]")
            return
        
        table = Table(title="Registered Models", show_header=True, header_style="bold magenta")
        table.add_column("Model Name", style="cyan", no_wrap=True)
        table.add_column("Latest Versions", style="green")
        table.add_column("Description", style="white")
        
        for model in models:
            versions_str = ""
            for v in model["latest_versions"]:
                versions_str += f"v{v['version']} ({v['stage']})\n"
            
            table.add_row(
                model["name"],
                versions_str.strip(),
                model["description"] or "-",
            )
        
        console.print(table)
        console.print(f"\n[bold]Total models:[/bold] {len(models)}")
        
    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Error: {e}")
        raise typer.Exit(code=1)


@app.command("versions")
def list_versions(
    model_name: str = typer.Argument(..., help="Model name"),
    stage: Optional[str] = typer.Option(None, "--stage", "-s", help="Filter by stage"),
):
    """List all versions of a model."""
    try:
        manager = ModelManager()
        versions = manager.list_model_versions(model_name, stage=stage)
        
        if not versions:
            console.print(f"[yellow]No versions found for {model_name}[/yellow]")
            return
        
        table = Table(
            title=f"Versions of {model_name}" + (f" (Stage: {stage})" if stage else ""),
            show_header=True,
            header_style="bold magenta"
        )
        table.add_column("Version", style="cyan", no_wrap=True)
        table.add_column("Stage", style="green")
        table.add_column("Run ID", style="yellow")
        table.add_column("Status", style="white")
        table.add_column("Created", style="blue")
        
        for version in versions:
            created_time = datetime.fromtimestamp(
                version.creation_timestamp / 1000
            ).strftime("%Y-%m-%d %H:%M")
            
            table.add_row(
                version.version,
                version.current_stage,
                version.run_id[:8] + "...",
                version.status,
                created_time,
            )
        
        console.print(table)
        console.print(f"\n[bold]Total versions:[/bold] {len(versions)}")
        
    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Error: {e}")
        raise typer.Exit(code=1)


@app.command("info")
def model_info(
    model_name: str = typer.Argument(..., help="Model name"),
    version: Optional[str] = typer.Option(None, "--version", "-v", help="Specific version"),
):
    """Show detailed information about a model."""
    try:
        manager = ModelManager()
        
        if version:
            # Show specific version info
            model_version = manager.get_model_version(model_name, version=version)
            
            console.print(f"\n[bold cyan]Model:[/bold cyan] {model_name}")
            console.print(f"[bold cyan]Version:[/bold cyan] {model_version.version}")
            console.print(f"[bold cyan]Stage:[/bold cyan] {model_version.current_stage}")
            console.print(f"[bold cyan]Status:[/bold cyan] {model_version.status}")
            console.print(f"[bold cyan]Run ID:[/bold cyan] {model_version.run_id}")
            console.print(f"[bold cyan]Description:[/bold cyan] {model_version.description or '-'}")
            
            if model_version.tags:
                console.print(f"\n[bold cyan]Tags:[/bold cyan]")
                for key, value in model_version.tags.items():
                    console.print(f"  {key}: {value}")
        else:
            # Show overall model info
            info = manager.get_model_info(model_name)
            
            console.print(f"\n[bold cyan]Model:[/bold cyan] {info['name']}")
            console.print(f"[bold cyan]Description:[/bold cyan] {info['description'] or '-'}")
            console.print(f"[bold cyan]Total Versions:[/bold cyan] {len(info['versions'])}")
            
            # Show version summary
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Version", style="cyan")
            table.add_column("Stage", style="green")
            table.add_column("Status", style="white")
            
            for v in info['versions']:
                table.add_row(
                    v['version'],
                    v['stage'],
                    v['status'],
                )
            
            console.print("\n")
            console.print(table)
        
    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Error: {e}")
        raise typer.Exit(code=1)