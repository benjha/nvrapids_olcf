#!/bin/bash

export CONDA_PLATFORM=ppc64le
export CONDA_VER=2022.05

export ROOT_DIR=/sw/summit/ums/gen119/nvrapids
export CONDA_DIR=$ROOT_DIR/bin/anaconda-${CONDA_VER}

export RAPIDS_VER=v22.06.00
export CONDAENV_NAME=nvrapids-${RAPIDS_VER}
export CONDAENV_LOCATION="${CONDA_DIR}/envs/${CONDAENV_NAME}"

export SRC_DIR=$ROOT_DIR/src/nvrapids_${RAPIDS_VER}_src
export YAML_SPEC=rapids_22.06_cuda_11.5.yml
export UCX_VER=v1.12.1
export UCX_PY_VER=v0.26.00
export FAISS_VER=v1.7.0
export ARROW_VER=release-8.0.0
export CUTENSOR_VER=1.4.0
export NCCL_VER=v2.9.9-1
export CUPY_VER=v10.6.0
export MPI4PY_VER=3.1.1
export RMM_VER=$RAPIDS_VER
export CUDF_VER=$RAPIDS_VER
export DASK_CUDA_VER=$RAPIDS_VER
export CUML_VER=$RAPIDS_VER
export CUGRAPH_VER=$RAPIDS_VER
export RAFT_VER=$RAPIDS_VER
export CUCIM_VER=$RAPIDS_VER
export DASK_SQL_VER=2022.6.0

echo '---------Setting-up Anaconda'
#wget https://repo.anaconda.com/archive/Anaconda3-${CONDA_VER}-Linux-${CONDA_PLATFORM}.sh
#bash Anaconda3-${CONDA_VER}-Linux-${CONDA_PLATFORM}.sh -b -p $CONDA_DIR

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

echo
read -p "---------Press <enter> to continue"
echo

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
if [ $? -ne 0 ]; then
    echo '---------UCX-PY build failed, cannot continue'
    exit 1
fi

echo
read -p "---------Press <enter> to continue"
echo

echo '---------ARROW ' $ARROW_VER
#./arrow.sh $ARROW_VER
if [ $? -ne 0 ]; then
    echo '---------ARROW build failed, cannot continue' 
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


echo '---------NCCL ' $NCCL_VER
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

echo '---------DASK-CUDA ' $DASK_CUDA_VER
#./dask-cuda.sh $DASK_CUDA_VER
if [ $? -ne 0 ]; then
    echo '---------DASK CUDA build failed, cannot continue'
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

echo '---------RAFT ' $RAFT_VER
#./raft.sh $RAFT_VER
if [ $? -ne 0 ]; then
    echo '---------RAFT build failed, cannot continue'
    exit 1
fi

echo
read -p "---------Press <enter> to continue"
echo


echo '---------CUGRAPH ' $CUGRAPH_VER
./cugraph.sh $CUGRAPH_VER
if [ $? -ne 0 ]; then
    echo '---------CUGRAPH failed, cannot continue'
    exit 1
fi

echo
read -p "---------Press <enter> to continue"
echo

echo '---------DASK-SQL ' $DASK_SQL_VER
#./dask-sql.sh $BSQL_VER

echo
read -p "---------Press <enter> to continue"
echo


echo '---------CUML ' $CUML_VER
#./cuml.sh $CUML_VER

echo
read -p "---------Press <enter> to continue"
echo
echo '---------MPI4PY ' $MPI4PY_VER
#./mpi4py.sh $MPI4PY_VER


#echo '---------CUCIM ' $CUCIM_VER
#./cucim.sh $CUCIM_VER
