#!/bin/bash

module load python/3.7.0-anaconda3-5.3.0

export UMS_DIR=/sw/summit/ums/gen119
export ENV_DIR=$UMS_DIR/nvrapids_0.19_gcc_9.3.0

conda env create -f rapids_0.19_cuda11.0.3_ppc64le.yml -p $ENV_DIR

