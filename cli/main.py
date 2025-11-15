"""
MLflow Model Registry CLI

Command-line interface for model lifecycle management.
"""

import typer
from rich.console import Console
from rich.table import Table
from typing import Optional

from cli.commands import register, list, promote, compare

app = typer.Typer(
    name="mlflow-registry",
    help="MLflow Model Registry - Production-ready ML model management",
    add_completion=False,
)

console = Console()

# Add command groups
app.add_typer(register.app, name="register", help="Register models")
app.add_typer(list.app, name="list", help="List models and versions")
app.add_typer(promote.app, name="promote", help="Promote models between stages")
app.add_typer(compare.app, name="compare", help="Compare experiments and runs")


@app.command()
def version():
    """Show version information."""
    console.print("[bold green]MLflow Model Registry v0.1.0[/bold green]")
    console.print("Production-ready model lifecycle management")


@app.command()
def init():
    """Initialize MLflow registry."""
    import subprocess
    import sys
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent
    init_script = project_root / "scripts" / "init_mlflow.py"
    
    console.print("[bold cyan]Initializing MLflow Model Registry...[/bold cyan]\n")
    
    result = subprocess.run([sys.executable, str(init_script)])
    
    if result.returncode == 0:
        console.print("\n[bold green]✓ Initialization complete![/bold green]")
    else:
        console.print("\n[bold red]✗ Initialization failed[/bold red]")
        raise typer.Exit(code=1)


@app.command()
def server():
    """Start MLflow tracking server."""
    import subprocess
    import sys
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent
    server_script = project_root / "scripts" / "start_mlflow.py"
    
    console.print("[bold cyan]Starting MLflow Tracking Server...[/bold cyan]\n")
    
    subprocess.run([sys.executable, str(server_script)])


@app.callback()
def callback():
    """
    MLflow Model Registry CLI
    
    Manage your ML models with confidence.
    """
    pass


if __name__ == "__main__":
    app()