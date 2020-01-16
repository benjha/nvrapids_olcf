
#TODO: UPDATE this


# Instructions

The next instructions applies to NVIDIA Rapids ver. 0.11 and are intended for any SUMMIT's user, however you need to 
modify the scripts according to your project ID.

## Conda environment for DASK and NVIDIA Rapids users

DASK and NVIDIA Rapids has been deployed in a conda enviroment available in:

```
$WORLDWORK/stf011/nvrapids_0.11_gcc_6.4.0
```

You can activate this environment by first loading the next modules:

```
module load gcc/6.4.0
module load cuda/10.1.168
module load python/3.7.0-anaconda3-5.3.0
```

and then use the `source activate` command:

```
source activate $WORLDWORK/stf011/nvrapids_0.11_gcc_6.4.0
```

to deactivate the environment type:

```
source deactivate

```

## Running a DASK cluster in SUMMIT

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
PROJ_ID=stf011

module load gcc/6.4.0
module load cuda/10.1.168

export PATH=$WORLDWORK/stf011/nvrapids_0.11_gcc_6.4.0/bin:$PATH

dask-scheduler --interface ib0 --scheduler-file $MEMBERWORK/$PROJ_ID/my-scheduler.json --local-directory $MEMBERWORK/$PROJ_ID/scheduler &

jsrun -c 42 -g 6 -n 4 -r 1 -a 1 --bind rs dask-worker --scheduler-file $MEMBERWORK/$PROJ_ID/my-scheduler.json --nthreads 42  --memory-limit 512GB  --nanny --death-timeout 60 --interface ib0 --local-directory $MEMBERWORK/$PROJ_ID/worker

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

Once the script in Step 1. has passed through the SUMMIT's batch queue and is running, you can submit your workload to the DASK cluster. 

First you need to activate the conda environment as explained above, the you can call your script, in this example, from the login node:

```
$python verify_dask_cluster.py
```

Your python script, in this case `verify_dask_cluster.py`, should include the next python lines to connect to the DASK scheduler:

```
import os
from dask.distributed import Client

if __name__ == '__main__': 
    file = os.getenv('MEMBERWORK') + '/PROJ_ID/my-scheduler.json'
    client = Client(scheduler_file=file)
    print("client information ",client)
    print("Done!") 
#Next line will shutdown the DASK Cluster and eventually the LSF jobs
#    client.shutdown ()
```

After executing `verify_dask_cluster.py` script, your output should be similar to this:

```
$python verify_dask_worker.py
client information  <Client: scheduler='tcp://10.41.0.45:8786' processes=4 cores=168>
Done!
```

#### NOTES

Likely, your workload will require some compute intensive activity before connecting to the DASK cluster, thus is important for you to consider to run your python script using a batch job.

### Step 3. Growing the DASK-cuda cluster

It is possible to grow and shrink Dask clusters based on current use. However, in contrast to DASK's built-in adaptive  method, you can grow your DASK cluster by submitting additional batch jobs after Step 1. is completed or shrink it by manually killing your running jobs accordingly.

`launch_dask_workers.lsf` script adds two new workers to your DASK cluster:

```
#!/usr/bin/env bash

#BSUB -P STF011
#BSUB -W 1:00
#BSUB -alloc_flags "gpumps"
#BSUB -nnodes 2
#BSUB -J dask_worker
#BSUB -o dask_worker.o%J
#BSUB -e dask_worker.e%J

JOB_ID=${LSB_JOBID%.*}
PROJ_ID=stf011

module load gcc/6.4.0
module load cuda/10.1.168

export PATH=$WORLDWORK/stf011/nvrapids_0.11_gcc_6.4.0/bin:$PATH

jsrun -c 42 -g 6 -n 2 -r 1 -a 1 --bind rs dask-worker --scheduler-file $MEMBERWORK/$PROJ_ID/my-scheduler.json --nthreads 42  --memory-limit 512GB  --nanny --death-timeout 60 --interface ib0 --local-directory $MEMBERWORK/$PROJ_ID/worker
```


#### NOTES

Consider OLCF's scheduling policy when submitting jobs. Smaller jobs may be dispachted first than larger ones. For more information, consult the next link:

https://www.olcf.ornl.gov/for-users/system-user-guides/summit/summit-user-guide/#scheduling-policy

