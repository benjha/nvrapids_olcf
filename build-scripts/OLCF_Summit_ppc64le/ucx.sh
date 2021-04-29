#!/bin/bash

module unload spectrum-mpi
module unload xl
module unload xalt
module load libtool/2.4.2
module load gdrcopy/2.0


if [ "$1" == "" ]; then
    echo "Specify UCX  version"
    echo "example: "
    echo "    ./ucx.sh v1.8.1"
else
    UCX_DIR=ucx_$1
    git clone https://github.com/openucx/ucx.git $UCX_DIR
    cd $UCX_DIR
    git checkout $1

    # https://ucx-py.readthedocs.io/en/latest/install.html#ucx-1-8
    # apply UCX IB registration cache patch, improves overall
    # CUDA IB performance when using a memory pool
    curl -LO https://raw.githubusercontent.com/rapidsai/ucx-split-feedstock/bd0377fb7363fd0ddbc3d506ae3414ef6f2e2f50/recipe/add-page-alignment.patch add-page-alignment.patch
    curl -LO https://raw.githubusercontent.com/rapidsai/ucx-split-feedstock/bd0377fb7363fd0ddbc3d506ae3414ef6f2e2f50/recipe/ib_registration_cache.patch ib_registration_cache.patch
    git apply ib_registration_cache.patch && git apply add-page-alignment.patch

    KNEM_DIR=$(pkg-config --variable=prefix knem)
    INSTALL_DIR=$CONDA_PREFIX

    ./autogen.sh

    ./configure CC=gcc CXX=g++ \
        CXXFLAGS="-m64 -O3" \
        CFLAGS="-m64 -O3" \
        --prefix=$INSTALL_DIR \
        --enable-compiler-opt=3 --enable-optimizations \
        --enable-mt --with-mcpu=powerpc64le \
        --enable-debug \
        --with-cuda=$CUDA_DIR --with-knem=$KNEM_DIR \
        --with-verbs='/usr' \
        --with-gdrcopy=$OLCF_GDRCOPY_ROOT \
        --with-rc --with-ud --with-dc --with-mlx5-dv \
        --with-cm --with-dm

    make -j${PARALLEL_LEVEL}
    make install
fi
