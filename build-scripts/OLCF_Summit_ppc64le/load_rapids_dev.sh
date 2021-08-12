#!/bin/bash

module purge
module load gcc/9.3.0
module load cmake/3.20.2
module load cuda/11.0.3
module load netlib-lapack/3.8.0
module load libtool/2.4.2
module load gdrcopy/2.0

export CUDA_TOOLKIT_LIB_PATH=$CUDA_TOOLKIT_ROOT_DIR/lib64
export CLANG_TOOLS_PATH=$CONDA_PREFIX/bin
export CUDA_HOME=$CUDA_DIR
export LDFLAGS="-L$CUDA_DIR/lib64/stubs":"-L$CUDA_DIR/lib64":"-L$CONDA_PREFIX/lib"
export CC=$(which gcc)
export CXX=$(which g++)
export PARALLEL_LEVEL=4

export LAPACK=$OLCF_NETLIB_LAPACK_ROOT/lib64/liblapack.so
export BLAS=$OLCF_NETLIB_LAPACK_ROOT/lib64/libcblas.so

source $ENV_DIR/etc/profile.d/conda.sh
conda activate
conda activate $ENV_NAME

export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH
export  JAVA_HOME=$CONDA_PREFIX/lib/server/libjvm.so

