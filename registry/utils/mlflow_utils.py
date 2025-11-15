"""
MLflow Configuration Utilities

Helper functions for MLflow setup and configuration.
"""

import mlflow
from mlflow.tracking import MlflowClient
from typing import Optional, Dict, List
import logging

from config.settings import (
    get_tracking_uri,
    get_artifact_root,
    DEFAULT_EXPERIMENT_NAME,
)

logger = logging.getLogger(__name__)


def get_mlflow_client() -> MlflowClient:
    """
    Get configured MLflow client.
    
    Returns:
        MlflowClient instance
    """
    tracking_uri = get_tracking_uri()
    mlflow.set_tracking_uri(tracking_uri)
    return MlflowClient(tracking_uri=tracking_uri)


def create_experiment(
    name: str,
    artifact_location: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None
) -> str:
    """
    Create a new MLflow experiment.
    
    Args:
        name: Experiment name
        artifact_location: Optional custom artifact location
        tags: Optional experiment tags
        
    Returns:
        Experiment ID
    """
    client = get_mlflow_client()
    
    # Check if experiment already exists
    experiment = client.get_experiment_by_name(name)
    if experiment is not None:
        logger.info(f"Experiment '{name}' already exists with ID: {experiment.experiment_id}")
        return experiment.experiment_id
    
    # Set artifact location
    if artifact_location is None:
        artifact_location = f"{get_artifact_root()}/{name}"
    
    # Create experiment
    experiment_id = client.create_experiment(
        name=name,
        artifact_location=artifact_location,
        tags=tags or {}
    )
    
    logger.info(f"Created experiment '{name}' with ID: {experiment_id}")
    return experiment_id


def get_or_create_experiment(name: str) -> str:
    """
    Get existing experiment or create if it doesn't exist.
    
    Args:
        name: Experiment name
        
    Returns:
        Experiment ID
    """
    client = get_mlflow_client()
    experiment = client.get_experiment_by_name(name)
    
    if experiment is not None:
        return experiment.experiment_id
    
    return create_experiment(name)


def list_experiments() -> List[Dict[str, str]]:
    """
    List all experiments.
    
    Returns:
        List of experiment dictionaries
    """
    client = get_mlflow_client()
    experiments = client.search_experiments()
    
    return [
        {
            "experiment_id": exp.experiment_id,
            "name": exp.name,
            "artifact_location": exp.artifact_location,
            "lifecycle_stage": exp.lifecycle_stage,
        }
        for exp in experiments
    ]


def delete_experiment(experiment_id: str) -> None:
    """
    Delete an experiment.
    
    Args:
        experiment_id: ID of experiment to delete
    """
    client = get_mlflow_client()
    client.delete_experiment(experiment_id)
    logger.info(f"Deleted experiment with ID: {experiment_id}")


def set_experiment(experiment_name: str) -> None:
    """
    Set the active experiment.
    
    Args:
        experiment_name: Name of experiment to activate
    """
    # Create experiment if it doesn't exist
    experiment_id = get_or_create_experiment(experiment_name)
    mlflow.set_experiment(experiment_name)
    logger.info(f"Active experiment set to: {experiment_name} (ID: {experiment_id})")


def get_experiment_info(experiment_name: str) -> Optional[Dict[str, str]]:
    """
    Get information about an experiment.
    
    Args:
        experiment_name: Name of the experiment
        
    Returns:
        Experiment information dictionary or None
    """
    client = get_mlflow_client()
    experiment = client.get_experiment_by_name(experiment_name)
    
    if experiment is None:
        return None
    
    return {
        "experiment_id": experiment.experiment_id,
        "name": experiment.name,
        "artifact_location": experiment.artifact_location,
        "lifecycle_stage": experiment.lifecycle_stage,
        "creation_time": str(experiment.creation_time),
        "last_update_time": str(experiment.last_update_time),
    }


def verify_mlflow_connection() -> bool:
    """
    Verify MLflow connection is working.
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        client = get_mlflow_client()
        # Try to list experiments as a connection test
        client.search_experiments()
        logger.info("MLflow connection verified successfully")
        return True
    except Exception as e:
        logger.error(f"MLflow connection failed: {e}")
        return False