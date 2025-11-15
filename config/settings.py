"""
Configuration Settings for MLflow Model Registry

Environment-based configuration management.
"""

import os
from pathlib import Path
from typing import Optional

# Project Root
PROJECT_ROOT = Path(__file__).parent.parent

# MLflow Configuration
MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI", f"sqlite:///{PROJECT_ROOT}/data/mlflow.db"
)
MLFLOW_ARTIFACT_ROOT = os.getenv(
    "MLFLOW_ARTIFACT_ROOT", str(PROJECT_ROOT / "data" / "mlartifacts")
)
MLFLOW_BACKEND_STORE = os.getenv(
    "MLFLOW_BACKEND_STORE", str(PROJECT_ROOT / "data" / "mlruns")
)

# Model Registry Configuration
REGISTRY_NAME = os.getenv("REGISTRY_NAME", "mlflow-model-registry")
DEFAULT_EXPERIMENT_NAME = os.getenv("DEFAULT_EXPERIMENT_NAME", "default")

# Stage Names
STAGE_DEV = "Development"
STAGE_STAGING = "Staging"
STAGE_PRODUCTION = "Production"
STAGE_ARCHIVED = "Archived"

VALID_STAGES = [STAGE_DEV, STAGE_STAGING, STAGE_PRODUCTION, STAGE_ARCHIVED]

# Validation Thresholds
MIN_ACCURACY_THRESHOLD = float(os.getenv("MIN_ACCURACY_THRESHOLD", "0.75"))
REQUIRED_TAGS = ["model_type", "created_by", "framework"]

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_RELOAD = os.getenv("API_RELOAD", "true").lower() == "true"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Database Configuration (for optional PostgreSQL)
DB_TYPE = os.getenv("DB_TYPE", "sqlite")  # sqlite or postgresql
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "mlflow")
DB_USER = os.getenv("DB_USER", "mlflow")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")


def get_tracking_uri() -> str:
    """Get MLflow tracking URI based on database type."""
    if DB_TYPE == "postgresql":
        return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return MLFLOW_TRACKING_URI


def get_artifact_root() -> str:
    """Get artifact storage root path."""
    artifact_path = Path(MLFLOW_ARTIFACT_ROOT)
    artifact_path.mkdir(parents=True, exist_ok=True)
    return str(artifact_path)


def get_backend_store() -> str:
    """Get backend store path."""
    backend_path = Path(MLFLOW_BACKEND_STORE)
    backend_path.mkdir(parents=True, exist_ok=True)
    return str(backend_path)
