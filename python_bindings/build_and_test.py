#!/usr/bin/env python3
"""
Automated build and test script for ORCA Python bindings
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """Run a command and return the result"""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=check, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return None

def check_dependencies():
    """Check if required dependencies are installed"""
    print("Checking dependencies...")
    
    # Check Python packages
    required_packages = ['pybind11', 'setuptools', 'wheel']
    missing_packages = []
    
    for package in required_packages:
        result = run_command(f"python -c \"import {package}\"", check=False)
        if result is None or result.returncode != 0:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing packages: {missing_packages}")
        print("Install with: pip install " + " ".join(missing_packages))
        return False
    
    print("✓ All Python dependencies found")
    return True

def build_bindings():
    """Build the Python bindings"""
    print("\nBuilding Python bindings...")
    
    # Change to bindings directory
    bindings_dir = Path(__file__).parent
    
    # Clean previous builds
    build_dirs = ['build', 'dist', '*.egg-info']
    for pattern in build_dirs:
        run_command(f"rm -rf {pattern}", cwd=bindings_dir, check=False)
    
    # Build with pip
    result = run_command("pip install -e .", cwd=bindings_dir)
    
    if result and result.returncode == 0:
        print("✓ Build completed successfully")
        return True
    else:
        print("✗ Build failed")
        return False

def test_bindings():
    """Test the built bindings"""
    print("\nTesting bindings...")
    
    # Test basic import
    result = run_command("python -c \"import orca_core; print('Import successful')\"")
    if not result or result.returncode != 0:
        print("✗ Basic import test failed")
        return False
    
    print("✓ Basic import test passed")
    
    # Run example scripts
    examples_dir = Path(__file__).parent / "examples"
    
    # Test configuration system
    config_test = examples_dir / "config_test.py"
    if config_test.exists():
        result = run_command(f"python {config_test}")
        if not result or result.returncode != 0:
            print("✗ Configuration test failed")
            return False
        print("✓ Configuration test passed")
    
    # Test basic usage
    basic_test = examples_dir / "basic_usage.py"
    if basic_test.exists():
        result = run_command(f"python {basic_test}")
        if not result or result.returncode != 0:
            print("✗ Basic usage test failed")
            return False
        print("✓ Basic usage test passed")
    
    return True

def show_config_info():
    """Show current configuration information"""
    print("\nCurrent Configuration:")
    print("-" * 25)
    
    config_path = Path(__file__).parent / "config.json"
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        for module_name, module_config in config.get('modules', {}).items():
            status = "ENABLED" if module_config.get('enabled', False) else "DISABLED"
            print(f"  {module_name}: {status}")
    except Exception as e:
        print(f"Could not read config: {e}")

def main():
    """Main build and test function"""
    print("ORCA Python Bindings - Build and Test")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        print("\n✗ Dependency check failed")
        return 1
    
    # Show current configuration
    show_config_info()
    
    # Build bindings
    if not build_bindings():
        print("\n✗ Build failed")
        return 1
    
    # Test bindings
    if not test_bindings():
        print("\n✗ Tests failed")
        return 1
    
    print("\n" + "=" * 40)
    print("✓ All tests passed successfully!")
    print("\nYou can now use the ORCA Python bindings:")
    print("  import orca_core")
    print("  print(orca_core.get_enabled_modules())")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())