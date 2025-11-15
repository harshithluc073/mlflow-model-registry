"""
Sample Model Training Script

Demonstrates how to train a model and log it to MLflow registry.
"""

import sys
from pathlib import Path
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from registry.core.experiment_tracker import ExperimentTracker
from registry.core.model_manager import ModelManager
from config.settings import STAGE_DEV


def generate_sample_data(n_samples=1000, n_features=20, random_state=42):
    """Generate sample classification dataset."""
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=15,
        n_redundant=5,
        n_classes=2,
        random_state=random_state,
    )
    
    return train_test_split(X, y, test_size=0.2, random_state=random_state)


def train_model(
    n_estimators=100,
    max_depth=10,
    min_samples_split=2,
    random_state=42,
):
    """
    Train a Random Forest classifier and log to MLflow.
    
    Args:
        n_estimators: Number of trees
        max_depth: Maximum tree depth
        min_samples_split: Minimum samples to split
        random_state: Random seed
        
    Returns:
        Trained model and metrics
    """
    print("="*60)
    print("Training Sample Model")
    print("="*60)
    
    # Initialize tracker
    tracker = ExperimentTracker(experiment_name="sample_models")
    
    # Generate data
    print("\n1. Generating sample data...")
    X_train, X_test, y_train, y_test = generate_sample_data(
        n_samples=1000,
        n_features=20,
        random_state=random_state,
    )
    print(f"   Train samples: {len(X_train)}")
    print(f"   Test samples: {len(X_test)}")
    
    # Start MLflow run
    print("\n2. Starting MLflow run...")
    with tracker.start_run(run_name="random_forest_classifier") as run:
        
        # Log parameters
        print("\n3. Logging parameters...")
        params = {
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "min_samples_split": min_samples_split,
            "random_state": random_state,
        }
        tracker.log_params(params)
        
        # Log tags
        tracker.set_tags({
            "model_type": "RandomForest",
            "framework": "scikit-learn",
            "created_by": "sample_training_script",
            "task": "classification",
        })
        
        # Train model
        print("\n4. Training model...")
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            random_state=random_state,
        )
        model.fit(X_train, y_train)
        
        # Make predictions
        print("\n5. Evaluating model...")
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1_score": f1_score(y_test, y_pred, zero_division=0),
        }
        
        # Log metrics
        print("\n6. Logging metrics...")
        tracker.log_metrics(metrics)
        
        for metric_name, metric_value in metrics.items():
            print(f"   {metric_name}: {metric_value:.4f}")
        
        # Log model
        print("\n7. Logging model to MLflow...")
        tracker.log_model(
            model=model,
            artifact_path="model",
            registered_model_name="sample_classifier",
        )
        
        run_id = run.info.run_id
        print(f"\n✓ Run completed: {run_id}")
        
        return model, metrics, run_id


def register_and_stage_model(run_id: str):
    """
    Register model and set to None (Development) stage.
    
    Args:
        run_id: MLflow run ID
    """
    print("\n" + "="*60)
    print("Registering Model")
    print("="*60)
    
    model_manager = ModelManager()
    
    # The model is already registered during training
    # Now we'll transition it to None (Development) stage
    
    # Get the latest version
    versions = model_manager.list_model_versions("sample_classifier")
    if versions:
        latest_version = versions[0].version
        
        print(f"\n1. Setting model version {latest_version} to None (Development) stage...")
        model_manager.transition_stage(
            model_name="sample_classifier",
            version=latest_version,
            stage=STAGE_DEV,  # This is "None"
            archive_existing=False,
        )
        
        print(f"✓ Model registered and staged: sample_classifier v{latest_version}")
        return latest_version
    
    return None


def main():
    """Main training workflow."""
    print("\n" + "="*60)
    print("MLflow Model Training Demo")
    print("="*60)
    
    try:
        # Train model
        model, metrics, run_id = train_model(
            n_estimators=100,
            max_depth=10,
            min_samples_split=2,
        )
        
        # Register and stage
        version = register_and_stage_model(run_id)
        
        print("\n" + "="*60)
        print("Training Complete!")
        print("="*60)
        print(f"\nRun ID: {run_id}")
        print(f"Model: sample_classifier")
        print(f"Version: {version}")
        print(f"Stage: None (Development)")
        print(f"\nAccuracy: {metrics['accuracy']:.4f}")
        print("\nNext steps:")
        print("  1. View in MLflow UI: http://localhost:5000")
        print("  2. Promote to Staging: mlflow-registry promote staging sample_classifier 1")
        print("  3. Use CLI: mlflow-registry list models")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())