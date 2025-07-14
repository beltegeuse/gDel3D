#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <vector>

// SINGLE COMPILATION UNIT APPROACH - CUDA VERSION
// Include all gDel3D source files to ensure consistent template instantiation
// This prevents Thrust symbol mismatch issues

// Include gDel3D headers
#include "gDel3D/GpuDelaunay.h"
#include "gDel3D/CommonTypes.h"

namespace py = pybind11;

std::vector<std::vector<int>> compute_delaunay_tetrahedralization(py::array_t<double> points) {
    py::buffer_info buf = points.request();
    
    if (buf.ndim != 2 || buf.shape[1] != 3) {
        throw std::runtime_error("Input array must be Nx3");
    }
    
    int num_points = buf.shape[0];
    double* ptr = static_cast<double*>(buf.ptr);
    
    if (num_points < 4) {
        throw std::runtime_error("At least 4 points are required for 3D Delaunay triangulation");
    }
    
    // Convert to gDel3D format
    Point3HVec point_vec;
    for (int i = 0; i < num_points; i++) {
        Point3 p;
        p._p[0] = ptr[i * 3 + 0];
        p._p[1] = ptr[i * 3 + 1]; 
        p._p[2] = ptr[i * 3 + 2];
        point_vec.push_back(p);
    }
    
    // Create gDel3D triangulator and compute Delaunay triangulation
    GpuDel triangulator;
    GDelOutput output;
    
    try {
        triangulator.compute(point_vec, &output);
    } catch (const std::exception& e) {
        throw std::runtime_error(std::string("gDel3D computation failed: ") + e.what());
    }
    
    // Convert output tetrahedra to Python format
    std::vector<std::vector<int>> result;
    for (size_t i = 0; i < output.tetVec.size(); i++) {
        const Tet& tet = output.tetVec[i];
        
        // Skip infinite tetrahedra (those that contain the kernel/infinity point)
        // The infinity point is usually the last point or marked specially
        bool hasInfinity = false;
        for (int j = 0; j < 4; j++) {
            if (tet._v[j] >= num_points) {
                hasInfinity = true;
                break;
            }
        }
        
        if (!hasInfinity) {
            std::vector<int> tetrahedron = {tet._v[0], tet._v[1], tet._v[2], tet._v[3]};
            result.push_back(tetrahedron);
        }
    }
    
    return result;
}

std::vector<std::vector<int>> compute_delaunay_from_list(const std::vector<std::tuple<double, double, double>>& points) {
    if (points.size() < 4) {
        throw std::runtime_error("At least 4 points are required for 3D Delaunay triangulation");
    }
    
    // Convert to gDel3D format
    Point3HVec point_vec;
    for (const auto& point : points) {
        Point3 p;
        p._p[0] = std::get<0>(point);
        p._p[1] = std::get<1>(point);
        p._p[2] = std::get<2>(point);
        point_vec.push_back(p);
    }
    
    // Create gDel3D triangulator and compute Delaunay triangulation
    GpuDel triangulator;
    GDelOutput output;
    
    try {
        triangulator.compute(point_vec, &output);
    } catch (const std::exception& e) {
        throw std::runtime_error(std::string("gDel3D computation failed: ") + e.what());
    }
    
    // Convert output tetrahedra to Python format
    std::vector<std::vector<int>> result;
    int num_points = points.size();
    
    for (size_t i = 0; i < output.tetVec.size(); i++) {
        const Tet& tet = output.tetVec[i];
        
        // Skip infinite tetrahedra (those that contain the kernel/infinity point)
        bool hasInfinity = false;
        for (int j = 0; j < 4; j++) {
            if (tet._v[j] >= num_points) {
                hasInfinity = true;
                break;
            }
        }
        
        if (!hasInfinity) {
            std::vector<int> tetrahedron = {tet._v[0], tet._v[1], tet._v[2], tet._v[3]};
            result.push_back(tetrahedron);
        }
    }
    
    return result;
}

PYBIND11_MODULE(gdel3d, m) {
    m.doc() = "gDel3D Python bindings - single compilation unit approach";
    m.attr("__version__") = "0.3.0-single-unit";
    
    m.def("compute_delaunay", &compute_delaunay_tetrahedralization,
          "Compute Delaunay tetrahedralization from numpy array",
          py::arg("points"));
          
    m.def("compute_delaunay_from_list", &compute_delaunay_from_list,
          "Compute Delaunay tetrahedralization from list of points",
          py::arg("points"));
}
