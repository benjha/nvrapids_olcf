#!/usr/bin/env bash

#BSUB -P STF011
#BSUB -W 0:30
#BSUB -alloc_flags "gpumps smt4"
#BSUB -nnodes 1
#BSUB -J svd_cupy_1GPU
#BSUB -o svd_cupy_1GPU.o%J
#BSUB -e svd_cupy_1GPU.e%J
#BSUB -q batch-hm

module load gcc/7.4.0
module load python/3.7.0-anaconda3-5.3.0
module load cuda/10.1.243

#source activate /gpfs/alpine/world-shared/stf011/nvrapids_0.14_gcc_7.4.0


PROJ_ID=stf011
export PATH=$WORLDWORK/stf011/nvrapids_0.14_gcc_7.4.0/bin:$PATH
export CUPY_CACHE_DIR=$MEMBERWORK/$PROJ_ID/dask
export OMP_PROC_BIND=FALSE

cd /gpfs/alpine/world-shared/stf011/benjha/gtc_2020/dask_cupy/svd_perf_eval/rapids_0.14

jsrun -n 1 -r 1 -a 1 -c 1 -g 1 python -u svd_cupy.py
jsrun -n 1 -r 1 -a 1 -c 1 -g 1 python -u svd_cupy.py
jsrun -n 1 -r 1 -a 1 -c 1 -g 1 python -u svd_cupy.py
jsrun -n 1 -r 1 -a 1 -c 1 -g 1 python -u svd_cupy.py
jsrun -n 1 -r 1 -a 1 -c 1 -g 1 python -u svd_cupy.py
jsrun -n 1 -r 1 -a 1 -c 1 -g 1 python -u svd_cupy.py
jsrun -n 1 -r 1 -a 1 -c 1 -g 1 python -u svd_cupy.py
jsrun -n 1 -r 1 -a 1 -c 1 -g 1 python -u svd_cupy.py
jsrun -n 1 -r 1 -a 1 -c 1 -g 1 python -u svd_cupy.py
jsrun -n 1 -r 1 -a 1 -c 1 -g 1 python -u svd_cupy.py

#jskill all
