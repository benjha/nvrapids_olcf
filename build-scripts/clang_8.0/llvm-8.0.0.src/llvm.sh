#!/bin/bash

REPODIR=$(cd $(dirname $0); pwd)
LLVM_BUILD_DIR=${REPODIR}/build

mkdir -p ${LLVM_BUILD_DIR}
cd  ${LLVM_BUILD_DIR}

cmake ..                                        \
  -DCMAKE_C_COMPILER=gcc			\
  -DCMAKE_CXX_COMPILER=g++			\
  -DCMAKE_BUILD_TYPE=Release                    \
  -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX  \
  -DLLVM_BUILD_LLVM_DYLIB=ON                    \
  -DLLVM_ENABLE_RTTI=ON                         \
  -DLLVM_INSTALL_UTILS=ON                       \
  -DLLVM_TARGETS_TO_BUILD:STRING=PowerPC        \
  -DLLVM_ENABLE_PROJECTS="clang" \
  -DLLVM_DEFAULT_TARGET_TRIPLE="powerpc64le-linux-rhel-7.6" \
  -DLLVM_HOST_TRIPLE="powerpc64le-linux-rhel-7.6" \
  -DPYTHON_EXECUTABLE=$CONDA_PREFIX/bin/python3.7 \
  ..

make -j${PARALLEL_LEVEL}
make install
