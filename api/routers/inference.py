"""
Inference Router - Model prediction endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import Optional
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from api.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
)
from api.services.model_service import model_service
from registry.utils.logging_utils import setup_logger

logger = setup_logger(__name__)

# CREATE ROUTER INSTANCE - THIS IS CRITICAL!
router = APIRouter()


@router.post("/{model_name}", response_model=PredictionResponse)
async def predict(model_name: str, request: PredictionRequest):
    """
    Make predictions using the latest production model.
    
    Args:
        model_name: Name of the registered model
        request: Prediction request with input instances
    """
    try:
        predictions = model_service.predict(
            model_name=model_name,
            instances=request.instances,
            stage="Production"
        )
        
        model_info = model_service.get_model_info(
            model_name=model_name,
            stage="Production"
        )
        
        return PredictionResponse(
            predictions=predictions,
            model_name=model_name,
            model_version=model_info["version"],
            model_stage=model_info["stage"]
        )
        
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{model_name}/version/{version}", response_model=PredictionResponse)
async def predict_version(
    model_name: str,
    version: str,
    request: PredictionRequest
):
    """
    Make predictions using a specific model version.
    
    Args:
        model_name: Name of the registered model
        version: Model version number
        request: Prediction request with input instances
    """
    try:
        predictions = model_service.predict(
            model_name=model_name,
            instances=request.instances,
            version=version
        )
        
        model_info = model_service.get_model_info(
            model_name=model_name,
            version=version
        )
        
        return PredictionResponse(
            predictions=predictions,
            model_name=model_name,
            model_version=version,
            model_stage=model_info["stage"]
        )
        
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{model_name}/stage/{stage}", response_model=PredictionResponse)
async def predict_stage(
    model_name: str,
    stage: str,
    request: PredictionRequest
):
    """
    Make predictions using a model from a specific stage.
    
    Args:
        model_name: Name of the registered model
        stage: Stage name (None, Staging, Production, Archived)
        request: Prediction request with input instances
    """
    try:
        predictions = model_service.predict(
            model_name=model_name,
            instances=request.instances,
            stage=stage
        )
        
        model_info = model_service.get_model_info(
            model_name=model_name,
            stage=stage
        )
        
        return PredictionResponse(
            predictions=predictions,
            model_name=model_name,
            model_version=model_info["version"],
            model_stage=stage
        )
        
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{model_name}/batch", response_model=BatchPredictionResponse)
async def predict_batch(
    model_name: str,
    request: BatchPredictionRequest
):
    """
    Make batch predictions with optional probability outputs.
    
    Args:
        model_name: Name of the registered model
        request: Batch prediction request
    """
    try:
        if request.return_probabilities:
            predictions, probabilities = model_service.predict_proba(
                model_name=model_name,
                instances=request.instances,
                stage="Production"
            )
        else:
            predictions = model_service.predict(
                model_name=model_name,
                instances=request.instances,
                stage="Production"
            )
            probabilities = None
        
        model_info = model_service.get_model_info(
            model_name=model_name,
            stage="Production"
        )
        
        return BatchPredictionResponse(
            predictions=predictions,
            probabilities=probabilities,
            model_name=model_name,
            model_version=model_info["version"],
            count=len(predictions)
        )
        
    except Exception as e:
        logger.error(f"Batch prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))