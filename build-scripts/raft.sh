#!/bin/bash

if [ "$1" == "" ]; then
    echo "Specify RAFT version"
    echo "example: "
    echo "    ./cugraph.sh v22.06.00"
else
   echo 'CONDA_PREFIX='$CONDA_PREFIX
   RAFT_DIR=raft_$1
   git clone https://github.com/rapidsai/raft.git $RAFT_DIR
   cd $RAFT_DIR

   export CMAKE_GENERATOR="Unix Makefiles"

   git checkout $1
   ./build.sh libraft --compile-libs --install

   echo
   read -p "---------Press <enter> to continue"
   echo

   ./build.sh pyraft --install
   ./build.sh pylibraft --install
fi
