#!/usr/bin/env bash

#BSUB -P STF011
#BSUB -W 1:00
#BSUB -alloc_flags "gpumps"
#BSUB -nnodes 4
#BSUB -J dask_ucx_cluster
#BSUB -o dask_ucx_cluster.o%J
#BSUB -e dask_ucx_cluster.e%J

PROJ_ID=stf011

module load gcc/6.4.0
module load cuda/10.1.168

export PATH=$WORLDWORK/stf011/nvrapids_0.11_gcc_6.4.0/bin:$PATH

dask-scheduler --interface ib0 --protocol ucx --scheduler-file $MEMBERWORK/$PROJ_ID/my-scheduler.json --local-directory $MEMBERWORK/$PROJ_ID/scheduler &

jsrun -c 42 -g 6 -n 4 -r 1 -a 1 --bind rs dask-worker --scheduler-file $MEMBERWORK/$PROJ_ID/my-scheduler.json --nthreads 42  --memory-limit 512GB  --nanny --death-timeout 60 --interface ib0 --protocol ucx --local-directory $MEMBERWORK/$PROJ_ID/worker
