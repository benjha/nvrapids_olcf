*************************************************************************************
BlazingSQL
*************************************************************************************

Overview
========

`BlazingSQL <https://blazingsql.com/>`_ provides a high-performance distributed SQL engine in Python. Built on the RAPIDS GPU data science ecosystem, ETL massive datasets on GPUs.

Getting Started
===============

BlazingSQL is available at OLCF via `Jupyter <https://docs.olcf.ornl.gov/services_and_applications/jupyter/overview.html#example-creating-a-conda-environment-for-rapids>`_ and via ``module load`` command in Summit. 

We recommend the use of Jupyter in example situations like:

- Python script preparation.
- Workload fits comfortably on a single GPU (NVIDIA V100 16GB).
- Interactive capabilities needed. 

whereas Summit is recommended in example situations like:

- Large workloads.
- Long runtimes on Summit's high memory nodes.
- Your Python script has support for multi-gpu/multi-node execution via dask-cuda.
- Your Python script is single GPU but requires `concurrent job steps <https://docs.olcf.ornl.gov/systems/summit_user_guide.html?highlight=jsrun%20steps#concurrent-job-steps>`_.

BlazingSQL on `Jupyter <https://docs.olcf.ornl.gov/services_and_applications/jupyter/overview.html>`_
======================

BlazingSQL is provided in Jupyter following  `these instructions <https://docs.olcf.ornl.gov/services_and_applications/jupyter/overview.html#example-creating-a-conda-environment-for-rapids>`_.

Note that Python scripts prepared on Jupyter can be deployed on Summit if they use the same RAPIDS version. Use ``!jupyter nbconvert --to script my_notebook.ipynb`` to convert notebook files to Python scripts.

BlazingSQL on Summit
====================

BlazingSQL is provided on Summit through the ``module load`` command:

.. code-block:: bash

    module load ums
    module load ums-gen119
    module load nvidia-rapids/0.18

The BlazingSQL module loads ``gcc/7.4.0``, ``cuda/10.1.243`` and ``python/3.7.0-anaconda3-5.3.0`` modules. For a complete list of available packages, use ``conda list`` command after loading these modules. 

The BlazingSQL module also defines a set of environment variables to take advantage of `UCX <https://dask-cuda.readthedocs.io/en/latest/ucx.html>`_, an optimized communication framework for high-performance networking using Summit's NVLink and Infiniband communication interfaces.

BlazingSQL basic execution
--------------------------

As an example, the following LSF script will run a single-GPU BlazingSQL script in one Summit node:

.. code-block:: bash

    #BSUB -P <PROJECT>
    #BSUB -W 0:05
    #BSUB -nnodes 1
    #BSUB -q batch
    #BSUB -J bsql_test_
    #BSUB -o bsql_test_%J.out
    #BSUB -e bsql_test_%J.out

    module load ums
    module load ums-gen119
    module load nvidia-rapids/0.18

    jsrun --nrs 1 --tasks_per_rs 1 --cpu_per_rs 1 --gpu_per_rs 1 --smpiargs="-disable_gpu_hooks" \ 
          python $CONDA_PREFIX/examples/blazingsql/bsql_test.py

From the ``jsrun`` options, note the ``--smpiargs="-disable_gpu_hooks"`` flag is being used. Disabling gpu hooks allows non Spectrum MPI codes run with CUDA.

Note the "BlazingSQL basic execution" option is for illustrative purposes and not recommended to run BlazingSQL on Summit since it underutilizes resources. If your BlazingSQL code is single GPU, consider `Jupyter <https://docs.olcf.ornl.gov/services_and_applications/jupyter/overview.html#example-creating-a-conda-environment-for-rapids>`_ or the concurrent job steps option.

Concurrent job steps with BlazingSQL
------------------------------------

In cases when a set of time steps need to be processed by single-GPU BlazingSQL codes and each time step fits comfortably in GPU memory, it is recommended to execute `concurrent job steps <https://docs.olcf.ornl.gov/systems/summit_user_guide.html?highlight=jsrun%20steps#concurrent-job-steps>`_.

The following script provides a general pattern to run job steps concurrently with BlazingSQL:

