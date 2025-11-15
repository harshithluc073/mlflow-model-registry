"""
Model Manager - Core model registry operations

Handles model registration, versioning, and stage management.
"""

import mlflow
from mlflow.tracking import MlflowClient
from mlflow.entities.model_registry import ModelVersion
from typing import Optional, Dict, List, Any
import logging

from config.settings import (
    STAGE_DEV,
    STAGE_STAGING,
    STAGE_PRODUCTION,
    STAGE_ARCHIVED,
    VALID_STAGES,
)
from registry.utils.logging_utils import setup_logger
from registry.utils.mlflow_utils import get_mlflow_client

logger = setup_logger(__name__)


class ModelManager:
    """Manages model lifecycle in MLflow registry."""
    
    def __init__(self):
        """Initialize ModelManager with MLflow client."""
        self.client = get_mlflow_client()
        logger.info("ModelManager initialized")
    
    def register_model(
        self,
        model_uri: str,
        model_name: str,
        tags: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
    ) -> ModelVersion:
        """
        Register a model in the MLflow registry.
        
        Args:
            model_uri: URI of the model artifact (e.g., runs:/<run_id>/model)
            model_name: Name to register the model under
            tags: Optional tags for the model version
            description: Optional description
            
        Returns:
            Registered ModelVersion object
        """
        try:
            # Register model
            model_version = mlflow.register_model(
                model_uri=model_uri,
                name=model_name,
                tags=tags
            )
            
            # Add description if provided
            if description:
                self.client.update_model_version(
                    name=model_name,
                    version=model_version.version,
                    description=description
                )
            
            logger.info(
                f"Registered model '{model_name}' version {model_version.version}"
            )
            
            return model_version
            
        except Exception as e:
            logger.error(f"Failed to register model: {e}")
            raise
    
    def create_registered_model(
        self,
        name: str,
        tags: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
    ) -> None:
        """
        Create a new registered model (without version).
        
        Args:
            name: Model name
            tags: Optional tags
            description: Optional description
        """
        try:
            self.client.create_registered_model(
                name=name,
                tags=tags,
                description=description
            )
            logger.info(f"Created registered model: {name}")
            
        except Exception as e:
            logger.error(f"Failed to create registered model: {e}")
            raise
    
    def get_model_version(
        self,
        model_name: str,
        version: Optional[str] = None,
        stage: Optional[str] = None,
    ) -> ModelVersion:
        """
        Get a specific model version.
        
        Args:
            model_name: Name of the registered model
            version: Version number (or None to use stage)
            stage: Stage name (or None to use version)
            
        Returns:
            ModelVersion object
        """
        try:
            if version:
                model_version = self.client.get_model_version(
                    name=model_name,
                    version=version
                )
            elif stage:
                if stage not in VALID_STAGES:
                    raise ValueError(f"Invalid stage: {stage}")
                
                # Get latest version in stage
                versions = self.client.get_latest_versions(
                    name=model_name,
                    stages=[stage]
                )
                
                if not versions:
                    raise ValueError(
                        f"No model version found in stage '{stage}'"
                    )
                
                model_version = versions[0]
            else:
                raise ValueError("Must specify either version or stage")
            
            return model_version
            
        except Exception as e:
            logger.error(f"Failed to get model version: {e}")
            raise
    
    def transition_stage(
        self,
        model_name: str,
        version: str,
        stage: str,
        archive_existing: bool = True,
    ) -> ModelVersion:
        """
        Transition a model version to a new stage.
        
        Args:
            model_name: Name of the registered model
            version: Version number to transition
            stage: Target stage (Development, Staging, Production, Archived)
            archive_existing: Whether to archive existing versions in target stage
            
        Returns:
            Updated ModelVersion object
        """
        try:
            if stage not in VALID_STAGES:
                raise ValueError(
                    f"Invalid stage '{stage}'. Must be one of: {VALID_STAGES}"
                )
            
            # Transition the version
            model_version = self.client.transition_model_version_stage(
                name=model_name,
                version=version,
                stage=stage,
                archive_existing_versions=archive_existing
            )
            
            logger.info(
                f"Transitioned {model_name} v{version} to {stage}"
            )
            
            return model_version
            
        except Exception as e:
            logger.error(f"Failed to transition model stage: {e}")
            raise
    
    def list_models(self) -> List[Dict[str, Any]]:
        """
        List all registered models.
        
        Returns:
            List of model dictionaries
        """
        try:
            models = self.client.search_registered_models()
            
            model_list = []
            for model in models:
                model_info = {
                    "name": model.name,
                    "creation_timestamp": model.creation_timestamp,
                    "last_updated_timestamp": model.last_updated_timestamp,
                    "description": model.description,
                    "latest_versions": [],
                }
                
                # Get latest version per stage
                for version in model.latest_versions:
                    model_info["latest_versions"].append({
                        "version": version.version,
                        "stage": version.current_stage,
                        "run_id": version.run_id,
                    })
                
                model_list.append(model_info)
            
            return model_list
            
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            raise
    
    def list_model_versions(
        self,
        model_name: str,
        stage: Optional[str] = None,
    ) -> List[ModelVersion]:
        """
        List all versions of a model.
        
        Args:
            model_name: Name of the registered model
            stage: Optional stage filter
            
        Returns:
            List of ModelVersion objects
        """
        try:
            if stage and stage not in VALID_STAGES:
                raise ValueError(f"Invalid stage: {stage}")
            
            # Search model versions
            filter_string = f"name='{model_name}'"
            
            versions = self.client.search_model_versions(filter_string)
            
            # Filter by stage if specified
            if stage:
                versions = [v for v in versions if v.current_stage == stage]
            
            return versions
            
        except Exception as e:
            logger.error(f"Failed to list model versions: {e}")
            raise
    
    def delete_model_version(
        self,
        model_name: str,
        version: str,
    ) -> None:
        """
        Delete a specific model version.
        
        Args:
            model_name: Name of the registered model
            version: Version number to delete
        """
        try:
            self.client.delete_model_version(
                name=model_name,
                version=version
            )
            logger.info(f"Deleted {model_name} version {version}")
            
        except Exception as e:
            logger.error(f"Failed to delete model version: {e}")
            raise
    
    def delete_registered_model(self, model_name: str) -> None:
        """
        Delete a registered model and all its versions.
        
        Args:
            model_name: Name of the registered model
        """
        try:
            self.client.delete_registered_model(name=model_name)
            logger.info(f"Deleted registered model: {model_name}")
            
        except Exception as e:
            logger.error(f"Failed to delete registered model: {e}")
            raise
    
    def update_model_version(
        self,
        model_name: str,
        version: str,
        description: Optional[str] = None,
    ) -> ModelVersion:
        """
        Update model version metadata.
        
        Args:
            model_name: Name of the registered model
            version: Version number
            description: New description
            
        Returns:
            Updated ModelVersion object
        """
        try:
            model_version = self.client.update_model_version(
                name=model_name,
                version=version,
                description=description
            )
            
            logger.info(f"Updated {model_name} version {version}")
            return model_version
            
        except Exception as e:
            logger.error(f"Failed to update model version: {e}")
            raise
    
    def set_model_version_tag(
        self,
        model_name: str,
        version: str,
        key: str,
        value: str,
    ) -> None:
        """
        Set a tag on a model version.
        
        Args:
            model_name: Name of the registered model
            version: Version number
            key: Tag key
            value: Tag value
        """
        try:
            self.client.set_model_version_tag(
                name=model_name,
                version=version,
                key=key,
                value=value
            )
            logger.info(f"Set tag '{key}={value}' on {model_name} v{version}")
            
        except Exception as e:
            logger.error(f"Failed to set model version tag: {e}")
            raise
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """
        Get comprehensive information about a registered model.
        
        Args:
            model_name: Name of the registered model
            
        Returns:
            Dictionary with model information
        """
        try:
            model = self.client.get_registered_model(model_name)
            
            info = {
                "name": model.name,
                "creation_timestamp": model.creation_timestamp,
                "last_updated_timestamp": model.last_updated_timestamp,
                "description": model.description,
                "tags": model.tags,
                "versions": [],
            }
            
            # Get all versions
            versions = self.list_model_versions(model_name)
            for version in versions:
                version_info = {
                    "version": version.version,
                    "stage": version.current_stage,
                    "run_id": version.run_id,
                    "status": version.status,
                    "creation_timestamp": version.creation_timestamp,
                    "last_updated_timestamp": version.last_updated_timestamp,
                    "description": version.description,
                    "tags": version.tags,
                }
                info["versions"].append(version_info)
            
            return info
            
        except Exception as e:
            logger.error(f"Failed to get model info: {e}")
            raise