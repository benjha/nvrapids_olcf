#!/bin/bash

if [ "$1" == "" ]; then
    echo "Specify cuDF version"
    echo "example: "
    echo "    ./cudf.sh v0.19.1"
else
   CUDF_DIR=cudf_$1
#   git clone https://github.com/rapidsai/cudf.git $CUDF_DIR
   cd $CUDF_DIR
#   git checkout $1
   export Arrow_DIR=$CONDA_PREFIX
#   ./build.sh libcudf cudf dask_cudf
   ./build.sh dask_cudf
fi