.. code-block:: bash

    #BSUB -P <PROJECT>
    #BSUB -W 0:05
    #BSUB -nnodes 1
    #BSUB -q batch
    #BSUB -J bsql_test_
    #BSUB -o bsql_test_%J.out
    #BSUB -e bsql_test_%J.out

    module load ums
    module load ums-gen119
    module load nvidia-rapids/0.18

    jsrun --nrs 1 --tasks_per_rs 1 --cpu_per_rs 1 --gpu_per_rs 1 --smpiargs="-disable_gpu_hooks" \ 
          python /my_path/my_bsql_script.py dataset_part01 &
    jsrun --nrs 1 --tasks_per_rs 1 --cpu_per_rs 1 --gpu_per_rs 1 --smpiargs="-disable_gpu_hooks" \ 
          python /my_path/my_bsql_script.py dataset_part02 &
    jsrun --nrs 1 --tasks_per_rs 1 --cpu_per_rs 1 --gpu_per_rs 1 --smpiargs="-disable_gpu_hooks" \ 
          python /my_path/my_bsql_script.py dataset_part03 &
    ...
    wait

Be aware of different OLCF's queues and scheduling policies to make best use of `regular <https://docs.olcf.ornl.gov/systems/summit_user_guide.html#job-priority-by-processor-count>`_ and `high memory <https://docs.olcf.ornl.gov/systems/summit_user_guide.html#batch-hm-queue-policy>`_ Summit nodes.

Distributed BlazingSQL execution
--------------------------------

Preliminaries
^^^^^^^^^^^^^

Running BlazingSQL multi-gpu/multi-node workloads requires a dask-cuda cluster. Setting up a dask-cuda cluster on Summit requires two components:

- `dask-scheduler <https://docs.dask.org/en/latest/setup/cli.html#dask-scheduler>`_.
- `dask-cuda-workers <https://dask-cuda.readthedocs.io/en/latest/worker.html#worker>`_.

Once the dask-cluster is running, the BlazingSQL script should perform five main tasks:
1. Create a dask client to connect to the dask-scheduler
2. Create a BlazingContext that takes in the dask client
3. Create some tables
4. Run queries
5. Shutting down the dask-cuda-cluster


Launching the dask-scheduler and dask-cuda-workers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following script will run a dask-cuda cluster on two compute nodes, then it executes a Python script running BlazingSQL.

.. code-block:: bash

    #BSUB -P <PROJECT>
    #BSUB -W 0:05
    #BSUB -alloc_flags NVME
    #BSUB -nnodes 3
    #BSUB -J bsql_dask_test_tcp
    #BSUB -o bsql_dask_test_tcp_%J.out
    #BSUB -e bsql_dask_test_tcp_%J.out

    PROJ_ID=<project>

    module load ums
    module load ums-gen119
    module load nvidia-rapids/0.18

    SCHEDULER_DIR=$MEMBERWORK/$PROJ_ID/dask
    WORKER_DIR=/mnt/bb/$USER

    if [ ! -d "$SCHEDULER_DIR" ]
    then
        mkdir $SCHEDULER_DIR
    fi

    SCHEDULER_FILE=$SCHEDULER_DIR/my-scheduler.json

    echo 'Running scheduler'
    jsrun -n 1 -g 1 -a 1 -c 2  --smpiargs="-disable_gpu_hooks" -D UCX_MEM_MMAP_HOOK_MODE \
        dask-scheduler --interface ib0 \
                        --scheduler-file $SCHEDULER_FILE \
                        --no-dashboard --no-show &

    #Wait for the dask-scheduler to start
    sleep 10

    echo 'Running workers'

    jsrun -n 2 -a 1 -g 6 -c 4 -b rs --smpiargs="-disable_gpu_hooks" -D UCX_MEM_MMAP_HOOK_MODE \
      dask-cuda-worker --nthreads 1 --memory-limit 82GB --device-memory-limit 16GB --rmm-pool-size=15GB \
                       --death-timeout 60  --interface ib0 --scheduler-file $SCHEDULER_FILE --local-directory $WORKER_DIR \
                       --no-dashboard &


    #Wait for WORKERS
    sleep 10 

    python -u $CONDA_PREFIX/examples/blazingsql/bsql_test_multi.py $SCHEDULER_FILE
    
    wait

    #clean DASK files
    rm -fr $SCHEDULER_DIR

    echo "Done!"
   
