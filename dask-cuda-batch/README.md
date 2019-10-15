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

### Step 1. Launching the dask-scheduler and dask-cuda-workers

The next script launches the dask-scheduler in a batch node and two dask-cuda-workers in two compute nodes, 

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

DASK-cuda cluster connection information will be stored in `my-scheduler-gpu.json` file. See Step 2 for further instructions.

For a detailed explanation of dask-scheduler options, consult the next link:

https://docs.dask.org/en/stable/setup/cli.html

For a detailed explanation of dask-cuda-worker type the next command:

```
$dask-cuda-worker --help
```

For a detailed explanation of jsrun options, consult the next link:

https://www.olcf.ornl.gov/for-users/system-user-guides/summit/summit-user-guide/#running-jobs

## Step 2. Get your code know about the DASK-cuda cluster

Once the script in Step 1. has passed through the  SUMMIT's batch queue and is running. You can submit your workload to the
DASK-cuda cluster by calling your script, in this example, from the login node:

```
$python verify_dask_cuda_worker.py
```

Your python script, in this case `verify_dask_cuda_worker.py`, should include the next python lines to connect to the DASK scheduler:

```
import os
from dask.distributed import Client

if __name__ == '__main__': 
    file = os.getenv('MEMBERWORK') + '/gen119/my-scheduler-gpu.json'
    print (file)
    client = Client(scheduler_file=file)
    print("client information ",client)
    print("Done!") 

```

After executing `verify_dask_cuda_worker.py` script, you output should be similar to this:

```
$python verify_dask_cuda_worker.py 
client information  <Client: scheduler='tcp://10.41.0.44:8786' processes=12 cores=72>
Done!
```

#### NOTES

Likely, your workload will require some compute intensive activity before connecting to the DASK-cuda cluster, thus is important
for you to consider to run your python script in a batch job.

### Step 3. Adapting DASK-cuda cluster dynamically


