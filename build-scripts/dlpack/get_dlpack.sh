#!/bin/bash

mkdir  $CONDA_PREFIX/include/dlpack
wget --directory-prefix=$CONDA_PREFIX/include/dlpack https://raw.githubusercontent.com/dmlc/dlpack/master/include/dlpack/dlpack.h