Note twelve dask-cuda-workers are executed, one per each available GPU, ``--memory-limit`` is set to 82 GB and  ``--device-memory-limit`` is set to 16 GB. If using Summit's high-memory nodes ``--memory-limit`` can be increased and setting ``--device-memory-limit`` to 32 GB  and ``--rmm-pool-size`` to 30 GB or so is recommended. Also note it is recommeded to wait some seconds for the dask-scheduler and dask-cuda-workers to start.

As mentioned earlier, the BlazingSQL code should perform five main tasks as shown in the following script. First, create a dask client to connect to the dask-scheduler; second create a BlazingContext that takes in the dask client; third create some tables; fourth run queries; fifth shutting down the dask-cuda-cluster.

.. code-block:: bash
    
    import sys
    import cudf
    from dask.distributed import Client
    from blazingsql import BlazingContext
    

    def disconnect(client, workers_list):
        client.retire_workers(workers_list, close_workers=True)
        client.shutdown()

    if __name__ == '__main__':

        sched_file = str(sys.argv[1]) #scheduler file
        
        # 1. Create a dask client to connect to the dask-scheduler
        client = Client(scheduler_file=sched_file)
        print("client information ",client)

        workers_info=client.scheduler_info()['workers']
        connected_workers = len(workers_info)
        print(str(connected_workers) + " workers connected")
        
        # 2. Create a BlazingContext that takes in the dask client
        # you want to set `allocator='existing'` if you are launching the dask-cuda-worker with an rmm memory pool
        bc = BlazingContext(dask_client = client, network_interface='ib0', allocator='existing')

        # 3. Create some tables
        bc.create_table('my_table','/data/file*.parquet')

        # 4. Run queries
        ddf = bc.sql('select count(*) from my_table')
        print(ddf.head())
        
        # 5. Shutting down the dask-cuda-cluster
        print("Shutting down the cluster")
        workers_list = list(workers_info)
        disconnect (client, workers_list)

Launching the dask-scheduler and dask-cuda-workers using UCX
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The BlazingSQL module was build with `UCX <https://dask-cuda.readthedocs.io/en/latest/ucx.html>`_, an optimized communication framework for high-performance networking, to support Summit's NVLink and Infiniband communication interfaces. 

Using UCX requires the use of the ``--protocol ucx`` option in the dask-scheduler call and, ``--enable-nvlink`` and ``--enable-infiniband`` options in the dask-cuda-worker call. Additionally you will want to set the environment variable BSQL_PROTOCOL=UCX.

.. code-block:: bash

    #BSUB -P <PROJECT>
    #BSUB -W 0:05
    #BSUB -alloc_flags NVME
    #BSUB -nnodes 2
    #BSUB -J bsql_dask_test_ucx
    #BSUB -o bsql_dask_test_ucx%J.out
    #BSUB -e bsql_dask_test_ucx%J.out

    PROJ_ID=<project>

    module load ums
    module load ums-gen119
    module load nvidia-rapids/0.18

    SCHEDULER_DIR=$MEMBERWORK/$PROJ_ID/dask
    WORKER_DIR=/mnt/bb/$USER

    if [ ! -d "$SCHEDULER_DIR" ]
    then
        mkdir $SCHEDULER_DIR
    fi

    SCHEDULER_FILE=$SCHEDULER_DIR/my-scheduler.json

    export BSQL_PROTOCOL=UCX

    echo 'Running scheduler'
    jsrun -n 1 -g 1 -a 1 -c 2  --smpiargs="-disable_gpu_hooks" -D UCX_MEM_MMAP_HOOK_MODE \
        dask-scheduler --interface ib0 \
                        --scheduler-file $SCHEDULER_FILE \
                        --no-dashboard --no-show &

    #Wait for the dask-scheduler to start
    sleep 10

    echo 'Running workers'

    jsrun -n 2 -a 1 -g 6 -c 4 -b rs --smpiargs="-disable_gpu_hooks" -D UCX_MEM_MMAP_HOOK_MODE \
        dask-cuda-worker --nthreads 1 --memory-limit 82GB --device-memory-limit 16GB --rmm-pool-size=15GB \
                        --death-timeout 60  --interface ib0 --scheduler-file $SCHEDULER_FILE --local-directory $WORKER_DIR \
                        --no-dashboard &

    #Wait for WORKERS
    sleep 60

    python -u $CONDA_PREFIX/examples/blazingsql/bsql_test_multi.py $SCHEDULER_FILE

    #clean DASK files
    rm -fr $SCHEDULER_DIR

    echo "Done!"

