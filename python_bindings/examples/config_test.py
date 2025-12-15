#!/usr/bin/env python3
"""
Test script to verify configuration system works
"""

import json
import os
import sys

def test_config_system():
    """Test the dynamic configuration system"""
    
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    
    print("Configuration System Test")
    print("=" * 30)
    
    # Read current config
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        print("✓ Successfully read config.json")
    except Exception as e:
        print(f"✗ Failed to read config: {e}")
        return False
    
    # Display current configuration
    print("\nCurrent module configuration:")
    for module_name, module_config in config.get('modules', {}).items():
        status = "ENABLED" if module_config.get('enabled', False) else "DISABLED"
        print(f"  {module_name}: {status}")
        if module_config.get('description'):
            print(f"    Description: {module_config['description']}")
        if module_config.get('classes'):
            print(f"    Classes: {', '.join(module_config['classes'])}")
    
    # Test configuration modification
    print("\nTesting configuration modification...")
    
    # Create backup
    backup_config = config.copy()
    
    # Modify experimental module
    if 'experimental' in config['modules']:
        original_state = config['modules']['experimental']['enabled']
        config['modules']['experimental']['enabled'] = not original_state
        
        # Write modified config
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✓ Modified experimental module: {original_state} -> {not original_state}")
        except Exception as e:
            print(f"✗ Failed to write config: {e}")
            return False
        
        # Restore original config
        try:
            with open(config_path, 'w') as f:
                json.dump(backup_config, f, indent=2)
            print("✓ Restored original configuration")
        except Exception as e:
            print(f"✗ Failed to restore config: {e}")
            return False
    
    print("\n✓ Configuration system test completed successfully!")
    return True

def show_usage_instructions():
    """Show instructions for using the configuration system"""
    
    print("\nConfiguration Usage Instructions:")
    print("-" * 35)
    print("1. Edit config.json to enable/disable modules")
    print("2. Set 'enabled': true/false for each module")
    print("3. Recompile with: pip install -e .")
    print("4. Import and test: import orca_core")
    print()
    print("Example workflow:")
    print("  # Enable experimental features")
    print("  # Edit config.json: 'experimental': {'enabled': true}")
    print("  # Recompile: pip install -e .")
    print("  # Test: python examples/basic_usage.py")

if __name__ == "__main__":
    success = test_config_system()
    show_usage_instructions()
    
    if not success:
        sys.exit(1)