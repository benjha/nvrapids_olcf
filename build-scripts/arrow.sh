#!/bin/bash

echo $CUDA_HOME
export LD=/usr/bin/ld

if [ "$1" == "" ]; then
    echo "Specify Arrow version"
    echo "example: "
    echo "    ./arrow.sh apache-arrow-1.0.1"
else
    ARROW_DIR=$1
    ARROW_BUILD_DIR=cpp/build

    git clone https://github.com/apache/arrow.git $ARROW_DIR
    cd $ARROW_DIR
    git checkout $1

    mkdir -p ${ARROW_BUILD_DIR}
    cd  ${ARROW_BUILD_DIR}

    cmake .. \
      -DCMAKE_C_COMPILER=gcc \
      -DCMAKE_CXX_COMPILER=g++ \
      -DCMAKE_LINKER=/usr/bin/ld \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_LIBDIR="lib" \
      -DCMAKE_INSTALL_PREFIX=${CONDA_PREFIX} \
      -DARROW_BOOST_USE_SHARED=ON \
      -DARROW_BUILD_BENCHMARKS=OFF \
      -DARROW_BUILD_STATIC=OFF \
      -DARROW_BUILD_SHARED=ON \
      -DARROW_BUILD_TESTS=OFF \
      -DARROW_BUILD_UTILITIES=OFF \
      -DARROW_DATASET=ON \
      -DARROW_FLIGHT=OFF \
      -DARROW_GANDIVA=OFF \
      -DARROW_HDFS=OFF \
      -DARROW_JEMALLOC=ON \
      -DARROW_MIMALLOC=ON \
      -DARROW_ORC=ON \
      -DARROW_PARQUET=ON \
      -DARROW_PLASMA=ON \
      -DARROW_PYTHON=ON \
      -DARROW_S3=OFF \
      -DARROW_CUDA=ON \
      -DARROW_IPC=ON \
      -DARROW_SIMD_LEVEL=NONE \
      -DARROW_WITH_BROTLI=ON \
      -DARROW_WITH_BZ2=ON \
      -DARROW_WITH_LZ4=ON \
      -DARROW_WITH_SNAPPY=ON \
      -DARROW_WITH_ZLIB=ON \
      -DARROW_WITH_ZSTD=ON \
      ..

    if [ $? -ne 0 ]; then
        echo '---------ARROW configuration error'
        exit 1
    fi

    make -j${PARALLEL_LEVEL}

    if [ $? -ne 0 ]; then
        echo '---------ARROW make error'
        exit 1
    fi
    make install


    cd ../../python

    export ARROW_HOME=${CONDA_PREFIX}
    export PARQUET_HOME=${CONDA_PREFIX}
    export PLASMA_HOME=${CONDA_PREFIX}
    export PYARROW_BUILD_TYPE=release
    export PYARROW_WITH_DATASET=1
    export PYARROW_WITH_PARQUET=1
    export PYARROW_WITH_ORC=1
    export PYARROW_WITH_PLASMA=1
    export PYARROW_WITH_CUDA=1
    export PYARROW_WITH_BROTLI=1
    export PYARROW_WITH_GANDIVA=0
    export PYARROW_WITH_FLIGHT=0
    export PYARROW_WITH_S3=0
    export PYARROW_WITH_HDFS=0

    python setup.py build_ext --inplace
    python setup.py install

    if [ $? -ne 0 ]; then
        echo '---------ARROW pybindings build error'
        exit 1
    fi
fi
