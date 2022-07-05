#!/bin/bash

module load gcc/9.3.0

export CC=$(which gcc)
export CXX=$(which g++)


mkdir libcypher-parser-v0.6.2
cd libcypher-parser-v0.6.2

wget https://github.com/cleishm/libcypher-parser/releases/download/v0.6.2/libcypher-parser-0.6.2.tar.gz
tar xvf libcypher-parser-0.6.2.tar.gz
cd libcypher-parser-0.6.2
./configure --prefix=$CONDAENV_LOCATION
make -j${PARALLEL_LEVEL}
make install

