#!/bin/bash


REPODIR=$(cd $(dirname $0); pwd)
XGBOOST_BUILD_DIR=${REPODIR}/build


# Set defaults for vars that may not have been defined externally
#  FIXME: if INSTALL_PREFIX is not set, check PREFIX, then check
#         CONDA_PREFIX, but there is no fallback from there!
INSTALL_PREFIX=${INSTALL_PREFIX:=${PREFIX:=${CONDA_PREFIX}}}
PARALLEL_LEVEL=${PARALLEL_LEVEL:=""}

mkdir -p ${XGBOOST_BUILD_DIR}
cd ${XGBOOST_BUILD_DIR}

cmake -DCMAKE_INSTALL_PREFIX=${INSTALL_PREFIX} \
      -DCMAKE_INSTALL_LIBDIR="lib" \
      -DUSE_CUDA=ON \
      -DUSE_NCCL=ON \
      -DNCCL_ROOT=${CONDA_PREFIX} \
      ..

make -j${PARALLEL_LEVEL} install

