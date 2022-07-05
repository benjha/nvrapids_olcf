#!/bin/bash

export RAPIDS_VER=21.08
export PLATFORM=${PLATFORM:-ppc64le}
export BRANCH_VER=branch-$RAPIDS_VER
export ENV_NAME=nvrapids_cucim_${RAPIDS_VER}_gcc_9.3.0
export SUMMIT_ENV_DIR=/sw/summit/ums/gen119/nvrapids/bin/nvrapids_${RAPIDS_VER}_gcc_9.3.0
export CUSTOM_ENV_DIR=
export ENV_DIR=${CUSTOM_ENV_DIR:-$SUMMIT_ENV_DIR}
export SUMMIT_SRC_DIR=/sw/summit/ums/gen119/nvrapids/src/nvrapids_cucim_${RAPIDS_VER}_src
export CUSTOM_SRC_DIR=
export SRC_DIR=${CUSTOM_SRC_DIR:-$SUMMIT_SRC_DIR}
export YAML_SPEC=cucim_${RAPIDS_VER}_cuda11.0.3.yml
export UCX_VER=v1.9.0
export UCX_PY_VER=v0.21.0a
export MAVEN_VER=3.6.3
export FAISS_VER=1.7.0
export ARROW_VER=apache-arrow-4.0.1
export CUTENSOR_VER=1.3.0
export NCCL_VER=v2.9.9-1
export CUPY_VER=v9.2.0
export RMM_VER=$BRANCH_VER
export CUDF_VER=$BRANCH_VER
export DASK_CUDA_VER=$BRANCH_VER
export CUML_VER=$BRANCH_VER
export CUGRAPH_VER=$BRANCH_VER
export CUCIM_VER=$BRANCH_VER
export BSQL_VER=$BRANCH_VER

echo '---------Setting-up Anaconda'
#wget https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-${PLATFORM}.sh
#bash Anaconda3-2021.05-Linux-${PLATFORM}.sh -b -p $ENV_DIR

echo '---------Creating conda environment from ' $YAML_SPEC
#./create_conda_env.sh

echo 'Loading RAPIDS environment'
source load_rapids_dev.sh

echo '---------CONDA_PREFIX='$CONDA_PREFIX

echo '---------Installing RAPIDS dependencies '
echo
read -p "---------Press <enter> to continue"
echo

mkdir -p $SRC_DIR

cp *.sh $SRC_DIR
cd $SRC_DIR

echo '---------UCX ' $UCX_VER
#./ucx.sh $UCX_VER
#if [ $? -ne 0 ]; then
#    echo '---------UCX failed, cannot continue' 
#    exit 1
#fi

echo '---------UCX-PY ' $UCX_PY_VER
#./ucx-py.sh $UCX_PY_VER

echo '---------MAVEN ' $MAVEN_VER
#./maven.sh $MAVEN_VER

echo '---------FAISS ' $FAISS_VER
#./faiss.sh $FAISS_VER

echo '---------LIBcypher-parser v0.6.2'
#./libcypher-parser.sh

echo '---------ARROW ' $ARROW_VER
#./arrow.sh $ARROW_VER
#if [ $? -ne 0 ]; then
#    echo '---------ARROW failed, cannot continue' 
#    exit 1
#fi

echo
read -p "---------Press <enter> to continue"
echo

echo '---------CUTENSOR ' $CUTENSOR_VER
#./cutensor.sh $CUTENSOR_VER

echo '---------NCCL $NCCL_VER '
./nccl.sh $NCCL_VER

echo '---------CUPY ' $CUPY_VER
./cupy.sh $CUPY_VER

echo
read -p "---------Press <enter> to continue"
echo

echo '---------Installing RAPIDS '
echo '---------RMM ' $RMM_VER
#./rmm.sh $RMM_VER

echo '---------CUDF ' $CUDF_VER
#./cudf.sh $CUDF_VER

echo
read -p "---------Press <enter> to continue"
echo


echo '---------DASK-CUDA ' $DASK_CUDA_VER
#./dask-cuda.sh $DASK_CUDA_VER


echo '---------CUGRAPH ' $CUGRAPH_VER
#./cugraph.sh $CUGRAPH_VER

echo
read -p "---------Press <enter> to continue"
echo

echo '---------BSQL ' $BSQL_VER
#./blazingsql.sh $BSQL_VER

echo
read -p "---------Press <enter> to continue"
echo


echo '---------CUML ' $CUML_VER
#./cuml.sh $CUML_VER


echo
read -p "---------Press <enter> to continue"
echo

echo '---------JBIG '
#./jbig.sh

echo '---------CUCIM ' $CUCIM_VER
#./cucim.sh $CUCIM_VER
