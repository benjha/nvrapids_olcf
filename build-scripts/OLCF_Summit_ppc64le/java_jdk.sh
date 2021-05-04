#!/bin/bash

mkdir -p ibm-java-sdk-10
cd ibm-java-sdk-10

wget http://public.dhe.ibm.com/ibmdl/export/pub/systems/cloud/runtimes/java/11.0.10.0/linux/ppc64le/ibm-java-jdk_ppc64le_linux_11.0.10.0-archive.bin
chmod +x ibm-java-jdk_ppc64le_linux_11.0.10.0-archive.bin

echo INSTALLER_UI=silent &> installer.options
echo USER_INSTALL_DIR=$ENV_DIR/ibm-java-ppc64le-110 >> installer.options
echo LICENSE_ACCEPTED=TRUE >> installer.options

./ibm-java-jdk_ppc64le_linux_11.0.10.0-archive.bin -f installer.options
