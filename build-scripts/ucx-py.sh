#!/bin/bash

if [ "$1" == "" ]; then
    echo "Specify UCX-Py version"
    echo "example: "
    echo "    ./ucx-py.sh v0.19.0"
else
    UCX_PY_DIR=ucx-py_$1
    git clone https://github.com/rapidsai/ucx-py.git $UCX_PY_DIR
    cd $UCX_PY_DIR
    git checkout $1
    
    #python setup.py build_ext --inplace
    #pip install .
    pip install -v .
fi
