#!/bin/bash

wget https://downloads.apache.org/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz
tar xvfz apache-maven-3.6.3-bin.tar.gz
mv apache-maven-3.6.3 $CONDA_PREFIX
