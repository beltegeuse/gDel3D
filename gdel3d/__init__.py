"""
gDel3D Python Package
Python bindings for 3D Delaunay triangulation using CUDA
"""

import sys
from pathlib import Path
import importlib.util

__version__ = "0.3.0"


# Try to import the compiled module
def _load_native_module():
    """Load the native gDel3D module"""
    # Search for the compiled module
    package_dir = Path(__file__).parent
    parent_dir = Path(__file__).parent.parent

    # Look for renamed module in package directory first
    renamed_module = (
        package_dir / f"_gdel3d_core.cpython-{sys.version_info.major}{sys.version_info.minor}-x86_64-linux-gnu.so"
    )
    if renamed_module.exists():
        spec = importlib.util.spec_from_file_location("gdel3d", renamed_module)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module

    # Look for original module in parent directory
    orig_modules = list(parent_dir.glob(f"gdel3d.cpython-{sys.version_info.major}{sys.version_info.minor}-*.so"))
    if orig_modules:
        spec = importlib.util.spec_from_file_location("gdel3d", orig_modules[0])
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module

    raise ImportError(
        f"Could not find gDel3D compiled module for Python {sys.version_info.major}.{sys.version_info.minor}"
    )


try:
    _native_module = _load_native_module()

    # Export the main functions
    compute_delaunay = _native_module.compute_delaunay
    compute_delaunay_from_list = _native_module.compute_delaunay_from_list

    # Update version if available
    if hasattr(_native_module, "__version__"):
        __version__ = _native_module.__version__

except ImportError as e:
    raise ImportError(f"Failed to load gDel3D compiled module: {e}")

__all__ = ["compute_delaunay", "compute_delaunay_from_list", "__version__"]
