#!/bin/bash

if [ "$1" == "" ]; then
    echo "Specify NCCL version"
    echo "example: "
    echo "    ./nccl.sh v2.9.6-1"
else
   git clone https://github.com/NVIDIA/nccl.git nccl_$NCCL_VER
   cd nccl_$NCCL_VER
   git checkout $1
   make -j 160 src.build  CUDA_HOME=$CUDA_DIR NVCC_GENCODE="-gencode=arch=compute_70,code=sm_70" BUILDDIR=$CONDA_PREFIX
fi
