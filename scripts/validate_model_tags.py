"""
Validate Model Tags

Checks if required tags are present on models.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from registry.core.model_manager import ModelManager
from registry.validation.validators import ModelValidator
from config.settings import REQUIRED_TAGS


def main():
    """Validate model tags."""
    print("Validating model tags...")
    
    manager = ModelManager()
    validator = ModelValidator()
    
    # Get latest model version
    versions = manager.list_model_versions("sample_classifier")
    
    if not versions:
        print("No models found to validate")
        return 1
    
    latest_version = versions[0]
    tags = latest_version.tags or {}
    
    # Validate tags
    if not validator.validate_required_tags(tags, REQUIRED_TAGS):
        print(f"❌ Missing required tags: {REQUIRED_TAGS}")
        return 1
    
    print(f"✅ Tag validation passed!")
    print(f"   Tags: {tags}")
    return 0


if __name__ == "__main__":
    sys.exit(main())