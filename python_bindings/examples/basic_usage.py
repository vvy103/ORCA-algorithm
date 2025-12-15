#!/usr/bin/env python3
"""
ORCA Python Bindings - Basic Usage Example
"""

import sys
import os

# Add the parent directory to path to import orca_core
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    import orca_core
    print("✓ Successfully imported orca_core")
except ImportError as e:
    print(f"✗ Failed to import orca_core: {e}")
    print("Make sure you have compiled the bindings with: pip install -e .")
    sys.exit(1)

def main():
    print("ORCA Python Bindings - Basic Usage Example")
    print("=" * 50)
    
    # Check enabled modules
    print("Enabled modules:", orca_core.get_enabled_modules())
    print()
    
    # Test geometry functionality
    print("1. Testing Point class:")
    point1 = orca_core.Point(1.0, 2.0)
    point2 = orca_core.Point(3.0, 4.0)
    
    print(f"   Point 1: {point1}")
    print(f"   Point 2: {point2}")
    
    # Point operations
    diff = point2 - point1
    print(f"   Difference: {diff}")
    
    distance = diff.euclidean_norm()
    print(f"   Distance: {distance:.2f}")
    
    # Scalar operations
    scaled = point1 * 2.0
    print(f"   Point1 * 2: {scaled}")
    print()
    
    # Test Node class
    print("2. Testing Node class:")
    node1 = orca_core.Node(0, 0)
    node2 = orca_core.Node(5, 5)
    
    print(f"   Node 1: {node1}")
    print(f"   Node 2: {node2}")
    print(f"   Nodes equal: {node1 == node2}")
    print()
    
    # Test AgentParam
    print("3. Testing AgentParam:")
    params = orca_core.AgentParam()
    print(f"   Default radius: {params.radius}")
    print(f"   Default max_speed: {params.max_speed}")
    print(f"   Default sight_radius: {params.sight_radius}")
    
    # Modify parameters
    params.radius = 0.5
    params.max_speed = 2.0
    params.sight_radius = 5.0
    
    print(f"   Modified radius: {params.radius}")
    print(f"   Modified max_speed: {params.max_speed}")
    print(f"   Modified sight_radius: {params.sight_radius}")
    print()
    
    print("✓ All basic tests completed successfully!")
    print()
    print("Next steps:")
    print("- Create XML scenario files to test Mission functionality")
    print("- Implement concrete Agent classes for full simulation")
    print("- Add more geometry utilities as needed")

if __name__ == "__main__":
    main()