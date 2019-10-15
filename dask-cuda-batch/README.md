## Instructions

The next instructions applies to NVIDIA Rapids ver. 0.9 and are intended for SUMMIT's users in GEN119 project, however
they can be used by other projects by changing the directory paths accordingly.

Running NVIDIA Rapids distributed workloads requires a DASK-cuda cluster. Setting up a DASK-cuda cluster in SUMMIT
needs three components: dask-cuda-scheduler, dask-cuda-workers and python calls in your python script to
connect to the DASK-cuda cluster.

The next steps describe one of several ways to launch a dask-cuda cluster in SUMMIT using its custom LSF scheduler. 
In this particular case, a dask-scheduler is run in a batch node and dask-cuda-workers are run in compute nodes, then
additional dask-cuda-workers are spawn by submitting new batch jobs.

You might need to adapt these steps according to your needs, but it is desirable not to run dask-scheduler nor
dask-cuda-workers in SUMMIT's login nodes.

### Step 1. 

The next script launches the dask-scheduler in a batch node and two dask-cuda-workers in two compute nodes:

```
#!/usr/bin/env bash
#BSUB -P ABC123
#BSUB -W 1:00
#BSUB -alloc_flags "gpumps"
#BSUB -nnodes 2
#BSUB -J dask_cuda_worker
#BSUB -o dask_cuda_worker.o%J
#BSUB -e dask_cuda_worker.e%J
JOB_ID=${LSB_JOBID%.*}

module load gcc/6.4.0
module load cuda/10.1.168
module load cmake/3.14.2
module load boost/1.66.0
module load netlib-lapack/3.8.0

export PATH=/gpfs/alpine/proj-shared/gen119/gcc_6.4.0/anaconda3/bin:$PATH
export NUMBAPRO_NVVM=/sw/summit/cuda/10.1.168/nvvm/lib64/libnvvm.so
export NUMBAPRO_LIBDEVICE=/sw/summit/cuda/10.1.168/nvvm/libdevice

hostname
dask-scheduler --interface ib0 --scheduler-file $MEMBERWORK/gen119/my-scheduler-gpu.json --local-directory $MEMBERWORK/gen119 &

jsrun -c 42 -g 6 -n 2 -r 1 -a 1 dask-cuda-worker --scheduler-file $MEMBERWORK/gen119/my-scheduler-gpu.json  --local-directory $MEMBERWORK/gen119  --nthreads 1 --memory-limit 100GB --device-memory-limit 16GB  --death-timeout 60 --interface ib0

```

#### NOTES

For a detailed explanation of dask-scheduler options, consult the next link:

https://docs.dask.org/en/stable/setup/cli.html

For a detailed explanation of dask-cuda-worker type the next command:

```
$dask-cuda-worker --help
```

For a detailed explanation of jsrun options, consult the next link:

https://www.olcf.ornl.gov/for-users/system-user-guides/summit/summit-user-guide/#running-jobs

