#!/bin/bash

module load gcc/9.3.0
module load cmake/3.18.2
module load python/3.7.0-anaconda3-5.3.0
module load cuda/11.0.3
module load netlib-lapack/3.8.0

export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH
export CUDA_TOOLKIT_LIB_PATH=$CUDA_TOOLKIT_ROOT_DIR/lib64
export CLANG_TOOLS_PATH=$CONDA_PREFIX/bin
export CUDA_HOME=$CUDA_DIR
export LDFLAGS="-L$CUDA_DIR/lib64":"-L$CONDA_PREFIX/lib"
export CC=$(which gcc)
export CXX=$(which g++)
export PARALLEL_LEVEL=4

export JAVA_HOME=$ENV_DIR/ibm-java-ppc64le-110/jdk-11.0.10+9

export LAPACK=$OLCF_NETLIB_LAPACK_ROOT/lib64/liblapack.so
export BLAS=$OLCF_NETLIB_LAPACK_ROOT/lib64/libcblas.so

source activate $ENV_DIR

