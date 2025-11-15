"""
Initialize MLflow database and directory structure

This script sets up:
- SQLite database for backend store
- Artifact storage directories
- Default experiment
"""

import os
import sys
from pathlib import Path

import mlflow
from mlflow.tracking import MlflowClient

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.settings import (
    get_tracking_uri,
    get_artifact_root,
    get_backend_store,
    DEFAULT_EXPERIMENT_NAME,
    PROJECT_ROOT,
)


def create_directories():
    """Create necessary directories for MLflow."""
    directories = [
        PROJECT_ROOT / "data",
        PROJECT_ROOT / "data" / "mlruns",
        PROJECT_ROOT / "data" / "mlartifacts",
        PROJECT_ROOT / "data" / "models",
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")


def initialize_mlflow():
    """Initialize MLflow tracking server."""
    from pathlib import Path
    
    tracking_uri = get_tracking_uri()
    artifact_root = get_artifact_root()
    
    # Set tracking URI
    mlflow.set_tracking_uri(tracking_uri)
    print(f"✓ MLflow tracking URI set to: {tracking_uri}")
    
    # Create MLflow client
    client = MlflowClient(tracking_uri=tracking_uri)
    
    # Create default experiment if it doesn't exist
    try:
        experiment = client.get_experiment_by_name(DEFAULT_EXPERIMENT_NAME)
        if experiment is None:
            # Create proper file URI for artifact location
            if artifact_root.startswith('file://'):
                artifact_root_path = artifact_root[7:]
                # Handle Windows paths like /C:/Users/...
                if artifact_root_path.startswith('/') and ':' in artifact_root_path:
                    artifact_root_path = artifact_root_path[1:]
            else:
                artifact_root_path = artifact_root
            
            # Create absolute path and convert to URI
            artifact_location = (Path(artifact_root_path) / DEFAULT_EXPERIMENT_NAME).resolve().as_uri()
            
            experiment_id = client.create_experiment(
                name=DEFAULT_EXPERIMENT_NAME,
                artifact_location=artifact_location
            )
            print(f"✓ Created default experiment: {DEFAULT_EXPERIMENT_NAME} (ID: {experiment_id})")
        else:
            print(f"✓ Default experiment already exists: {DEFAULT_EXPERIMENT_NAME}")
    except Exception as e:
        print(f"✗ Error creating experiment: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def verify_setup():
    """Verify MLflow setup is working."""
    try:
        client = MlflowClient()
        experiments = client.search_experiments()
        
        print("\n" + "="*60)
        print("MLflow Setup Verification")
        print("="*60)
        print(f"Tracking URI: {mlflow.get_tracking_uri()}")
        print(f"Artifact Root: {get_artifact_root()}")
        print(f"\nExperiments found: {len(experiments)}")
        
        for exp in experiments:
            print(f"  - {exp.name} (ID: {exp.experiment_id})")
        
        print("="*60)
        print("✓ MLflow is configured correctly!")
        return True
        
    except Exception as e:
        print(f"✗ Verification failed: {e}")
        return False


def main():
    """Main initialization function."""
    print("Initializing MLflow Model Registry...\n")
    
    # Step 1: Create directories
    print("Step 1: Creating directories...")
    create_directories()
    
    # Step 2: Initialize MLflow
    print("\nStep 2: Initializing MLflow...")
    if not initialize_mlflow():
        print("✗ Failed to initialize MLflow")
        return 1
    
    # Step 3: Verify setup
    print("\nStep 3: Verifying setup...")
    if not verify_setup():
        print("✗ Setup verification failed")
        return 1
    
    print("\n✓ MLflow Model Registry initialized successfully!")
    print("\nNext steps:")
    print("  1. Start MLflow UI: python scripts/start_mlflow.py")
    print("  2. Train a model: python workflows/training/sample_model.py")
    print("  3. View in browser: http://localhost:5000")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())