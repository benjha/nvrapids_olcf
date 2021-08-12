#!/bin/bash

source $ENV_DIR/etc/profile.d/conda.sh 
conda activate
conda env create -f $YAML_SPEC 
conda activate $ENV_NAME
conda deactivate

