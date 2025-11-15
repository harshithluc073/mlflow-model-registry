"""
Prediction Schemas - Request/Response models for predictions
"""

from pydantic import BaseModel, Field
from typing import List, Any, Optional


class PredictionRequest(BaseModel):
    """Prediction request schema."""
    instances: List[List[float]] = Field(
        ...,
        description="Input instances for prediction",
        example=[[1.0, 2.0, 3.0]]
    )


class PredictionResponse(BaseModel):
    """Prediction response schema."""
    predictions: List[Any] = Field(..., description="Model predictions")
    model_name: str = Field(..., description="Model name used")
    model_version: Optional[str] = Field(None, description="Model version used")
    model_stage: Optional[str] = Field(None, description="Model stage used")


class BatchPredictionRequest(BaseModel):
    """Batch prediction request schema."""
    instances: List[List[float]] = Field(
        ...,
        description="Batch of input instances",
        example=[[1.0, 2.0], [3.0, 4.0]]
    )
    return_probabilities: bool = Field(
        False,
        description="Return class probabilities (classification only)"
    )


class BatchPredictionResponse(BaseModel):
    """Batch prediction response schema."""
    predictions: List[Any] = Field(..., description="Batch predictions")
    probabilities: Optional[List[List[float]]] = Field(
        None, description="Class probabilities (if requested)"
    )
    model_name: str = Field(..., description="Model name used")
    model_version: Optional[str] = Field(None, description="Model version")
    count: int = Field(..., description="Number of predictions")


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Error details")
    timestamp: str = Field(..., description="Error timestamp")