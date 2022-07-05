#!/bin/bash

export RAPIDS_VER=21.10
export PLATFORM=${PLATFORM:-ppc64le}
export BRANCH_VER=branch-$RAPIDS_VER

export ROOT_DIR=/sw/summit/ums/gen119/nvrapids
export ANACONDA_DIR=$ROOT_DIR/bin/anaconda-base

export CONDAENV_NAME=nvrapids-${RAPIDS_VER}
export CONDAENV_LOCATION="${ANACONDA_DIR}/envs/${CONDAENV_NAME}"

export SRC_DIR=$ROOT_DIR/src/nvrapids_${RAPIDS_VER}_src
export YAML_SPEC=rapids_${RAPIDS_VER}_cuda11.0.3.yml
export UCX_VER=v1.11.x
export UCX_PY_VER=v0.22.01
export MAVEN_VER=3.6.3
export FAISS_VER=v1.7.0
export ARROW_VER=apache-arrow-5.0.0
export CUTENSOR_VER=1.3.0
export NCCL_VER=v2.9.9-1
export CUPY_VER=v9.2.0
export MPI4PY_VER=3.1.1
export RMM_VER=$BRANCH_VER
export CUDF_VER=$BRANCH_VER
export DASK_CUDA_VER=$BRANCH_VER
export CUML_VER=$BRANCH_VER
export CUGRAPH_VER=$BRANCH_VER
export CUCIM_VER=$BRANCH_VER
export BSQL_VER=$BRANCH_VER

echo '---------Setting-up Anaconda'
#wget https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-${PLATFORM}.sh
#bash Anaconda3-2021.05-Linux-${PLATFORM}.sh -b -p $ANACONDA_DIR

echo '---------Creating conda environment from ' $YAML_SPEC
#./create_conda_env.sh

echo '---------Building C/C++ Libraries'
mkdir -p $SRC_DIR
cp *.sh $SRC_DIR
cp *.yml $SRC_DIR
cd $SRC_DIR

# UCX needs to build out of the environment
# to link with MOFED correctly, to link with correct ld
echo '---------UCX ' $UCX_VER
echo $UCX_DIR
#./ucx.sh $UCX_VER
if [ $? -ne 0 ]; then
    echo '---------UCX failed, cannot continue'
    exit 1
fi

echo '---------LIBcypher-parser v0.6.2'
#./libcypher-parser.sh
if [ $? -ne 0 ]; then
    echo '---------LIBcypher-parser failed, cannot continue'
    exit 1
fi

echo '---------FAISS ' $FAISS_VER
#./faiss.sh $FAISS_VER
if [ $? -ne 0 ]; then
    echo '---------FAISS failed, cannot continue'
    exit 1
fi


echo 'Loading RAPIDS environment'
source load_rapids_dev.sh
echo '---------CONDA_PREFIX='$CONDA_PREFIX

echo '---------Installing RAPIDS dependencies '
echo
read -p "---------Press <enter> to continue"
echo

echo '---------UCX-PY ' $UCX_PY_VER
#./ucx-py.sh $UCX_PY_VER

echo '---------MAVEN ' $MAVEN_VER
#./maven.sh $MAVEN_VER


echo
read -p "---------Press <enter> to continue"
echo

echo '---------ARROW ' $ARROW_VER
#./arrow.sh $ARROW_VER
if [ $? -ne 0 ]; then
    echo '---------ARROW failed, cannot continue' 
    exit 1
fi

echo
read -p "---------Press <enter> to continue"
echo

echo '---------CUTENSOR ' $CUTENSOR_VER
#./cutensor.sh $CUTENSOR_VER
if [ $? -ne 0 ]; then
    echo '---------CUTENSOR failed, cannot continue'
    exit 1
fi


echo '---------NCCL $NCCL_VER '
#./nccl.sh $NCCL_VER
if [ $? -ne 0 ]; then
    echo '---------NCCL failed, cannot continue'
    exit 1
fi


echo '---------CUPY ' $CUPY_VER
#./cupy.sh $CUPY_VER
if [ $? -ne 0 ]; then
    echo '---------CUPY failed, cannot continue'
    exit 1
fi

echo
read -p "---------Press <enter> to continue"
echo

echo '---------Installing RAPIDS '
echo '---------RMM ' $RMM_VER
#./rmm.sh $RMM_VER

if [ $? -ne 0 ]; then
    echo '---------RMM failed, cannot continue'
    exit 1
fi

echo '---------CUDF ' $CUDF_VER
#./cudf.sh $CUDF_VER
if [ $? -ne 0 ]; then
    echo '---------CUDF failed, cannot continue'
    exit 1
fi


echo
read -p "---------Press <enter> to continue"
echo


echo '---------DASK-CUDA ' $DASK_CUDA_VER
#./dask-cuda.sh $DASK_CUDA_VER


echo '---------CUGRAPH ' $CUGRAPH_VER
#./cugraph.sh $CUGRAPH_VER
if [ $? -ne 0 ]; then
    echo '---------CUGRAPH failed, cannot continue'
    exit 1
fi

echo
read -p "---------Press <enter> to continue"
echo

echo '---------BSQL ' $BSQL_VER
#./blazingsql.sh $BSQL_VER

echo
read -p "---------Press <enter> to continue"
echo


echo '---------CUML ' $CUML_VER
./cuml.sh $CUML_VER

echo
read -p "---------Press <enter> to continue"
echo
echo '---------MPI4PY ' $MPI4PY_VER
#./mpi4py.sh $MPI4PY_VER


#echo '---------CUCIM ' $CUCIM_VER
#./cucim.sh $CUCIM_VER
