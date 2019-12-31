#!/bin/bash

REPODIR=$(cd $(dirname $0); pwd)

PYARROW_BUILD_DIR=${REPODIR}/python

cd ${REPODIR}

cd ${PYARROW_BUILD_DIR}

export PYARROW_WITH_FLIGHT=0
export PYARROW_WITH_GANDIVA=0
export PYARROW_WITH_ORC=0
export PYARROW_WITH_PARQUET=0
export PYARROW_WITH_PLASMA=0
export PYARROW_WITH_CUDA=1
export ARROW_HOME=${CONDA_PREFIX}

python setup.py build_ext --inplace
python setup.py install

cd ${REPODIR}


