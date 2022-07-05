#!/bin/bash

# https://docs.cupy.dev/en/stable/reference/environment.html

if [ "$1" == "" ]; then
    echo "Specify CuPy version"
    echo "example: "
    echo "    ./cupy.sh v8.6.0"
else
   CUPY_DIR=cupy_$1
   git clone https://github.com/cupy/cupy.git $CUPY_DIR
   cd $CUPY_DIR
   git checkout $1
   git submodule update --init

   export CUPY_ACCELERATORS='cutensor'
   export CUPY_NVCC_GENERATE_CODE="arch=compute_70,code=sm_70"
   export CFLAGS=-I$CONDA_PREFIX/include
   export LDFLAGS="-L$CONDA_PREFIX/lib":$LDFLAGS
   python setup.py build
   python setup.py install
fi
