#!/bin/bash

if [ "$1" == "" ]; then
    echo "Specify RMM version"
    echo "example: "
    echo "    ./rmm.sh v0.19.0"
else
   RMM_DIR=rmm_$1
   git clone https://github.com/rapidsai/rmm.git $RMM_DIR
   cd $RMM_DIR
   git checkout $1
   ./build.sh librmm rmm
fi
