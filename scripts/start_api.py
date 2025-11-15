"""
Start FastAPI Inference Service

Launch the model inference API server.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Also set PYTHONPATH environment variable
os.environ['PYTHONPATH'] = str(project_root)


def main():
    """Start the FastAPI server."""
    import uvicorn
    
    print("="*60)
    print("Starting FastAPI Inference Service")
    print("="*60)
    print("\nEndpoints:")
    print("  - API Docs: http://127.0.0.1:8000/docs")
    print("  - Health: http://127.0.0.1:8000/health/health")
    print("  - Models: http://127.0.0.1:8000/models/")
    print("  - Predict: http://127.0.0.1:8000/predict/")
    print("\nPress Ctrl+C to stop")
    print("="*60)
    print()
    
    from config.settings import API_HOST, API_PORT, API_RELOAD
    
    uvicorn.run(
        "api.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=API_RELOAD,
    )


if __name__ == "__main__":
    main()