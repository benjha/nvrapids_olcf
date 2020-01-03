#!/bin/bash

REPODIR=$(cd $(dirname $0); pwd)

THRIFT_BUILD_DIR=${REPODIR}

./bootstrap.sh
./configure CXXFLAGS='-O3' CFLAGS='-O3' \
    --prefix=${CONDA_PREFIX} \
    --with-cpp=yes \
    --with-haskell=no --with-nodejs=no \
    --with-python=no \
    --with-boost=${CONDA_PREFIX} \
    --with-libevent=${CONDA_PREFIX} \
    --enable-shared --enable-static \
    --enable-tests=no --enable-tutorial=no

make -j${PARALLEL_LEVEL}
cp -r lib/cpp/src/thrift ${CONDA_PREFIX}/include
