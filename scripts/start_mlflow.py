"""
Start MLflow Tracking Server

This script starts the MLflow UI server with configured backend and artifact stores.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.settings import (
    get_tracking_uri,
    get_artifact_root,
    get_backend_store,
)


def start_mlflow_server(host="127.0.0.1", port=5000):
    """
    Start MLflow tracking server.
    
    Args:
        host: Host address to bind to
        port: Port number to use
    """
    backend_store = get_backend_store()
    artifact_root = get_artifact_root()
    
    # Ensure directories exist
    Path(backend_store).mkdir(parents=True, exist_ok=True)
    
    # Extract path from file:// URI if present
    if artifact_root.startswith('file://'):
        artifact_path = artifact_root[7:]  # Remove file://
        if artifact_path.startswith('/') and ':' in artifact_path:
            # Windows path like /C:/Users/...
            artifact_path = artifact_path[1:]  # Remove leading /
    else:
        artifact_path = artifact_root
    
    Path(artifact_path).mkdir(parents=True, exist_ok=True)
    
    print("="*60)
    print("Starting MLflow Tracking Server")
    print("="*60)
    print(f"Backend Store: {backend_store}")
    print(f"Artifact Root: {artifact_root}")
    print(f"Server URL: http://{host}:{port}")
    print("="*60)
    print("\nPress Ctrl+C to stop the server\n")
    
    # Build command - use the actual path for artifact root, not URI
    cmd = [
        "mlflow",
        "server",
        "--backend-store-uri", f"file:///{backend_store}",
        "--default-artifact-root", artifact_path,  # Use path, not URI
        "--host", host,
        "--port", str(port),
    ]
    
    try:
        # Start server
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n\n✓ MLflow server stopped")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error starting MLflow server: {e}")
        return 1
    except FileNotFoundError:
        print("\n✗ MLflow not found. Please install it: pip install mlflow")
        return 1
    
    return 0


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Start MLflow Tracking Server")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host address (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port number (default: 5000)"
    )
    
    args = parser.parse_args()
    
    return start_mlflow_server(host=args.host, port=args.port)


if __name__ == "__main__":
    sys.exit(main())