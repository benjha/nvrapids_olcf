#!/bin/bash

module purge

#export LDFLAGS="-L$CUDA_DIR/lib64/stubs -L$CUDA_DIR/lib64":"-L$CONDA_PREFIX/lib"
export PARALLEL_LEVEL=4

source $CONDA_DIR/etc/profile.d/conda.sh
conda activate $CONDAENV_LOCATION

module load cmake/3.20.2
module load cuda/11.5.2
module load gcc/9.3.0
module load spectrum-mpi/10.4.0.3-20210112

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib
export JAVA_HOME=$CONDA_PREFIX/lib/server/libjvm.so

export CC=$(which gcc)
export CXX=$(which g++)

export CUDA_TOOLKIT_LIB_PATH=$CUDA_TOOLKIT_ROOT_DIR/lib64
export CLANG_TOOLS_PATH=$CONDA_PREFIX/bin
export CUDA_HOME=$CUDA_DIR

