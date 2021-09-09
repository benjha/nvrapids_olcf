#!/bin/bash

JBIG_PATH="jbig_2.1"

wget https://www.cl.cam.ac.uk/~mgk25/jbigkit/download/jbigkit-2.1.tar.gz

mkdir -p $JBIG_PATH
tar -xvf jbigkit-2.1.tar.gz -C $JBIG_PATH
cd $JBIG_PATH/jbigkit-2.1
make lib

echo 'Installing jbig_2.1'
echo 'cp libjbig/*.a' ${CONDA_PREFIX}'/lib'
cp libjbig/*.a $CONDA_PREFIX/lib

echo 'cp libjbig/*.h' ${CONDA_PREFIX}'/include'
cp libjbig/*.h $CONDA_PREFIX/include
echo 'done!'
