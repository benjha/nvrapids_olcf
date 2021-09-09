#!/bin/bash

module purge
module load gcc/9.3.0
module load cmake/3.20.2
module load cuda/11.0.3
module load gdrcopy/2.2

export CUDA_TOOLKIT_LIB_PATH=$CUDA_TOOLKIT_ROOT_DIR/lib64
export CLANG_TOOLS_PATH=$CONDA_PREFIX/bin
export CUDA_HOME=$CUDA_DIR
export LDFLAGS="-L$CUDA_DIR/lib64/stubs":"-L$CUDA_DIR/lib64":"-L$CONDA_PREFIX/lib"
export CC=$(which gcc)
export CXX=$(which g++)
export PARALLEL_LEVEL=4

source $ENV_DIR/etc/profile.d/conda.sh
conda activate $ENV_NAME

export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH
export  JAVA_HOME=$CONDA_PREFIX/lib/server/libjvm.so

