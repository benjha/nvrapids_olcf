#!/usr/bin/env bash

#BSUB -P ABC123
#BSUB -W 1:00
#BSUB -alloc_flags "gpumps smt4"
#BSUB -nnodes 1
#BSUB -J dask_cuda_cupy_cluster
#BSUB -o dask_cuda_cupy_cluster.o%J
#BSUB -e dask_cuda_cupy_cluster.e%J

PROJ_ID=stf011

module load gcc/6.4.0
module load cuda/10.1.168

export PATH=$WORLDWORK/stf011/nvrapids_0.11_gcc_6.4.0/bin:$PATH
export CUPY_CACHE_DIR=$MEMBERWORK/$PROJ_ID
export OMP_PROC_BIND=FALSE

dask-scheduler --interface ib0 --scheduler-file $MEMBERWORK/$PROJ_ID/my-scheduler-gpu.json --local-directory $MEMBERWORK/$PROJ_ID &

jsrun -c 1 -g 6 -n 1 -r 1 -a 1 --bind rs --smpiargs="off" dask-cuda-worker --scheduler-file $MEMBERWORK/$PROJ_ID/my-scheduler-gpu.json  --local-directory $MEMBERWORK/$PROJ_ID  --nthreads 1 --memory-limit 85GB --device-memory-limit 16GB  --death-timeout 60 --interface ib0 --enable-nvlink
