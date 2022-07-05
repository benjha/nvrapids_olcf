#!/bin/bash

if [ "$1" == "" ]; then
    echo "Specify  version"
    echo "example: "
    echo "    ./openslide-python.sh v1.1.2"
else
   OS_PY_DIR=openslide-python_$1
   git clone https://github.com/openslide/openslide-python.git $OS_PY_DIR
   cd $OS_PY_DIR
   git checkout $1
   python setup.py install --single-version-externally-managed --record /dev/null
fi
