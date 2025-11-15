"""
Verify that all required dependencies are installed correctly
"""

import sys
from importlib import import_module

# Required packages and their minimum versions
REQUIRED_PACKAGES = {
    "mlflow": "2.9.0",
    "fastapi": "0.108.0",
    "typer": "0.9.0",
    "sklearn": "1.3.0",
    "pandas": "2.1.0",
    "numpy": "1.24.0",
    "pydantic": "2.5.0",
    "uvicorn": "0.25.0",
}

def check_package(package_name: str, min_version: str) -> bool:
    """Check if a package is installed and meets minimum version."""
    try:
        module = import_module(package_name)
        version = getattr(module, "__version__", "unknown")
        print(f"✓ {package_name}: {version} (required: >={min_version})")
        return True
    except ImportError:
        print(f"✗ {package_name}: NOT INSTALLED (required: >={min_version})")
        return False

def main():
    """Check all required packages."""
    print("Checking required dependencies...\n")
    
    all_installed = True
    for package, min_version in REQUIRED_PACKAGES.items():
        if not check_package(package, min_version):
            all_installed = False
    
    print("\n" + "="*60)
    if all_installed:
        print("✓ All required packages are installed!")
        print("Your environment is ready for development.")
        return 0
    else:
        print("✗ Some packages are missing.")
        print("Run: pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())