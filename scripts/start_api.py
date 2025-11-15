"""
Start FastAPI Inference Service

Launch the model inference API server.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def main():
    """Start the FastAPI server."""
    from api.main import main as run_api
    
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
    
    run_api()


if __name__ == "__main__":
    main()