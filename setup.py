from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
import os
import shutil
import glob

# Read the README for long description
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Python bindings for gDel3D 3D Delaunay triangulation library"


def copy_compiled_module():
    """Copy the compiled module to the package directory"""
    # Find the compiled module
    module_files = glob.glob("gdel3d.cpython-*.so")
    if module_files:
        src_file = module_files[0]  # Take the first one found
        dst_file = os.path.join("gdel3d", os.path.basename(src_file))

        print(f"Copying {src_file} to {dst_file}")
        os.makedirs("gdel3d", exist_ok=True)
        shutil.copy2(src_file, dst_file)
        return True
    return False


class CustomInstall(install):
    def run(self):
        copy_compiled_module()
        super().run()


class CustomDevelop(develop):
    def run(self):
        copy_compiled_module()
        super().run()


setup(
    name="gdel3d",
    version="0.3.0",
    author="gDel3D Python Bindings",
    author_email="",
    description="Python bindings for gDel3D 3D Delaunay triangulation library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/beltegeuse/gDel3D",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.19.0",
    ],
    include_package_data=True,
    package_data={
        "gdel3d": ["*.so"],
    },
    cmdclass={
        "install": CustomInstall,
        "develop": CustomDevelop,
    },
    zip_safe=False,
)
