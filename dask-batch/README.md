## Instructions

The next instructions applies to NVIDIA Rapids ver. 0.9 and are intended for SUMMIT's users in GEN119 project, however
they can be used by other projects by changing the directory paths accordingly.

Running DASK distributed workloads requires a DASK cluster. Setting up a DASK cluster in SUMMIT needs three components: 
dask-scheduler, dask--workers and python calls in your python script to connect to the DASK cluster.

The next steps describe one of several ways to launch a DASK cluster in SUMMIT using its custom LSF scheduler. 
In this particular case, a dask-scheduler is run in a batch node and dask-cuda-workers are run in compute nodes, then
additional dask-workers are spawn by submitting new batch jobs.

You might need to adapt these steps according to your needs, but it is desirable not to run dask-scheduler nor
dask-workers in SUMMIT's login nodes.

### Step 1. Launching the dask-scheduler and dask-workers

`launch_dask_cluster.lsf` script launches the dask-scheduler in a batch node and four dask-workers in two compute nodes:

```
#!/usr/bin/env bash

#BSUB -P ABC123
#BSUB -W 1:00
#BSUB -alloc_flags "gpumps"
#BSUB -nnodes 4
#BSUB -J dask_worker
#BSUB -o dask_worker.o%J
#BSUB -e dask_worker.e%J
JOB_ID=${LSB_JOBID%.*}

module load gcc/6.4.0
module load cuda/10.1.168
module load cmake/3.14.2
module load boost/1.66.0
module load netlib-lapack/3.8.0

export PATH=/gpfs/alpine/proj-shared/gen119/gcc_6.4.0/anaconda3/bin:$PATH
export NUMBAPRO_NVVM=/sw/summit/cuda/10.1.168/nvvm/lib64/libnvvm.so
export NUMBAPRO_LIBDEVICE=/sw/summit/cuda/10.1.168/nvvm/libdevice

dask-scheduler --interface ib0 --scheduler-file $MEMBERWORK/gen119/my-scheduler.json --local-directory $MEMBERWORK/gen119/scheduler &

jsrun -c 42 -g 6 -n 4 -r 1 -a 1 --bind rs dask-worker --scheduler-file $MEMBERWORK/gen119/my-scheduler.json --nthreads 42  --memory-limit 512GB  --nanny --death-timeout 60 --interface ib0 --local-directory $MEMBERWORK/gen119/worker
```

#### NOTES

DASK cluster connection information will be stored in `my-scheduler.json` file. See Step 2 for further instructions.

For a detailed explanation of dask-scheduler options, consult the next link:

https://docs.dask.org/en/stable/setup/cli.html

For a detailed explanation of dask-workers, consult the next link:

https://distributed.dask.org/en/latest/worker.html

For a detailed explanation of jsrun options, consult the next link:

https://www.olcf.ornl.gov/for-users/system-user-guides/summit/summit-user-guide/#job-launcher-(jsrun)

##### CPU Affinity with jsrun

The jsrun `--bind` flag defaults to "packed:1", which results in all threads of a dask-worker process to be bound to a 
single physical core while remaining cores are left idle. Oversubscription is solved by using `--bind rs` flag to set 
all threads to the resource set.

On the other hand, on some Anaconda versions, NumPy will cause NumPy/OpenBLAS to try and bind the entire dask-worker process to a single physical core. This can be avoided by using `export OMP_PROC_BIND=FALSE` in the submission script's export section.
Further discussion on this topic can be found in:

https://stackoverflow.com/questions/15639779/why-does-multiprocessing-use-only-a-single-core-after-i-import-numpy

`test_affinity.py` is a simple python script to test CPU Affinity.

### Step 2. Get your code know about the DASK cluster

Once the script in Step 1. has passed through the SUMMIT's batch queue and is running. You can submit your workload to the DASK cluster by calling your script, in this example, from the login node:

```
$python verify_dask_cluster.py
```

Your python script, in this case `verify_dask_cluster.py`, should include the next python lines to connect to the DASK scheduler:

```
import os
from dask.distributed import Client

if __name__ == '__main__': 
    file = os.getenv('MEMBERWORK') + '/gen119/my-scheduler.json'
    client = Client(scheduler_file=file)
    print("client information ",client)
    print("Done!") 
```

After executing `verify_dask_cuda_worker.py` script, your output should be similar to this:

```
$python verify_dask_worker.py
client information  <Client: scheduler='tcp://10.41.0.45:8786' processes=4 cores=168>
Done!
```

#### NOTES

Likely, your workload will require some compute intensive activity before connecting to the DASK-cuda cluster, thus is important for you to consider to run your python script using a batch job.

### Step 3. Growing the DASK-cuda cluster

It is possible to grow and shrink Dask clusters based on current use. However, in contrast to DASK's built-in adaptive  method, you can grow your DASK cluster by submitting additional batch jobs after Step 1. is completed or shrink it by manually killing your running jobs accordingly.

`launch_dask_workers.lsf` script adds two new workers to your DASK cluster:

```
#!/usr/bin/env bash

#BSUB -P ABC123
#BSUB -W 1:00
#BSUB -alloc_flags "gpumps"
#BSUB -nnodes 2
#BSUB -J dask_worker
#BSUB -o dask_worker.o%J
#BSUB -e dask_worker.e%J
JOB_ID=${LSB_JOBID%.*}

module load gcc/6.4.0
module load cuda/10.1.168
module load cmake/3.14.2
module load boost/1.66.0
module load netlib-lapack/3.8.0

export PATH=/gpfs/alpine/proj-shared/gen119/gcc_6.4.0/anaconda3/bin:$PATH
export NUMBAPRO_NVVM=/sw/summit/cuda/10.1.168/nvvm/lib64/libnvvm.so
export NUMBAPRO_LIBDEVICE=/sw/summit/cuda/10.1.168/nvvm/libdevice

jsrun -c 42 -g 6 -n 2 -r 1 -a 1 --bind rs dask-worker --scheduler-file $MEMBERWORK/gen119/my-scheduler.json --nthreads 42  --memory-limit 512GB  --nanny --death-timeout 60 --interface ib0 --local-directory $MEMBERWORK/gen119/worker
```


#### NOTES

Consider OLCF's scheduling policy when submitting jobs. Smaller jobs may be dispachted first than larger ones. For more information, consult the next link:

https://www.olcf.ornl.gov/for-users/system-user-guides/summit/summit-user-guide/#scheduling-policy

