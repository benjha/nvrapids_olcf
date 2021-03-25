*************************************************************************************
NVIDIA RAPIDS
*************************************************************************************

Overview
========

`RAPIDS <https://rapids.ai/>`_ is a suite of libraries to execute end-to-end data science and analytics pipelines on GPUs. RAPIDS utilizes NVIDIA CUDA primitives for low-level compute optimization through user-friendly Python interfaces. An overview of the RAPIDS libraries available at OLCF is given next.

cuDF
----

cuDF is a Python GPU DataFrame library (built on the Apache Arrow columnar memory format) for loading, joining, aggregating, filtering, and otherwise manipulating data.

cuML
----

cuML is a suite of libraries that implement machine learning algorithms and mathematical primitives functions that share compatible APIs with other RAPIDS projects.

cuGraph
-------

cuGraph is a GPU accelerated graph analytics library, with functionality like NetworkX, which is seamlessly integrated into the RAPIDS data science platform.

dask-cuda
---------

dask-cuda extends Dask where it is necessary to scale up and scale out RAPIDS workflows.

CuPy
----

Chainer's CuPy is a NumPy-compatible, open source mathematical library. While CuPy is not a library under the RAPIDS framework, it is compatible with RAPIDS and dask-cuda for memory management and multi-GPU, multi-node workload distribution.

Additional information is available at the `official RAPIDS documentation <https://docs.rapids.ai/api>`_ and `CuPy's documentation <https://docs.cupy.dev/en/stable/overview.html>`_.

Getting Started
===============

RAPIDS is available at OLCF via `Jupyter <https://docs.olcf.ornl.gov/services_and_applications/jupyter/overview.html#example-creating-a-conda-environment-for-rapids>`_ and via ``module load`` command in Summit. 

We recommend the use of Jupyter in example situations like:

- Python script preparation.
- Your workload fits comfortably on a single GPU.
- Interactive capabilities are needed. 

whereas Summit is recommended in example situations like:

- Your Python script has support for multi-gpu/multi-node execution via dask-cuda.
- Large workloads.
- Your Python script is single GPU but requires `concurrent job steps <https://docs.olcf.ornl.gov/systems/summit_user_guide.html?highlight=jsrun%20steps#concurrent-job-steps>`_.

RAPIDS on `Jupyter <https://docs.olcf.ornl.gov/services_and_applications/jupyter/overview.html>`_
==================

RAPIDS is provided in Jupyter following the next `instructions <https://docs.olcf.ornl.gov/services_and_applications/jupyter/overview.html#example-creating-a-conda-environment-for-rapids>`_.

Note that Python scripts prepared on Jupyter can be deployed on Summit if they use the same RAPIDS version. Use ``!jupyter nbconvert --to script my_notebook.ipynb`` to convert notebook files to Python scripts.

RAPIDS on Summit
================

RAPIDS is provided on Summit through the ``module load`` command:

.. code-block:: bash

    module load ums
    module load ums-gen119
    module load nvidia-rapids/0.18

The RAPIDS module loads ``gcc/7.4.0``, ``cuda/10.1.243`` and ``python/3.7.0-anaconda3-5.3.0`` modules. For a complete list of available packages, use ``conda list`` command after loading this module. 

The RAPIDS module also defines a set of environment variables to take advantage of `UCX <https://dask-cuda.readthedocs.io/en/latest/ucx.html>`_, an optimized communication framework for high-performance networking using Summit's NVLink and Infiniband communication interfaces.

RAPIDS basic execution
----------------------

As an example, the following LSF script will run a single-GPU RAPIDS script in one Summit node:

.. code-block:: bash

    #BSUB -P <PROJECT>
    #BSUB -W 0:05
    #BSUB -nnodes 1
    #BSUB -q batch
    #BSUB -J rapids_test
    #BSUB -o rapids_test_%J.out
    #BSUB -e rapids_test_%J.out

    module load ums
    module load ums-gen119
    module load nvidia-rapids/0.18

    jsrun --nrs 1 --tasks_per_rs 1 --cpu_per_rs 1 --gpu_per_rs 1 --smpiargs="off" \ 
          python $CONDA_PREFIX/examples/cudf/cudf_test.py

From the ``jsrun`` options, note the ``--smpiargs="off"`` flag is being used. Disabling smpiargs allows non Spectrum MPI codes run with CUDA.

Note this option is for illustrative purposes and not recommended to run RAPIDS on Summit since it underutilizes resources. If your RAPIDS code is single GPU, consider `Jupyter <https://docs.olcf.ornl.gov/services_and_applications/jupyter/overview.html#example-creating-a-conda-environment-for-rapids>`_ or the concurrent job steps option.

Concurrent job steps with RAPIDS
--------------------------------

In cases when a set of time steps need to be processed by single-GPU RAPIDS codes and each time step fits comfortably in GPU memory, it is recommended to execute `concurrent job steps <https://docs.olcf.ornl.gov/systems/summit_user_guide.html?highlight=jsrun%20steps#concurrent-job-steps>`_.

The following script provides a general pattern to run job steps concurrently with RAPIDS:

.. code-block:: bash

    #BSUB -P <PROJECT>
    #BSUB -W 0:05
    #BSUB -nnodes 1
    #BSUB -q batch
    #BSUB -J rapids_test
    #BSUB -o rapids_test_%J.out
    #BSUB -e rapids_test_%J.out

    module load ums
    module load ums-gen119
    module load nvidia-rapids/0.18

    jsrun --nrs 1 --tasks_per_rs 1 --cpu_per_rs 1 --gpu_per_rs 1 --smpiargs="off" \ 
          python /my_path/my_rapids_script.py dataset_part01 &
    jsrun --nrs 1 --tasks_per_rs 1 --cpu_per_rs 1 --gpu_per_rs 1 --smpiargs="off" \ 
          python /my_path/my_rapids_script.py dataset_part02 &
    jsrun --nrs 1 --tasks_per_rs 1 --cpu_per_rs 1 --gpu_per_rs 1 --smpiargs="off" \ 
          python /my_path/my_rapids_script.py dataset_part03 &
    ...
    wait

Distributed RAPIDS execution
----------------------------

Running RAPIDS distributed workloads (multi-gpu/multi-node) requires a dask-cuda cluster. Setting up a dask-cuda cluster on Summit requires two components:

- `dask-scheduler <https://docs.dask.org/en/latest/setup/cli.html#dask-scheduler>`_.
- `dask-cuda-workers <https://dask-cuda.readthedocs.io/en/latest/worker.html#worker>`_.

Once the dask-cluster is running, the RAPIDS script should `connect to <https://docs.dask.org/en/latest/setup/single-distributed.html?highlight=Client#client>`_  to the dask-cuda cluster. 

Reference of multi-gpu/multi-node operation with cuDF, cuML, cuGraph is available in the next links:

- `10 Minutes to cuDF and Dask-cuDF <https://docs.rapids.ai/api/cudf/stable/10min.html#>`_.
- `cuML Multi-Node, Multi-GPU Algorithms <https://docs.rapids.ai/api/cuml/stable/api.html#multi-node-multi-gpu-algorithms>`_.
- `Multi-GPU with cuGraph <https://docs.rapids.ai/api/cuml/stable/api.html#multi-node-multi-gpu-algorithms>`_.
https://docs.rapids.ai/api/cugraph/stable/dask-cugraph.html


