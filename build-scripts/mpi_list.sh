#!/bin/bash

if [ "$1" == "" ]; then
    echo "Specify mpi4py version"
    echo "example: "
    echo "    ./mpi4py.sh 3.1.1"
else
   MPI4PY_DIR=mpi4py_$1
   git clone https://github.com/rapidsai/cudf.git $MPI4PY_DIR
   cd $MPI4PY_DIR
   git checkout $1
   CC=mpicc MPICC=mpicc pip install mpi4py --no-binary mpi4py
fi
