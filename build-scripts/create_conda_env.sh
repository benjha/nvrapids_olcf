#!/bin/bash

source $CONDA_DIR/etc/profile.d/conda.sh 
conda activate
# Update conda
conda install -n base -c defaults conda

conda env create --prefix "${CONDAENV_LOCATION}" \
  --file $YAML_SPEC

conda activate $CONDAENV_LOCATION

#this remove ld to not interfere with system's ld
echo 'Removing CONDA LD'
conda remove --force-remove ld_impl_linux-ppc64le -y

# cuda-python is a new dependency which installs cudatoolkit.
# cudatoolkit conflicts with Summit's cuda, thus removing
echo 'Removing CONDA cudatoolkit'

conda remove --force-remove cudatoolkit -y
conda deactivate
