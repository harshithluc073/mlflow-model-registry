"""
Model Info Schemas - Model metadata schemas
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str = Field(..., description="Health status")
    mlflow_connection: bool = Field(..., description="MLflow connection status")
    timestamp: str = Field(..., description="Timestamp of health check")


class ModelVersionInfo(BaseModel):
    """Model version information schema."""
    version: str = Field(..., description="Model version number")
    stage: str = Field(..., description="Current stage")
    run_id: str = Field(..., description="MLflow run ID")
    status: str = Field(..., description="Version status")


class ModelInfo(BaseModel):
    """Registered model information schema."""
    name: str = Field(..., description="Model name")
    description: Optional[str] = Field(None, description="Model description")
    latest_versions: List[ModelVersionInfo] = Field(
        ..., description="Latest versions per stage"
    )
    creation_timestamp: Optional[int] = Field(None, description="Creation timestamp")


class ModelsListResponse(BaseModel):
    """List of registered models response."""
    models: List[ModelInfo] = Field(..., description="List of models")
    total_count: int = Field(..., description="Total number of models")