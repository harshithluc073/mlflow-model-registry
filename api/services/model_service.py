"""
Model Service - Model loading and inference

Handles model loading from MLflow registry and prediction serving.
"""

import mlflow
from mlflow.tracking import MlflowClient
from typing import Optional, Any, List, Dict
import numpy as np
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from registry.core.model_manager import ModelManager
from registry.utils.logging_utils import setup_logger
from config.settings import STAGE_PRODUCTION

logger = setup_logger(__name__)


class ModelService:
    """Service for loading and serving models."""
    
    def __init__(self):
        """Initialize ModelService."""
        self.model_manager = ModelManager()
        self._loaded_models: Dict[str, Any] = {}
        logger.info("ModelService initialized")
    
    def load_model(
        self,
        model_name: str,
        version: Optional[str] = None,
        stage: Optional[str] = None,
    ) -> Any:
        """
        Load a model from MLflow registry.
        
        Args:
            model_name: Name of the registered model
            version: Specific version to load (or None to use stage)
            stage: Stage to load from (or None to use version)
            
        Returns:
            Loaded model object
        """
        try:
            # Create cache key
            if version:
                cache_key = f"{model_name}:v{version}"
            elif stage:
                cache_key = f"{model_name}:{stage}"
            else:
                # Default to production
                stage = STAGE_PRODUCTION
                cache_key = f"{model_name}:{stage}"
            
            # Check if model is already loaded
            if cache_key in self._loaded_models:
                logger.info(f"Using cached model: {cache_key}")
                return self._loaded_models[cache_key]
            
            # Get model version
            model_version = self.model_manager.get_model_version(
                model_name=model_name,
                version=version,
                stage=stage,
            )
            
            # Load model using MLflow
            model_uri = f"models:/{model_name}/{model_version.version}"
            model = mlflow.pyfunc.load_model(model_uri)
            
            # Cache the model
            self._loaded_models[cache_key] = model
            
            logger.info(
                f"Loaded model: {model_name} v{model_version.version} "
                f"(stage: {model_version.current_stage})"
            )
            
            return model
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def predict(
        self,
        model_name: str,
        instances: List[List[float]],
        version: Optional[str] = None,
        stage: Optional[str] = None,
    ) -> List[Any]:
        """
        Make predictions using a loaded model.
        
        Args:
            model_name: Name of the registered model
            instances: Input data for prediction
            version: Specific version to use
            stage: Stage to use
            
        Returns:
            List of predictions
        """
        try:
            # Load model
            model = self.load_model(
                model_name=model_name,
                version=version,
                stage=stage,
            )
            
            # Convert instances to numpy array
            input_data = np.array(instances)
            
            # Make predictions
            predictions = model.predict(input_data)
            
            # Convert to list
            if isinstance(predictions, np.ndarray):
                predictions = predictions.tolist()
            
            logger.info(
                f"Made {len(predictions)} predictions using {model_name}"
            )
            
            return predictions
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise
    
    def predict_proba(
        self,
        model_name: str,
        instances: List[List[float]],
        version: Optional[str] = None,
        stage: Optional[str] = None,
    ) -> tuple:
        """
        Make predictions with probabilities (classification models).
        
        Args:
            model_name: Name of the registered model
            instances: Input data for prediction
            version: Specific version to use
            stage: Stage to use
            
        Returns:
            Tuple of (predictions, probabilities)
        """
        try:
            # Load model
            model = self.load_model(
                model_name=model_name,
                version=version,
                stage=stage,
            )
            
            # Convert instances to numpy array
            input_data = np.array(instances)
            
            # Get underlying sklearn model if available
            if hasattr(model, '_model_impl'):
                sklearn_model = model._model_impl.python_model
                if hasattr(sklearn_model, 'predict_proba'):
                    # Make predictions
                    predictions = sklearn_model.predict(input_data)
                    probabilities = sklearn_model.predict_proba(input_data)
                    
                    # Convert to lists
                    if isinstance(predictions, np.ndarray):
                        predictions = predictions.tolist()
                    if isinstance(probabilities, np.ndarray):
                        probabilities = probabilities.tolist()
                    
                    return predictions, probabilities
            
            # Fallback to regular predictions if no predict_proba
            predictions = model.predict(input_data)
            if isinstance(predictions, np.ndarray):
                predictions = predictions.tolist()
            
            return predictions, []
            
        except Exception as e:
            logger.error(f"Prediction with probabilities failed: {e}")
            raise
    
    def get_model_info(
        self,
        model_name: str,
        version: Optional[str] = None,
        stage: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get information about a loaded model.
        
        Args:
            model_name: Name of the registered model
            version: Specific version
            stage: Stage
            
        Returns:
            Dictionary with model information
        """
        try:
            model_version = self.model_manager.get_model_version(
                model_name=model_name,
                version=version,
                stage=stage,
            )
            
            return {
                "name": model_name,
                "version": str(model_version.version),  # Convert to string
                "stage": model_version.current_stage,
                "run_id": model_version.run_id,
                "status": model_version.status,
                "description": model_version.description,
                "tags": model_version.tags,
            }
            
        except Exception as e:
            logger.error(f"Failed to get model info: {e}")
            raise
    
    def clear_cache(self):
        """Clear the model cache."""
        self._loaded_models.clear()
        logger.info("Model cache cleared")
    
    def get_cached_models(self) -> List[str]:
        """Get list of cached model keys."""
        return list(self._loaded_models.keys())


# Global model service instance
model_service = ModelService()