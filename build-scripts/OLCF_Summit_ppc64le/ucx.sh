#!/bin/bash

module unload spectrum-mpi
module unload xl
module unload xalt

if [ "$1" == "" ]; then
    echo "Specify UCX  version"
    echo "example: "
    echo "    ./ucx.sh v1.8.x"
else
    UCX_DIR=ucx_$1
    git clone https://github.com/openucx/ucx.git $UCX_DIR
    cd $UCX_DIR
    git checkout $1

    # https://ucx-py.readthedocs.io/en/latest/install.html#ucx-1-9
    # apply UCX IB registration cache patch, improves overall
    # CUDA IB performance when using a memory pool
    curl -LO https://raw.githubusercontent.com/rapidsai/ucx-split-feedstock/11ad7a3c1f25514df8064930f69c310be4fd55dc/recipe/cuda-alloc-rcache.patch
    git apply cuda-alloc-rcache.patch

    if [ -z "$CONDA_PREFIX" ]; then
        echo '---------UCX configuration error, CONDA_PREFIX not set'
        exit 1
    fi

    KNEM_DIR=$(pkg-config --variable=prefix knem)
    INSTALL_DIR=$CONDA_PREFIX

    ./autogen.sh

    ./configure CC=gcc CXX=g++ \
        CXXFLAGS="-m64 -O3 -fPIC" \
        CFLAGS="-m64 -O3 -fPIC" \
        --prefix=$INSTALL_DIR \
        --disable-debug \
        --enable-compiler-opt=3 --enable-optimizations \
        --enable-mt --with-mcpu=powerpc64le \
        --enable-debug \
        --with-cuda=$CUDA_DIR --with-knem=$KNEM_DIR \
        --with-verbs='/usr' --with-rdmacm='/usr' \
        --with-gdrcopy=$OLCF_GDRCOPY_ROOT \
        --with-rc --with-ud --with-dc --with-mlx5-dv \
        --with-cm --with-dm

    make -j${PARALLEL_LEVEL}
    make install
fi
