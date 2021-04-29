#!/bin/bash

wget https://github.com/llvm/llvm-project/releases/download/llvmorg-8.0.1/clang+llvm-8.0.1-powerpc64le-linux-rhel-7.4.tar.xz
tar -xvf clang+llvm-8.0.1-powerpc64le-linux-rhel-7.4.tar.xz
cd clang+llvm-8.0.1-powerpc64le-linux-rhel-7.4
cp -rP * $CONDA_PREFIX

