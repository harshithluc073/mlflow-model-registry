"""
Test FastAPI Application

Quick test to verify API is working.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_import():
    """Test if all imports work."""
    print("Testing API imports...")
    
    try:
        from api.main import app
        print("✓ Main app imported successfully")
        
        from api.routers import health, models, inference
        print("✓ Routers imported successfully")
        
        from api.schemas import prediction, model_info
        print("✓ Schemas imported successfully")
        
        from api.services.model_service import model_service
        print("✓ Model service imported successfully")
        
        print("\n✅ All API components imported successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_import()
    sys.exit(0 if success else 1)