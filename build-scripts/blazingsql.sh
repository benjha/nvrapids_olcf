#!/bin/bash

if [ "$1" == "" ]; then
    echo "Specify BlazingSQL version"
    echo "example: "
    echo "    ./blazingsql.sh v0.19.0"
else
   BLAZINGSQL_DIR=blazingsql_$1
    git clone https://github.com/rapidsai/blazingsql-release-staging.git $BLAZINGSQL_DIR
   cd $BLAZINGSQL_DIR
   git checkout $1   
   #FIX for Summit libcudacxx is not found with -isystem but with -I
   sed -i "s/'-isystem' + conda_env_inc_libcudacxx/'-I' + conda_env_inc_libcudacxx/g" engine/setup.py
   export CUDACXX=$CUDA_DIR/bin/nvcc
   export GPU_ARCHS="70"
   export CMAKE_CUDA_ARCHITECTURES="70"
   #setting maven
   export PATH=$CONDA_PREFIX/apache-maven-3.6.3/bin:$PATH
   export JAVA_HOME=$CONDA_PREFIX
   ./build.sh -t disable-aws-s3 disable-google-gs disable-mysql disable-sqlite disable-postgresql
fi
