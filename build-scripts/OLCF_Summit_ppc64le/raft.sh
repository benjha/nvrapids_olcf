#!/bin/bash

if [ "$1" == "" ]; then
    echo "Specify RAFT version"
    echo "example: "
    echo "    ./raft.sh v0.19.0a"
else
   RAFT_DIR=raft_$1
   # git clone https://github.com/rapidsai/raft.git $RAFT_DIR
   cd $RAFT_DIR
   # git checkout $1
   export GTEST_ROOT=$CONDA_PREFIX
   ./build.sh cppraft pyraft --nvtx
fi
