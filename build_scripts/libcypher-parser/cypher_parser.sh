#!/bin/bash

./configure --prefix=$CONDA_PREFIX
make -j${PARALLEL_LEVEL}
make install
