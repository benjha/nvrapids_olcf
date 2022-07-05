#!/bin/bash

source $ANACONDA_DIR/etc/profile.d/conda.sh 
conda activate
# Update conda
conda install -n base -c defaults conda

conda env create --prefix "${CONDAENV_LOCATION}" \
  --file $YAML_SPEC

conda activate $CONDAENV_LOCATION
#this remove ld to not interfere with system ld

echo 'Removing CONDA LD'
conda remove --force ld_impl_linux-ppc64le
conda deactivate

