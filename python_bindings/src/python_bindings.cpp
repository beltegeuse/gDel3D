#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <vector>
#include <cstring>
#include <tuple>

namespace py = pybind11;

// C wrapper declarations to avoid template symbol issues
extern "C" {
    struct CPoint3 {
        double x, y, z;
    };

    struct CDelaunayOutput {
        int* tetrahedra;
        int num_tetrahedra;
        double total_time;
        int success;
    };

    int compute_delaunay_c(CPoint3* points, int num_points, CDelaunayOutput* output);
    void free_delaunay_output_c(CDelaunayOutput* output);
}

// Simple triangulation function using C wrapper
std::tuple<py::array_t<int>, double> triangulate(py::array_t<double> points) {
    auto buf_info = points.request();
    
    if (buf_info.ndim != 2 || buf_info.shape[1] != 3) {
        throw std::runtime_error("Points array must be of shape (n, 3)");
    }
    
    int num_points = buf_info.shape[0];
    double* ptr = static_cast<double*>(buf_info.ptr);
    
    // Convert to C format
    std::vector<CPoint3> c_points(num_points);
    for (int i = 0; i < num_points; i++) {
        c_points[i].x = ptr[i * 3 + 0];
        c_points[i].y = ptr[i * 3 + 1];
        c_points[i].z = ptr[i * 3 + 2];
    }
    
    // Call C wrapper
    CDelaunayOutput output;
    int success = compute_delaunay_c(c_points.data(), num_points, &output);
    
    if (!success || !output.success) {
        throw std::runtime_error("Delaunay triangulation failed");
    }
    
    // Convert tetrahedra to numpy array
    auto tetrahedra_copy = py::array_t<int>(
        {output.num_tetrahedra, 4},   // shape
        {4 * sizeof(int), sizeof(int)} // strides  
    );
    
    auto buf_copy = tetrahedra_copy.request();
    int* copy_ptr = static_cast<int*>(buf_copy.ptr);
    std::memcpy(copy_ptr, output.tetrahedra, output.num_tetrahedra * 4 * sizeof(int));
    
    double total_time = output.total_time;
    
    // Free the C output
    free_delaunay_output_c(&output);
    
    return std::make_tuple(tetrahedra_copy, total_time);
}

// Define the pybind11 module
PYBIND11_MODULE(pygdel3d, m) {
    m.doc() = "Python bindings for gDel3D - GPU-accelerated 3D Delaunay triangulation";
    
    // Expose the main triangulation function
    m.def("triangulate", &triangulate, 
          "Compute 3D Delaunay triangulation of a set of points",
          py::arg("points"));
    
    // Add version info
    m.attr("__version__") = "1.0.0";
}
