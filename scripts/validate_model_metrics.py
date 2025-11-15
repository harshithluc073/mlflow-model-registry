"""
Validate Model Metrics

Checks if the latest model meets accuracy thresholds.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from registry.core.model_manager import ModelManager
from registry.validation.validators import ModelValidator
from config.settings import MIN_ACCURACY_THRESHOLD


def main():
    """Validate model metrics."""
    print("Validating model metrics...")
    
    manager = ModelManager()
    validator = ModelValidator()
    
    # Get latest model version
    versions = manager.list_model_versions("sample_classifier")
    
    if not versions:
        print("No models found to validate")
        return 1
    
    latest_version = versions[0]
    
    # Get run metrics
    run = manager.client.get_run(latest_version.run_id)
    metrics = run.data.metrics
    
    # Validate accuracy
    if not validator.validate_accuracy_threshold(metrics, MIN_ACCURACY_THRESHOLD):
        print(f"❌ Model accuracy below threshold: {MIN_ACCURACY_THRESHOLD}")
        return 1
    
    print(f"✅ Model validation passed!")
    print(f"   Accuracy: {metrics.get('accuracy', 0):.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())