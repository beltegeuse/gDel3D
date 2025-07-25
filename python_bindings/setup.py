from pybind11.setup_helpers import build_ext
from setuptools import setup, Extension
import subprocess
import shutil
import sys
from pathlib import Path


class CMakeBuildExt(build_ext):
    """Custom build extension that uses CMake to build CUDA code"""

    def build_extension(self, ext):
        # Create build directory
        build_dir = Path(self.build_temp).resolve()
        build_dir.mkdir(parents=True, exist_ok=True)

        # Configure CMake
        cmake_configure_cmd = [
            "cmake",
            str(Path.cwd()),  # Source directory
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={str(Path(self.build_lib).resolve())}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            "-DCMAKE_BUILD_TYPE=Release",
        ]

        # Build with CMake
        cmake_build_cmd = ["cmake", "--build", ".", "--config", "Release", "--", "-j4"]

        print(f"Building in {build_dir}")
        print(f"CMake configure: {' '.join(cmake_configure_cmd)}")

        # Run CMake configure
        subprocess.check_call(cmake_configure_cmd, cwd=build_dir)

        # Run CMake build
        print(f"CMake build: {' '.join(cmake_build_cmd)}")
        subprocess.check_call(cmake_build_cmd, cwd=build_dir)

        # Find the built module and copy it to the correct location
        built_lib = None
        for ext_suffix in [".so", ".pyd", ".dll"]:
            potential_lib = build_dir / f"pygdel3d{ext_suffix}"
            if potential_lib.exists():
                built_lib = potential_lib
                break

        if built_lib:
            # Copy to build_lib directory
            target_dir = Path(self.build_lib)
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(built_lib, target_dir / built_lib.name)
            print(f"Copied {built_lib} to {target_dir}")
        else:
            print("Warning: Could not find built library")


# Dummy extension - actual building is done by CMake
ext_modules = [
    Extension(
        "pygdel3d",
        sources=[],  # Empty - CMake handles the real sources
    )
]

setup(
    name="pygdel3d",
    version="1.0.0",
    description="Python bindings for gDel3D GPU-based 3D Delaunay triangulation",
    ext_modules=ext_modules,
    cmdclass={"build_ext": CMakeBuildExt},
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.19.0",
    ],
)
