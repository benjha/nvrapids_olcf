#!/bin/bash


module load cmake/3.20.2
module load cuda/11.0.3
module load gcc/9.3.0

export CC=$(which gcc)
export CXX=$(which g++)

export CUDA_TOOLKIT_LIB_PATH=$CUDA_TOOLKIT_ROOT_DIR/lib64
export CLANG_TOOLS_PATH=$CONDA_PREFIX/bin
export CUDA_HOME=$CUDA_DIR




if [ "$1" == "" ]; then
    echo "Specify UCX  version"
    echo "example: "
    echo "    ./ucx.sh v1.8.x"
else
    UCX_DIR=ucx_$1
    git clone https://github.com/openucx/ucx.git $UCX_DIR
    cd $UCX_DIR
    git checkout $1

    KNEM_DIR=$(pkg-config --variable=prefix knem)
    INSTALL_DIR=$CONDAENV_LOCATION

    ./autogen.sh

    ./configure \
        CXXFLAGS="-m64 -O3 -fPIC" \
        CFLAGS="-m64 -O3 -fPIC" \
	LDFLAGS="-L/usr/lib64 -liberty" \
	--disable-debug \
        --prefix=$INSTALL_DIR \
	--enable-compiler-opt=3 --enable-optimizations \
	--with-mcpu=powerpc64le \
        --enable-mt \
        --with-cuda="$CUDA_DIR" \
        --enable-mt \
	--with-knem=$KNEM_DIR \
        --with-rdmacm=/usr \
        --with-verbs=/usr \

    make -j${PARALLEL_LEVEL}
    make install
fi
