#!/bin/bash

if [ "$1" == "" ]; then
    echo "Specify dask-cuda version"
    echo "example: "
    echo "    ./dask-cuda.sh v0.19.1"
else
   DIR=dask-cuda_$1
   git clone https://github.com/rapidsai/dask-cuda.git $DIR
   cd $DIR
   git checkout $1
   python setup.py build_ext --inplace
   python setup.py install
fi
