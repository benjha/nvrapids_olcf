#!/bin/bash

if [ "$1" == "" ]; then
    echo "Specify cuTensor version"
    echo "example: "
    echo "    ./cutensor.sh 1.3.0"
    return 1
else
    CUTENSOR_PATH="libcutensor_${CUTENSOR_VER}"
    echo "cuTENSOR path: " $CUTENSOR_PATH

    if [ $CUTENSOR_VER = '1.4.0' ]; then
        CUTENSOR_MIN_VER=6
    elif [ $CUTENSOR_VER = '1.3.0' ]; then
        CUTENSOR_MIN_VER=3
    fi

    # old repo
    #wget https://developer.download.nvidia.com/compute/cutensor/${CUTENSOR_VER}/local_installers/libcutensor-linux-${PLATFORM}-${CUTENSOR_VER}.${CUTENSOR_MIN_VER}.tar.gz

    # new repo as 07072022
    wget https://developer.download.nvidia.com/compute/cutensor/redist/libcutensor/linux-ppc64le/libcutensor-linux-ppc64le-${CUTENSOR_VER}.${CUTENSOR_MIN_VER}-archive.tar.xz


    mkdir -p $CUTENSOR_PATH
    tar -xvf libcutensor-linux-ppc64le-${CUTENSOR_VER}.${CUTENSOR_MIN_VER}-archive.tar.xz -C $CUTENSOR_PATH

    cp -r $CUTENSOR_PATH/libcutensor-linux-ppc64le-${CUTENSOR_VER}.${CUTENSOR_MIN_VER}-archive/include/* $CONDA_PREFIX/include
    cp -P $CUTENSOR_PATH/libcutensor-linux-ppc64le-${CUTENSOR_VER}.${CUTENSOR_MIN_VER}-archive/lib/11.0/* $CONDA_PREFIX/lib
fi

