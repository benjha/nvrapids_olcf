#!/bin/bash

mkdir libcypher-parser-v0.6.2
cd libcypher-parser-v0.6.2

wget https://github.com/cleishm/libcypher-parser/releases/download/v0.6.2/libcypher-parser-0.6.2.tar.gz
tar xvf libcypher-parser-0.6.2.tar.gz
cd libcypher-parser-0.6.2
./configure --prefix=$CONDA_PREFIX
make -j${PARALLEL_LEVEL}
make install

