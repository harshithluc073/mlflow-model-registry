"""
CLI Commands - Experiment Comparison

Commands for comparing model experiments and runs.
"""

import typer
from rich.console import Console
from rich.table import Table
from typing import List
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from registry.core.experiment_tracker import ExperimentTracker

app = typer.Typer(help="Compare experiments and runs")
console = Console()


@app.command("runs")
def compare_runs(
    run_ids: List[str] = typer.Argument(..., help="Run IDs to compare"),
):
    """Compare multiple MLflow runs."""
    try:
        tracker = ExperimentTracker()
        
        console.print(f"\nComparing {len(run_ids)} runs...\n")
        
        comparison = tracker.compare_runs(run_ids)
        
        # Display parameters comparison
        console.print("[bold cyan]Parameters Comparison[/bold cyan]")
        param_table = Table(show_header=True, header_style="bold magenta")
        param_table.add_column("Parameter", style="cyan")
        
        for run_data in comparison["runs"]:
            param_table.add_column(
                f"Run {run_data['run_id'][:8]}",
                style="green"
            )
        
        # Collect all unique parameters
        all_params = set()
        for run_data in comparison["runs"]:
            all_params.update(run_data["params"].keys())
        
        for param in sorted(all_params):
            row = [param]
            for run_data in comparison["runs"]:
                row.append(run_data["params"].get(param, "-"))
            param_table.add_row(*row)
        
        console.print(param_table)
        
        # Display metrics comparison
        console.print("\n[bold cyan]Metrics Comparison[/bold cyan]")
        metric_table = Table(show_header=True, header_style="bold magenta")
        metric_table.add_column("Metric", style="cyan")
        
        for run_data in comparison["runs"]:
            metric_table.add_column(
                f"Run {run_data['run_id'][:8]}",
                style="green"
            )
        
        # Collect all unique metrics
        all_metrics = set()
        for run_data in comparison["runs"]:
            all_metrics.update(run_data["metrics"].keys())
        
        for metric in sorted(all_metrics):
            row = [metric]
            for run_data in comparison["runs"]:
                value = run_data["metrics"].get(metric, "-")
                if value != "-":
                    row.append(f"{value:.4f}")
                else:
                    row.append(value)
            metric_table.add_row(*row)
        
        console.print(metric_table)
        
    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Error: {e}")
        raise typer.Exit(code=1)


@app.command("best")
def find_best_run(
    experiment_name: str = typer.Argument(..., help="Experiment name"),
    metric: str = typer.Option("accuracy", "--metric", "-m", help="Metric to optimize"),
    maximize: bool = typer.Option(True, "--maximize/--minimize", help="Maximize or minimize metric"),
    top_n: int = typer.Option(5, "--top", "-n", help="Number of top runs to show"),
):
    """Find the best runs in an experiment based on a metric."""
    try:
        tracker = ExperimentTracker(experiment_name)
        
        # Search runs ordered by metric
        order_direction = "DESC" if maximize else "ASC"
        order_by = [f"metrics.{metric} {order_direction}"]
        
        runs = tracker.search_runs(
            filter_string="",
            order_by=order_by,
            max_results=top_n,
        )
        
        if not runs:
            console.print(f"[yellow]No runs found in experiment '{experiment_name}'[/yellow]")
            return
        
        console.print(
            f"\n[bold cyan]Top {len(runs)} runs by {metric} ({'max' if maximize else 'min'})[/bold cyan]\n"
        )
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Rank", style="cyan", no_wrap=True)
        table.add_column("Run ID", style="yellow")
        table.add_column(metric.capitalize(), style="green")
        table.add_column("Status", style="white")
        
        for i, run in enumerate(runs, 1):
            metric_value = run.data.metrics.get(metric, "-")
            if metric_value != "-":
                metric_str = f"{metric_value:.4f}"
            else:
                metric_str = "-"
            
            table.add_row(
                str(i),
                run.info.run_id[:8] + "...",
                metric_str,
                run.info.status,
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Error: {e}")
        raise typer.Exit(code=1)