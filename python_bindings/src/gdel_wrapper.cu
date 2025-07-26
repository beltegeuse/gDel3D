// CUDA wrapper to avoid C++ template symbol mangling issues
#include "gDel3D/GpuDelaunay.h"
#include "gDel3D/CommonTypes.h"

// C-style wrapper function to avoid template symbol mangling
extern "C"
{

    // Struct to hold point data in C-compatible format
    struct CPoint3
    {
        double x, y, z;
    };

    // Struct to hold output data in C-compatible format
    struct CDelaunayOutput
    {
        int *tetrahedra;
        int num_tetrahedra;
        double total_time;
        int success;
    };

    // C wrapper function that internally uses the C++ API
    int compute_delaunay_c(CPoint3 *points, int num_points, CDelaunayOutput *output)
    {
        try
        {
            // Convert C points to Point3HVec
            Point3HVec pointVec;
            pointVec.reserve(num_points);

            for (int i = 0; i < num_points; i++)
            {
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
            output->total_time = gdelOutput.stats.totalTime;
            output->success = 1;

            int nb_tetra_alive = 0;
            for (int i = 0; i < gdelOutput.tetInfoVec.size(); i++)
            {
                if (!isTetAlive(gdelOutput.tetInfoVec[i]))
                {
                    continue; // Skip dead tets
                }

                const Tet &tet = gdelOutput.tetVec[i];

                // Check all indices are differents
                if (tet._v[0] == tet._v[1] || tet._v[0] == tet._v[2] || tet._v[0] == tet._v[3] ||
                    tet._v[1] == tet._v[2] || tet._v[1] == tet._v[3] ||
                    tet._v[2] == tet._v[3])
                {
                    continue; // Skip invalid tetrahedra
                }

                // 32768 max
                if (tet._v[0] == num_points || tet._v[1] == num_points || tet._v[2] == num_points || tet._v[3] == num_points)
                {
                    continue; // Skip invalid tetrahedra
                }
                nb_tetra_alive++;
            }
            output->num_tetrahedra = nb_tetra_alive;

            // Allocate and copy tetrahedra data
            if (nb_tetra_alive > 0)
            {
                output->tetrahedra = new int[nb_tetra_alive * 4];
                int index = 0;
                for (int i = 0; i < gdelOutput.tetInfoVec.size(); i++)
                {
                    if (!isTetAlive(gdelOutput.tetInfoVec[i]))
                        continue; // Skip dead tets

                    const Tet &tet = gdelOutput.tetVec[i];
                    // Check all indices are different
                    if (tet._v[0] == tet._v[1] || tet._v[0] == tet._v[2] || tet._v[0] == tet._v[3] ||
                        tet._v[1] == tet._v[2] || tet._v[1] == tet._v[3] ||
                        tet._v[2] == tet._v[3])
                    {
                        continue; // Skip invalid tetrahedra
                    }

                    // 32768 max
                    if (tet._v[0] == num_points || tet._v[1] == num_points || tet._v[2] == num_points || tet._v[3] == num_points)
                    {
                        continue; // Skip invalid tetrahedra
                    }

                    output->tetrahedra[index * 4 + 0] = tet._v[0];
                    output->tetrahedra[index * 4 + 1] = tet._v[1];
                    output->tetrahedra[index * 4 + 2] = tet._v[2];
                    output->tetrahedra[index * 4 + 3] = tet._v[3];

                    index++;
                }
            }
            else
            {
                output->tetrahedra = nullptr;
            }

            return 1; // Success
        }
        catch (const std::exception &e)
        {
            output->success = 0;
            output->tetrahedra = nullptr;
            output->num_tetrahedra = 0;
            return 0; // Failure
        }
    }

    // Function to free allocated memory
    void free_delaunay_output_c(CDelaunayOutput *output)
    {
        if (output && output->tetrahedra)
        {
            delete[] output->tetrahedra;
            output->tetrahedra = nullptr;
        }
    }

} // extern "C"
