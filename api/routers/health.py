"""
Health Check Router - API health and status endpoints
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from api.schemas.model_info import HealthResponse
from registry.utils.mlflow_utils import verify_mlflow_connection
from registry.utils.logging_utils import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Check API health status.
    
    Returns health status including MLflow connection.
    """
    try:
        mlflow_ok = verify_mlflow_connection()
        
        return HealthResponse(
            status="healthy" if mlflow_ok else "degraded",
            mlflow_connection=mlflow_ok,
            timestamp=datetime.now().isoformat(),
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            mlflow_connection=False,
            timestamp=datetime.now().isoformat(),
        )


@router.get("/ready")
async def readiness_check():
    """
    Kubernetes readiness probe endpoint.
    
    Returns 200 if service is ready to accept traffic.
    """
    try:
        mlflow_ok = verify_mlflow_connection()
        
        if mlflow_ok:
            return {"status": "ready"}
        else:
            raise HTTPException(status_code=503, detail="Service not ready")
            
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=503, detail="Service not ready")


@router.get("/live")
async def liveness_check():
    """
    Kubernetes liveness probe endpoint.
    
    Returns 200 if service is alive.
    """
    return {"status": "alive"}