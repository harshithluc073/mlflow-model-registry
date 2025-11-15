"""
FastAPI Application - MLflow Model Inference Service

Production-ready API for serving ML models from the registry.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import routers directly
from api.routers.inference import router as inference_router
from api.routers.models import router as models_router
from api.routers.health import router as health_router

from config.settings import API_HOST, API_PORT, API_RELOAD
from registry.utils.logging_utils import setup_logger

logger = setup_logger(__name__)


# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    logger.info("Starting MLflow Model Inference API")
    logger.info(f"API Server: http://{API_HOST}:{API_PORT}")
    logger.info(f"API Docs: http://{API_HOST}:{API_PORT}/docs")
    yield
    # Shutdown
    logger.info("Shutting down MLflow Model Inference API")


# Create FastAPI app
app = FastAPI(
    title="MLflow Model Registry API",
    description="Production-ready inference API for MLflow registered models",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(health_router, tags=["Health"])
app.include_router(models_router, prefix="/models", tags=["Models"])
app.include_router(inference_router, prefix="/predict", tags=["Inference"])


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle uncaught exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
        },
    )


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "MLflow Model Registry API",
        "version": "0.1.0",
        "status": "running",
        "docs": f"http://{API_HOST}:{API_PORT}/docs",
    }


def main():
    """Run the API server."""
    uvicorn.run(
        "api.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=API_RELOAD,
        log_level="info",
    )


if __name__ == "__main__":
    main()