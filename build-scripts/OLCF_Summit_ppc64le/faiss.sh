#!/bin/bash

if [ "$1" == "" ]; then
    echo "Specify Faiss version"
    echo "example: "
    echo "    ./faiss.sh v1.7.0"
else
   FAISS_DIR=faiss_$1
   git clone https://github.com/facebookresearch/faiss.git $FAISS_DIR
   cd $FAISS_DIR
   git checkout $1

   mkdir -p build
   cd build

   cmake .. \
      -DCMAKE_C_COMPILER=gcc \
      -DCMAKE_CXX_COMPILER=g++ \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_LIBDIR="lib" \
      -DCMAKE_INSTALL_PREFIX=${CONDA_PREFIX} \
      -DCMAKE_CUDA_ARCHITECTURES="70" \
      -DFAISS_ENABLE_PYTHON=OFF \
      ..

    make -j${PARALLEL_LEVEL}
    make install
fi
