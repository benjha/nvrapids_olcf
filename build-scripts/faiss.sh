#!/bin/bash


module load cmake/3.20.2
module load cuda/11.0.3
module load gcc/9.3.0

export CC=$(which gcc)
export CXX=$(which g++)

export CUDA_TOOLKIT_LIB_PATH=$CUDA_TOOLKIT_ROOT_DIR/lib64
export CLANG_TOOLS_PATH=$CONDA_PREFIX/bin
export CUDA_HOME=$CUDA_DIR

export LD_LIBRARY_PATH=$CONDAENV_LOCATION/lib:$LD_LIBRARY_PATH

if [ "$1" == "" ]; then
    echo "Specify Faiss version"
    echo "example: "
    echo "    ./faiss.sh v1.7.0"
else
   FAISS_DIR=faiss_$1
#   git clone https://github.com/facebookresearch/faiss.git $FAISS_DIR
   cd $FAISS_DIR
#   git checkout $1

   mkdir -p build
   cd build

   cmake .. \
      -DCMAKE_C_COMPILER=$CC \
      -DCMAKE_CXX_COMPILER=$CXX \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_LIBDIR="lib" \
      -DCMAKE_INSTALL_PREFIX=${CONDAENV_LOCATION} \
      -DCMAKE_CUDA_ARCHITECTURES="70" \
      -DFAISS_ENABLE_PYTHON=OFF \
      ..

    make -j${PARALLEL_LEVEL}
    make install
fi
