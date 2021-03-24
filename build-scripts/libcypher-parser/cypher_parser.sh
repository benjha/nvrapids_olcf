#!/bin/bash

./autogen.sh
./configure --prefix=$CONDA_PREFIX
make -j${PARALLEL_LEVEL}
make install

