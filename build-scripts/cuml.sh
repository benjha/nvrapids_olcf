#!/bin/bash

if [ "$1" == "" ]; then
    echo "Specify cuML version"
    echo "example: "
    echo "    ./cuml.sh v0.19.0"
else
   CUML_DIR=cuml_$1
#   git clone https://github.com/rapidsai/cuml.git $CUML_DIR
   cd $CUML_DIR
#   git checkout $1
   export CMAKE_GENERATOR="Unix Makefiles"
   ./build.sh libcuml cuml
   #./build.sh libcuml cuml --singlegpu
fi
