#!/bin/bash

if [ "$1" == "" ]; then
    echo "Specify cuCIM version"
    echo "example: "
    echo "    ./cucim.sh v21.08"
else
   CUCIM_DIR=cucim_$1
   git clone https://github.com/rapidsai/cucim.git $CUCIM_DIR
   cd $CUCIM_DIR
   git checkout $1
   ./run build_local all release $CONDA_PREFIX
   python -m pip install python/cucim
fi
