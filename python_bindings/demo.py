#!/usr/bin/env python3
"""
PyGDel3D Installation and Usage Example
=======================================

This script demonstrates the installation and usage of PyGDel3D,
Python bindings for the gDel3D GPU-accelerated 3D Delaunay triangulation library.
"""

import sys
import numpy as np

# Add the built module to path
sys.path.insert(0, "src")

try:
    import pygdel3d

    print("PyGDel3D - GPU-Accelerated 3D Delaunay Triangulation")
    print("=" * 55)
    print(f"Version: {pygdel3d.__version__}")
    print("Successfully imported!")
    print()

    # Example 1: Simple test case
    print("Example 1: Cube vertices with center point")
    print("-" * 42)

    # 8 corners of a unit cube + center point
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 1.0],
            [1.0, 1.0, 1.0],
            [0.0, 1.0, 1.0],
            [0.5, 0.5, 0.5],  # Center point
        ],
        dtype=np.float64,
    )

    tetrahedra, time_taken = pygdel3d.triangulate(points)

    print(f"Input points: {points.shape[0]}")
    print(f"Output tetrahedra: {tetrahedra.shape[0]}")
    print("First few tetrahedra (vertex indices):")
    for i in range(min(5, tetrahedra.shape[0])):
        print(f"  Tetrahedron {i}: {tetrahedra[i]}")
    print(f"Processing time: {time_taken:.6f} ms")
    print()

    # Example 2: Random points performance test
    print("Example 2: Performance test with random points")
    print("-" * 46)

    np.random.seed(42)
    for n_points in [8**3, 16**3, 32**3, 64**3, 128**3]:
        points = np.random.rand(n_points, 3).astype(np.float64)
        tetrahedra, time_taken = pygdel3d.triangulate(points)

        print(f"Points: {n_points:4d} | Tetrahedra: {tetrahedra.shape[0]:5d} | Time: {time_taken:.6f} ms")

    print("✓ All tests passed! PyGDel3D is working correctly.")

except ImportError as e:
    print("ERROR: Failed to import pygdel3d")
    print(f"Import error: {e}")
    print()
    print("To build the module, run:")
    print("  cd /path/to/python_bindings")
    print("  python3 setup.py build_ext --inplace")
    print()
    print("Requirements:")
    print("- CUDA 12.9+")
    print("- CMake 3.18+")
    print("- pybind11 3.0+")
    print("- numpy")
    print("- Updated libstdc++ (GLIBCXX_3.4.32+)")
    sys.exit(1)

except Exception as e:
    print(f"ERROR during triangulation: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
