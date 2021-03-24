#!/bin/bash

./autogen.sh
./configure --prefix=$CONDA_PREFIX \
    --enable-compiler-opt \
    --enable-optimizations \
    --enable-mt \
    --with-avx --with-cuda=$CUDA_DIR \
    --with-verbs='/usr' \
    --with-rc --with-ud --with-dc --with-mlx5-dv

make -j${PARALLEL_LEVEL}
make install
