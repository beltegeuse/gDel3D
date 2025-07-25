cmake_minimum_required(VERSION 3.18)
project(pygdel3d LANGUAGES CXX CUDA)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CUDA_STANDARD 17)

# Find required packages
find_package(CUDA REQUIRED)
find_package(pybind11 REQUIRED)

# Set CUDA flags
set(CMAKE_CUDA_FLAGS "${CMAKE_CUDA_FLAGS} -std=c++17")
set(CMAKE_CUDA_ARCHITECTURES "75")  # Use single architecture to avoid symbol mangling issues

# Disable LTO to avoid version conflicts between CUDA and host compilers
set(CMAKE_INTERPROCEDURAL_OPTIMIZATION OFF)

# Source files from the original project
set(GDEL_SOURCES
    ../GDelFlipping/src/DelaunayChecker.cu
    ../GDelFlipping/src/InputCreator.cu
    ../GDelFlipping/src/RandGen.cpp
    ../GDelFlipping/src/gDel3D/GpuDelaunay.cu
    ../GDelFlipping/src/gDel3D/CPU/predicates.cpp
    ../GDelFlipping/src/gDel3D/CPU/PredWrapper.cu
    ../GDelFlipping/src/gDel3D/CPU/Splaying.cu
    ../GDelFlipping/src/gDel3D/CPU/Star.cu
    ../GDelFlipping/src/gDel3D/GPU/KerDivision.cu
    ../GDelFlipping/src/gDel3D/GPU/KerPredicates.cu
    ../GDelFlipping/src/gDel3D/GPU/ThrustWrapper.cu
)

# Python binding source
set(BINDING_SOURCE 
    src/python_bindings.cpp
    src/gdel_wrapper.cu
)

# Create the pybind11 module
pybind11_add_module(pygdel3d ${BINDING_SOURCE} ${GDEL_SOURCES})

# Disable LTO for pybind11
set_target_properties(pygdel3d PROPERTIES INTERPROCEDURAL_OPTIMIZATION FALSE)

# Set CUDA properties
set_target_properties(pygdel3d PROPERTIES
    CUDA_SEPARABLE_COMPILATION ON
    POSITION_INDEPENDENT_CODE ON
)

# Include directories
target_include_directories(pygdel3d PRIVATE 
    ../GDelFlipping/src
    ${CMAKE_CUDA_TOOLKIT_INCLUDE_DIRECTORIES}
    ${CUDA_INCLUDE_DIRS}
)

# Link CUDA libraries
target_link_libraries(pygdel3d PRIVATE 
    ${CUDA_LIBRARIES}
    ${CUDA_curand_LIBRARY}
)

# Compiler-specific options
target_compile_definitions(pygdel3d PRIVATE VERSION_INFO="${EXAMPLE_VERSION_INFO}")

# For older CMake versions, explicitly set the CUDA compiler
if(CMAKE_VERSION VERSION_LESS "3.20")
    set_property(TARGET pygdel3d PROPERTY CUDA_RESOLVE_DEVICE_SYMBOLS ON)
endif()
