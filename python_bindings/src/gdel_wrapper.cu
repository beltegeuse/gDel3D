// CUDA wrapper to avoid C++ template symbol mangling issues
#include "gDel3D/GpuDelaunay.h"
#include "gDel3D/CommonTypes.h"

// C-style wrapper function to avoid template symbol mangling
extern "C" {
    
// Struct to hold point data in C-compatible format
struct CPoint3 {
    double x, y, z;
};

// Struct to hold output data in C-compatible format
struct CDelaunayOutput {
    int* tetrahedra;
    int num_tetrahedra;
    double total_time;
    int success;
};

// C wrapper function that internally uses the C++ API
int compute_delaunay_c(CPoint3* points, int num_points, CDelaunayOutput* output) {
    try {
        // Convert C points to Point3HVec
        Point3HVec pointVec;
        pointVec.reserve(num_points);
        
        for (int i = 0; i < num_points; i++) {
            Point3 p;
            p._p[0] = points[i].x;
            p._p[1] = points[i].y;
            p._p[2] = points[i].z;
            pointVec.push_back(p);
        }
        
        // Create GpuDel instance and output
        GpuDel triangulator;
        GDelOutput gdelOutput;
        
        // Compute triangulation
        triangulator.compute(pointVec, &gdelOutput);
        
        // Convert output back to C format
        output->num_tetrahedra = gdelOutput.tetVec.size();
        output->total_time = gdelOutput.stats.totalTime;
        output->success = 1;
        
        // Allocate and copy tetrahedra data
        if (output->num_tetrahedra > 0) {
            output->tetrahedra = new int[output->num_tetrahedra * 4];
            for (int i = 0; i < output->num_tetrahedra; i++) {
                const Tet& tet = gdelOutput.tetVec[i];
                output->tetrahedra[i * 4 + 0] = tet._v[0];
                output->tetrahedra[i * 4 + 1] = tet._v[1];
                output->tetrahedra[i * 4 + 2] = tet._v[2];
                output->tetrahedra[i * 4 + 3] = tet._v[3];
            }
        } else {
            output->tetrahedra = nullptr;
        }
        
        return 1; // Success
        
    } catch (const std::exception& e) {
        output->success = 0;
        output->tetrahedra = nullptr;
        output->num_tetrahedra = 0;
        return 0; // Failure
    }
}

// Function to free allocated memory
void free_delaunay_output_c(CDelaunayOutput* output) {
    if (output && output->tetrahedra) {
        delete[] output->tetrahedra;
        output->tetrahedra = nullptr;
    }
}

} // extern "C"
