"""
Test FastAPI Application

Quick test to verify API is working.
"""

import sys
import os
from pathlib import Path

# Get absolute project root path
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent

# Add to Python path at the beginning
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Set PYTHONPATH environment variable
os.environ['PYTHONPATH'] = str(project_root)

# Change to project directory
os.chdir(project_root)


def test_import():
    """Test if all imports work."""
    print("Testing API imports...")
    print(f"Project root: {project_root}")
    print(f"Current directory: {os.getcwd()}")
    print()
    
    # Verify api directory is accessible
    api_dir = project_root / 'api'
    if not api_dir.exists():
        print(f"❌ API directory not found at: {api_dir}")
        return False
    
    # Check if key files exist
    files_to_check = [
        'api/main.py',
        'api/routers/health.py',
        'api/routers/models.py',
        'api/routers/inference.py',
        'api/schemas/prediction.py',
        'api/schemas/model_info.py',
        'api/services/model_service.py',
    ]
    
    print("Checking file existence:")
    all_exist = True
    for file_path in files_to_check:
        exists = (project_root / file_path).exists()
        status = "✓" if exists else "✗"
        print(f"  {status} {file_path}")
        if not exists:
            all_exist = False
    
    if not all_exist:
        print("\n❌ Some required files are missing!")
        return False
    
    print("\nAttempting imports...")
    
    try:
        print("\n1. Testing main app import...")
        import api.main
        print("   ✓ api.main module imported")
        from api.main import app
        print("   ✓ FastAPI app instance imported")
        
        print("\n2. Testing router imports...")
        import api.routers.health as health_router
        print("   ✓ health router imported")
        import api.routers.models as models_router
        print("   ✓ models router imported")
        import api.routers.inference as inference_router
        print("   ✓ inference router imported")
        
        print("\n3. Testing schema imports...")
        import api.schemas.prediction as prediction_schema
        print("   ✓ prediction schemas imported")
        import api.schemas.model_info as model_info_schema
        print("   ✓ model_info schemas imported")
        
        print("\n4. Testing service imports...")
        import api.services.model_service as model_service_module
        print("   ✓ model_service module imported")
        
        print("\n5. Testing FastAPI app structure...")
        print(f"   App title: {app.title}")
        print(f"   App version: {app.version}")
        print(f"   Number of routes: {len(app.routes)}")
        
        # Check routers are registered
        route_paths = [route.path for route in app.routes]
        print(f"   Route paths: {route_paths[:5]}...")
        
        print("\n" + "="*60)
        print("✅ All API components imported successfully!")
        print("="*60)
        print("\nYou can now start the API with:")
        print("  uvicorn api.main:app --reload")
        print("\nOr from any directory:")
        print(f"  cd {project_root}")
        print("  uvicorn api.main:app --reload")
        print("="*60)
        return True
        
    except ImportError as e:
        print(f"\n❌ Import failed: {e}")
        print(f"\nPython is looking in these paths:")
        for i, path in enumerate(sys.path[:10], 1):
            print(f"  {i}. {path}")
        print("\nDebug info:")
        print(f"  Working directory: {os.getcwd()}")
        print(f"  Project root: {project_root}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_import()
    
    if not success:
        print("\n" + "="*60)
        print("TROUBLESHOOTING")
        print("="*60)
        print("\nIf imports fail but files exist, try:")
        print("1. Make sure you're in the project root:")
        print(f"   cd {project_root}")
        print("\n2. Check virtual environment is activated:")
        print("   .\\venv\\Scripts\\activate")
        print("\n3. Start API directly (bypasses test):")
        print("   uvicorn api.main:app --reload")
        print("="*60)
    
    sys.exit(0 if success else 1)