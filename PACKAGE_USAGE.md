# gDel3D Python Package

A Python package for 3D Delaunay triangulation using CUDA acceleration.

## Installation

### Option 1: Development Install (Recommended for active development)
```bash
cd /path/to/gDel3D
pip install -e .
```

### Option 2: Install from Wheel
```bash
pip install /path/to/gDel3D/dist/gdel3d-0.3.0-py3-none-any.whl
```

### Option 3: Standard Install
```bash
cd /path/to/gDel3D
pip install .
```

## Usage

```python
import numpy as np
import gdel3d

# Create some 3D points
points = np.array([
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [0.5, 1.0, 0.0],
    [0.5, 0.5, 1.0]
])

# Compute Delaunay tetrahedralization
tetrahedra = gdel3d.compute_delaunay(points)
print(f"Generated {len(tetrahedra)} tetrahedra")

# Alternative: use list of tuples
points_list = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.5, 1.0, 0.0), (0.5, 0.5, 1.0)]
tetrahedra = gdel3d.compute_delaunay_from_list(points_list)
```

## Requirements

- Python 3.8+
- NumPy >= 1.19.0
- CUDA-capable GPU (for optimal performance)

## Notes

- The package is built for Python 3.12 and works on Linux systems
- Each tetrahedron is represented as a list of 4 vertex indices
- Input points should be 3D coordinates as NumPy arrays or lists of tuples
- The underlying implementation uses CUDA for GPU acceleration

## Functions

### `compute_delaunay(points)`
- **Input**: NumPy array of shape (N, 3) with 3D coordinates
- **Output**: List of tetrahedra, where each tetrahedron is a list of 4 vertex indices

### `compute_delaunay_from_list(points)`
- **Input**: List of tuples, where each tuple contains (x, y, z) coordinates
- **Output**: List of tetrahedra, where each tetrahedron is a list of 4 vertex indices
