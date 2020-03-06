#!/usr/bin/env bash
#BSUB -P STF011
#BSUB -W 1:50
#BSUB -alloc_flags "gpumps"
#BSUB -nnodes 4
#BSUB -J xgboost
#BSUB -o xgb.o%J
#BSUB -e xgb.e%J

NODES=$(cat ${LSB_DJOB_HOSTFILE} | sort | uniq | grep -v login | grep -v batch | wc -l)
module load gcc/6.4.0
module load cuda/10.1.168
export PATH=$WORLDWORK/stf011/nvrapids_0.11_gcc_6.4.0/bin:$PATH
export PYTHONPATH=$WORLDWORK/stf011/junqi/rapids/xgboost/python-package:$PYTHONPATH


mkdir -p scratch 
export WORKDIR=$(pwd)/scratch 
rm -rf $WORKDIR/*

MASTER=$(cat ${LSB_DJOB_HOSTFILE} | grep -v login | grep -v batch | head -1)

ssh $MASTER LD_LIBRARY_PATH=$LD_LIBRARY_PATH PATH=$PATH dask-scheduler --interface ib0 --scheduler-file $WORKDIR/my-scheduler-gpu.json --local-directory $WORKDIR &
#jsrun -n1 -a1 -c1 -r1 dask-scheduler --interface ib0 --scheduler-file $WORKDIR/my-scheduler-gpu.json --local-directory $WORKDIR &

#sleep 10

jsrun -n${NODES} -a1 -c42 -g6 --smpiargs="off" -b none -r1 dask-cuda-worker --scheduler-file $WORKDIR/my-scheduler-gpu.json  --local-directory $WORKDIR  --nthreads 7 --memory-limit 80GB --device-memory-limit 16GB  --death-timeout 60 --interface ib0 & 

#jsrun -n${NODES} -a1 -c42 -g6 -r1 --bind rs dask-cuda-worker --scheduler-file $WORKDIR/my-scheduler.json --nthreads 42  --memory-limit 512GB  --nanny --death-timeout 60 --interface ib0 --local-directory $WORKDIR

#sleep 10

ssh $MASTER LD_LIBRARY_PATH=$LD_LIBRARY_PATH PATH=$PATH WORKDIR=$WORKDIR PYTHONPATH=$PYTHONPATH python -u $(pwd)/rapids_xgboost.py --nrows 80000000 --npartitions $((NODES*6))
#ssh $MASTER LD_LIBRARY_PATH=$LD_LIBRARY_PATH PATH=$PATH WORKDIR=$WORKDIR PYTHONPATH=$PYTHONPATH python -u $(pwd)/rapids_xgboost.py --nrows 4000000 --npartitions $((NODES*6))

