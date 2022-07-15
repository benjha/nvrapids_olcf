#!/bin/bash

if [ "$1" == "" ]; then
    echo "Specify cuGraph version"
    echo "example: "
    echo "    ./cugraph.sh v0.19.0"
else
   CUGRAPH_DIR=cugraph_$1
   git clone https://github.com/rapidsai/cugraph.git $CUGRAPH_DIR
   cd $CUGRAPH_DIR
   git checkout $1
    
   # Patching CMakeLists.txt to set correct Thrust version
   # and avoid libcugraph ops
   sed -i 's@include(cmake/thirdparty/get_libcudacxx.cmake)@include(cmake/thirdparty/get_thrust.cmake)\ninclude(cmake/thirdparty/get_libcudacxx.cmake)@g' cpp/CMakeLists.txt
   sed -i 's@include(cmake/thirdparty/get_libcugraphops.cmake)@@g' cpp/CMakeLists.txt
   sed -i 's@cugraph-ops::cugraph-ops++@@g' cpp/CMakeLists.txt
   
   sed -i 's@src/sampling/neighborhood.cu@#src/sampling/neighborhood.cu@g' cpp/CMakeLists.txt
   sed -i 's@src/sampling/nbr_sampling_mg.cu@#src/sampling/nbr_sampling_mg.cu@g' cpp/CMakeLists.txt
   sed -i 's@src/sampling/uniform_neighbor_sampling_sg.cpp@#src/sampling/uniform_neighbor_sampling_sg.cpp@g' cpp/CMakeLists.txt
   sed -i 's@src/sampling/uniform_neighbor_sampling_mg.cpp@#src/sampling/uniform_neighbor_sampling_mg.cpp@g' cpp/CMakeLists.txt
   
   sed -i 's@#include <cugraph-ops/graph/sampling.hpp>@//#include <cugraph-ops/graph/sampling.hpp>@g' cpp/include/cugraph/algorithms.hpp

   wget -P cpp/cmake/thirdparty https://raw.githubusercontent.com/rapidsai/cugraph/0ba6551841680b6689f81a05c3636c75f679b5c1/cpp/cmake/thirdparty/get_thrust.cmake

   export LAPACK=$OLCF_NETLIB_LAPACK_ROOT/lib64/liblapack.so
   export BLAS=$OLCF_NETLIB_LAPACK_ROOT/lib64/libcblas.so
   ./build.sh libcugraph cugraph pylibcugraph --skip_cpp_tests
   ./build.sh pylibcugraph
fi
