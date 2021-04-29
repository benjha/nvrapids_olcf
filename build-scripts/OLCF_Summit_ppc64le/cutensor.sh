#!/bin/bash

CUTENSOR_VERSION=1.2.0
CUTENSOR_PATH="../dependencies/libcutensor_${CUTENSOR_VERSION}"

echo "cuTENSOR path: " $CUTENSOR_PATH

cp -r ${CUTENSOR_PATH}/include/* $CONDA_PREFIX/include
cp -P ${CUTENSOR_PATH}/lib/11.0/* $CONDA_PREFIX/lib

