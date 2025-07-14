cmake_minimum_required(VERSION 3.18)

project(gDel3D_single LANGUAGES CXX CUDA)

set(CMAKE_BUILD_TYPE Release)

# Find Python and pybind11
find_package(Python COMPONENTS Interpreter Development REQUIRED)

# Add pybind11 CMake directory to the module path
list(APPEND CMAKE_PREFIX_PATH "/home/wylliam/dev/gDel3D/.venv/lib/python3.13/site-packages/pybind11/share/cmake/pybind11")
find_package(pybind11 REQUIRED)

# Set standards
set(CMAKE_CUDA_STANDARD 17)
set(CMAKE_CXX_STANDARD 17)

# Single compilation unit approach - include all sources in one .cu file
# This should resolve Thrust template instantiation issues

# Create the Python module with single unit approach
pybind11_add_module(gdel3d 
    python_bindings/single_unit.cu
    # Include all gDel3D sources directly - no separate compilation
    GDelFlipping/src/DelaunayChecker.cu
    GDelFlipping/src/InputCreator.cu
    GDelFlipping/src/RandGen.cpp
    GDelFlipping/src/gDel3D/GpuDelaunay.cu
    GDelFlipping/src/gDel3D/CPU/predicates.cpp
    GDelFlipping/src/gDel3D/CPU/PredWrapper.cu
    GDelFlipping/src/gDel3D/CPU/Splaying.cu
    GDelFlipping/src/gDel3D/CPU/Star.cu
    GDelFlipping/src/gDel3D/GPU/KerDivision.cu
    GDelFlipping/src/gDel3D/GPU/KerPredicates.cu
    GDelFlipping/src/gDel3D/GPU/ThrustWrapper.cu
)

# Set CUDA properties - single architecture, no separable compilation
set_target_properties(gdel3d PROPERTIES
    CUDA_SEPARABLE_COMPILATION OFF
    CUDA_ARCHITECTURES "86"
    CUDA_RESOLVE_DEVICE_SYMBOLS OFF
)

# Include directories
target_include_directories(gdel3d PRIVATE 
    ${CMAKE_CUDA_TOOLKIT_INCLUDE_DIRECTORIES}
    GDelFlipping/src
)

# Link CUDA libraries
find_package(CUDA REQUIRED)
target_link_libraries(gdel3d PRIVATE cudart)

# Disable LTO
set_target_properties(gdel3d PROPERTIES
    INTERPROCEDURAL_OPTIMIZATION FALSE
)

# Force consistent compilation flags
target_compile_definitions(gdel3d PRIVATE 
    VERSION_INFO=${EXAMPLE_VERSION_INFO}
    THRUST_DEVICE_SYSTEM=THRUST_DEVICE_SYSTEM_CUDA
)

target_compile_options(gdel3d PRIVATE 
    $<$<COMPILE_LANGUAGE:CUDA>:--expt-relaxed-constexpr>
    $<$<COMPILE_LANGUAGE:CUDA>:-Xcompiler=-fPIC>
)
