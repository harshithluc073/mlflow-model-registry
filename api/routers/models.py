"""
Models Router - Model metadata and registry endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import Optional
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from api.schemas.model_info import ModelsListResponse, ModelInfo, ModelVersionInfo
from registry.core.model_manager import ModelManager
from registry.utils.logging_utils import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


@router.get("/", response_model=ModelsListResponse)
async def list_models():
    """
    List all registered models.
    
    Returns a list of all models in the registry.
    """
    try:
        manager = ModelManager()
        models = manager.list_models()
        
        model_list = []
        for model in models:
            latest_versions = [
                ModelVersionInfo(
                    version=str(v["version"]),
                    stage=v["stage"],
                    run_id=v["run_id"],
                    status="READY"
                )
                for v in model["latest_versions"]
            ]
            
            model_info = ModelInfo(
                name=model["name"],
                description=model.get("description"),
                latest_versions=latest_versions,
                creation_timestamp=model.get("creation_timestamp")
            )
            model_list.append(model_info)
        
        return ModelsListResponse(
            models=model_list,
            total_count=len(model_list)
        )
        
    except Exception as e:
        logger.error(f"Failed to list models: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{model_name}")
async def get_model_info(model_name: str):
    """
    Get information about a specific model.
    
    Args:
        model_name: Name of the registered model
    """
    try:
        manager = ModelManager()
        info = manager.get_model_info(model_name)
        
        return {
            "name": info["name"],
            "description": info.get("description"),
            "versions": info["versions"],
            "creation_timestamp": info.get("creation_timestamp"),
            "last_updated_timestamp": info.get("last_updated_timestamp"),
        }
        
    except Exception as e:
        logger.error(f"Failed to get model info: {e}")
        raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found")


@router.get("/{model_name}/version/{version}")
async def get_model_version_info(model_name: str, version: str):
    """
    Get information about a specific model version.
    
    Args:
        model_name: Name of the registered model
        version: Version number
    """
    try:
        manager = ModelManager()
        model_version = manager.get_model_version(model_name, version=version)
        
        return {
            "name": model_name,
            "version": model_version.version,
            "stage": model_version.current_stage,
            "run_id": model_version.run_id,
            "status": model_version.status,
            "description": model_version.description,
            "tags": model_version.tags,
            "creation_timestamp": model_version.creation_timestamp,
            "last_updated_timestamp": model_version.last_updated_timestamp,
        }
        
    except Exception as e:
        logger.error(f"Failed to get model version info: {e}")
        raise HTTPException(
            status_code=404, 
            detail=f"Model '{model_name}' version '{version}' not found"
        )