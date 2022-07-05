#!/bin/bash

if [ "$1" == "" ]; then
    echo "Specify cuGraph version"
    echo "example: "
    echo "    ./cugraph.sh v0.19.0"
else
   CUGRAPH_DIR=cugraph_$1
#   git clone https://github.com/rapidsai/cugraph.git $CUGRAPH_DIR
   cd $CUGRAPH_DIR
#   git checkout $1
   export LAPACK=$OLCF_NETLIB_LAPACK_ROOT/lib64/liblapack.so
   export BLAS=$OLCF_NETLIB_LAPACK_ROOT/lib64/libcblas.so
   ./build.sh libcugraph cugraph
fi
