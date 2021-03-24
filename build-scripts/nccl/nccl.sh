#!/bin/bash

make -j 160 src.build  CUDA_HOME=$CUDA_DIR NVCC_GENCODE="-gencode=arch=compute_70,code=sm_70" BUILDDIR=$CONDA_PREFIX

