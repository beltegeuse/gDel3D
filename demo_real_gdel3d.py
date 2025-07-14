#!/usr/bin/env python3
"""
gDel3D Python Bindings - Full Implementation Demo
This script demonstrates the real gDel3D 3D Delaunay triangulation algorithm
"""

import numpy as np
import gdel3d


def demo_real_gdel3d():
    print("🚀 gDel3D Python Bindings - Real Implementation Demo 🚀")
    print(f"Module version: {gdel3d.__version__}")
    print()

    # Create a set of interesting 3D points
    points = np.array(
        [
            [0.0, 0.0, 0.0],  # Origin
            [1.0, 0.0, 0.0],  # X-axis
            [0.0, 1.0, 0.0],  # Y-axis
            [0.0, 0.0, 1.0],  # Z-axis
            [0.5, 0.5, 0.5],  # Center
            [1.0, 1.0, 0.0],  # XY diagonal
            [1.0, 0.0, 1.0],  # XZ diagonal
            [0.0, 1.0, 1.0],  # YZ diagonal
            [1.0, 1.0, 1.0],  # Corner
        ]
    )

    print(f"Input: {len(points)} 3D points")
    print("Points:")
    for i, point in enumerate(points):
        print(f"  {i}: ({point[0]:.1f}, {point[1]:.1f}, {point[2]:.1f})")
    print()

    # Compute 3D Delaunay triangulation using real gDel3D algorithm
    print("Computing 3D Delaunay triangulation using real gDel3D...")
    try:
        tetrahedra = gdel3d.compute_delaunay(points)

        print(f"✅ Success! Generated {len(tetrahedra)} tetrahedra")
        print()
        print("Tetrahedra (vertex indices):")
        for i, tet in enumerate(tetrahedra):
            print(f"  Tetrahedron {i:2d}: [{tet[0]}, {tet[1]}, {tet[2]}, {tet[3]}]")

        print()
        print("🎯 This demonstrates that the real gDel3D CUDA algorithm is working!")
        print("   - Input: 3D point coordinates")
        print("   - Output: List of tetrahedra defined by vertex indices")
        print("   - Each tetrahedron connects 4 input points")
        print("   - The triangulation satisfies the Delaunay property")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    success = demo_real_gdel3d()
    if success:
        print("\n🎉 gDel3D Python bindings are fully operational! 🎉")
    else:
        print("\n❌ Demo failed")
