"""
Experiment Tracker - MLflow experiment management

Handles experiment creation, run tracking, and parameter/metric logging.
"""

import mlflow
from mlflow.tracking import MlflowClient
from typing import Optional, Dict, Any, List
import logging

from registry.utils.logging_utils import setup_logger
from registry.utils.mlflow_utils import (
    get_mlflow_client,
    get_or_create_experiment,
    set_experiment,
)

logger = setup_logger(__name__)


class ExperimentTracker:
    """Tracks ML experiments using MLflow."""
    
    def __init__(self, experiment_name: Optional[str] = None):
        """
        Initialize ExperimentTracker.
        
        Args:
            experiment_name: Name of the experiment to use
        """
        self.client = get_mlflow_client()
        
        if experiment_name:
            set_experiment(experiment_name)
            self.experiment_name = experiment_name
        else:
            self.experiment_name = None
        
        logger.info(f"ExperimentTracker initialized for '{experiment_name}'")
    
    def start_run(
        self,
        run_name: Optional[str] = None,
        nested: bool = False,
        tags: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
    ) -> mlflow.ActiveRun:
        """
        Start a new MLflow run.
        
        Args:
            run_name: Name for the run
            nested: Whether this is a nested run
            tags: Optional tags for the run
            description: Optional run description
            
        Returns:
            Active MLflow run context
        """
        try:
            run = mlflow.start_run(
                run_name=run_name,
                nested=nested,
                tags=tags,
                description=description
            )
            
            logger.info(f"Started run: {run.info.run_id}")
            return run
            
        except Exception as e:
            logger.error(f"Failed to start run: {e}")
            raise
    
    def log_params(self, params: Dict[str, Any]) -> None:
        """
        Log parameters to the active run.
        
        Args:
            params: Dictionary of parameters to log
        """
        try:
            mlflow.log_params(params)
            logger.debug(f"Logged {len(params)} parameters")
            
        except Exception as e:
            logger.error(f"Failed to log parameters: {e}")
            raise
    
    def log_metrics(
        self,
        metrics: Dict[str, float],
        step: Optional[int] = None,
    ) -> None:
        """
        Log metrics to the active run.
        
        Args:
            metrics: Dictionary of metrics to log
            step: Optional step number for the metrics
        """
        try:
            mlflow.log_metrics(metrics, step=step)
            logger.debug(f"Logged {len(metrics)} metrics")
            
        except Exception as e:
            logger.error(f"Failed to log metrics: {e}")
            raise
    
    def log_metric(
        self,
        key: str,
        value: float,
        step: Optional[int] = None,
    ) -> None:
        """
        Log a single metric to the active run.
        
        Args:
            key: Metric name
            value: Metric value
            step: Optional step number
        """
        try:
            mlflow.log_metric(key, value, step=step)
            logger.debug(f"Logged metric: {key}={value}")
            
        except Exception as e:
            logger.error(f"Failed to log metric: {e}")
            raise
    
    def log_artifact(self, local_path: str, artifact_path: Optional[str] = None) -> None:
        """
        Log an artifact to the active run.
        
        Args:
            local_path: Local path to the artifact
            artifact_path: Optional path within the artifact directory
        """
        try:
            mlflow.log_artifact(local_path, artifact_path)
            logger.debug(f"Logged artifact: {local_path}")
            
        except Exception as e:
            logger.error(f"Failed to log artifact: {e}")
            raise
    
    def log_model(
        self,
        model: Any,
        artifact_path: str,
        registered_model_name: Optional[str] = None,
        **kwargs,
    ) -> None:
        """
        Log a model to the active run.
        
        Args:
            model: Model object to log
            artifact_path: Path within the artifact directory
            registered_model_name: Optional name to register the model
            **kwargs: Additional arguments for model logging
        """
        try:
            # Detect model type and log appropriately
            if hasattr(model, 'fit') and hasattr(model, 'predict'):
                # Scikit-learn model
                mlflow.sklearn.log_model(
                    model,
                    artifact_path,
                    registered_model_name=registered_model_name,
                    **kwargs
                )
            else:
                # Generic Python model
                mlflow.pyfunc.log_model(
                    artifact_path=artifact_path,
                    python_model=model,
                    registered_model_name=registered_model_name,
                    **kwargs
                )
            
            logger.info(f"Logged model to: {artifact_path}")
            
        except Exception as e:
            logger.error(f"Failed to log model: {e}")
            raise
    
    def set_tags(self, tags: Dict[str, str]) -> None:
        """
        Set tags on the active run.
        
        Args:
            tags: Dictionary of tags to set
        """
        try:
            mlflow.set_tags(tags)
            logger.debug(f"Set {len(tags)} tags")
            
        except Exception as e:
            logger.error(f"Failed to set tags: {e}")
            raise
    
    def end_run(self, status: str = "FINISHED") -> None:
        """
        End the active run.
        
        Args:
            status: Run status (FINISHED, FAILED, KILLED)
        """
        try:
            mlflow.end_run(status=status)
            logger.info(f"Ended run with status: {status}")
            
        except Exception as e:
            logger.error(f"Failed to end run: {e}")
            raise
    
    def get_run(self, run_id: str) -> mlflow.entities.Run:
        """
        Get information about a specific run.
        
        Args:
            run_id: ID of the run
            
        Returns:
            Run object
        """
        try:
            return self.client.get_run(run_id)
            
        except Exception as e:
            logger.error(f"Failed to get run: {e}")
            raise
    
    def search_runs(
        self,
        filter_string: str = "",
        order_by: Optional[List[str]] = None,
        max_results: int = 1000,
    ) -> List[mlflow.entities.Run]:
        """
        Search for runs in the experiment.
        
        Args:
            filter_string: Filter query string
            order_by: List of columns to order by
            max_results: Maximum number of results
            
        Returns:
            List of Run objects
        """
        try:
            if self.experiment_name:
                experiment_id = get_or_create_experiment(self.experiment_name)
                experiment_ids = [experiment_id]
            else:
                experiment_ids = None
            
            runs = self.client.search_runs(
                experiment_ids=experiment_ids,
                filter_string=filter_string,
                order_by=order_by,
                max_results=max_results
            )
            
            return runs
            
        except Exception as e:
            logger.error(f"Failed to search runs: {e}")
            raise
    
    def compare_runs(
        self,
        run_ids: List[str],
        metric_names: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Compare multiple runs.
        
        Args:
            run_ids: List of run IDs to compare
            metric_names: Optional list of specific metrics to compare
            
        Returns:
            Dictionary with comparison data
        """
        try:
            comparison = {
                "runs": [],
                "metrics": {},
            }
            
            for run_id in run_ids:
                run = self.get_run(run_id)
                
                run_data = {
                    "run_id": run_id,
                    "run_name": run.data.tags.get("mlflow.runName", ""),
                    "params": run.data.params,
                    "metrics": run.data.metrics,
                    "status": run.info.status,
                    "start_time": run.info.start_time,
                    "end_time": run.info.end_time,
                }
                
                comparison["runs"].append(run_data)
                
                # Aggregate metrics
                for metric_name, metric_value in run.data.metrics.items():
                    if metric_names and metric_name not in metric_names:
                        continue
                    
                    if metric_name not in comparison["metrics"]:
                        comparison["metrics"][metric_name] = []
                    
                    comparison["metrics"][metric_name].append({
                        "run_id": run_id,
                        "value": metric_value,
                    })
            
            return comparison
            
        except Exception as e:
            logger.error(f"Failed to compare runs: {e}")
            raise