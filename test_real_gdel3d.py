#!/usr/bin/env python3
"""
Test script for real gDel3D implementation
Tests both API interfaces with actual 3D Delaunay triangulation computation
"""

import numpy as np
import gdel3d

def test_simple_tetrahedron():
    """Test with a simple 4-point tetrahedron"""
    print("=== Testing Simple Tetrahedron ===")
    
    # Define 4 points forming a simple tetrahedron
    points = np.array([
        [0.0, 0.0, 0.0],  # Point 0
        [1.0, 0.0, 0.0],  # Point 1  
        [0.5, 1.0, 0.0],  # Point 2
        [0.5, 0.5, 1.0]   # Point 3
    ])
    
    print(f"Input points shape: {points.shape}")
    print(f"Points:\n{points}")
    
    try:
        # Test numpy interface
        result = gdel3d.compute_delaunay(points)
        print(f"✅ Numpy interface success!")
        print(f"Number of tetrahedra: {len(result)}")
        for i, tet in enumerate(result):
            print(f"  Tetrahedron {i}: {tet}")
            
        # Test list interface
        points_list = [tuple(point) for point in points]
        result_list = gdel3d.compute_delaunay_from_list(points_list)
        print(f"✅ List interface success!")
        print(f"Number of tetrahedra (list): {len(result_list)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_cube_points():
    """Test with 8 points forming a cube"""
    print("\n=== Testing Cube Points ===")
    
    # Define 8 corner points of a unit cube
    points = np.array([
        [0.0, 0.0, 0.0],  # 0
        [1.0, 0.0, 0.0],  # 1
        [1.0, 1.0, 0.0],  # 2
        [0.0, 1.0, 0.0],  # 3
        [0.0, 0.0, 1.0],  # 4
        [1.0, 0.0, 1.0],  # 5
        [1.0, 1.0, 1.0],  # 6
        [0.0, 1.0, 1.0]   # 7
    ])
    
    print(f"Input points shape: {points.shape}")
    
    try:
        result = gdel3d.compute_delaunay(points)
        print(f"✅ Cube triangulation success!")
        print(f"Number of tetrahedra: {len(result)}")
        
        # A cube should typically be divided into 5 or 6 tetrahedra
        print("Tetrahedra:")
        for i, tet in enumerate(result):
            print(f"  {i}: {tet}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_random_points():
    """Test with random 3D points"""
    print("\n=== Testing Random Points ===")
    
    np.random.seed(42)  # For reproducible results
    num_points = 20
    points = np.random.rand(num_points, 3) * 10.0  # Random points in [0,10]^3
    
    print(f"Input: {num_points} random points")
    
    try:
        result = gdel3d.compute_delaunay(points)
        print(f"✅ Random points triangulation success!")
        print(f"Number of tetrahedra: {len(result)}")
        
        # Verify all tetrahedra have 4 vertices
        all_valid = True
        for i, tet in enumerate(result):
            if len(tet) != 4:
                print(f"❌ Invalid tetrahedron {i}: {tet}")
                all_valid = False
            elif min(tet) < 0 or max(tet) >= num_points:
                print(f"❌ Invalid vertex indices in tetrahedron {i}: {tet}")
                all_valid = False
                
        if all_valid:
            print("✅ All tetrahedra have valid vertex indices")
            
        return all_valid
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_error_cases():
    """Test error handling"""
    print("\n=== Testing Error Cases ===")
    
    try:
        # Test with too few points
        points = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]])  # Only 3 points
        try:
            result = gdel3d.compute_delaunay(points)
            print("❌ Should have failed with too few points")
            return False
        except RuntimeError as e:
            print(f"✅ Correctly caught error for too few points: {e}")
            
        # Test with wrong shape
        points = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])  # 2D points
        try:
            result = gdel3d.compute_delaunay(points)
            print("❌ Should have failed with wrong shape")
            return False
        except RuntimeError as e:
            print(f"✅ Correctly caught error for wrong shape: {e}")
            
        return True
        
    except Exception as e:
        print(f"❌ Unexpected error in error testing: {e}")
        return False

def main():
    print("🚀 Testing Real gDel3D Implementation 🚀")
    print(f"Module version: {gdel3d.__version__}")
    
    tests = [
        test_simple_tetrahedron,
        test_cube_points, 
        test_random_points,
        test_error_cases
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    print(f"\n📊 Summary: {sum(results)}/{len(results)} tests passed")
    
    if all(results):
        print("🎉 ALL TESTS PASSED! Real gDel3D implementation is working! 🎉")
    else:
        print("⚠️  Some tests failed - check implementation")
        
    return all(results)

if __name__ == "__main__":
    main()
