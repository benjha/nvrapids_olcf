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

dask-cuda extends Dask where necessary to scale up and scale out RAPIDS workflows.

CuPy
----

Chainer's CuPy is a NumPy-compatible, open source mathematical library. While CuPy is not a library under the RAPIDS framework, it is compatible with RAPIDS and dask-cuda for memory management and multi-GPU, multi-node workload distribution.

A more detailed explanation of each library, capabilities and APIs is available in the `official RAPIDS documentation <https://docs.rapids.ai/api>`_ and `CuPy's documentation <https://docs.cupy.dev/en/stable/overview.html>`_.

Getting Started
===============

RAPIDS is available at OLCF via `Jupyter <https://docs.olcf.ornl.gov/services_and_applications/jupyter/overview.html#example-creating-a-conda-environment-for-rapids>`_ and via ``module load`` command in Summit. 

We recommend to use Jupyter in the next situations (but not limited to):

- Python script preparation.
- Your workload fits comfortably on a single GPU.
- Interactive capabilities are needed. 

whereas Summit is recommended in the next situtations (but not limited to):

- Your Python script is single gpu but requires `concurrent job steps <https://docs.olcf.ornl.gov/systems/summit_user_guide.html?highlight=jsrun%20steps#concurrent-job-steps>`_.
- Your Python script has support for multi-gpu/multi-node execution via dask-cuda.
- Large workloads.

RAPIDS on OLCF's Jupyter
========================

RAPIDS is provided in Jupyter following then next `instructions <https://docs.olcf.ornl.gov/services_and_applications/jupyter/overview.html#example-creating-a-conda-environment-for-rapids>`_.

Note this option is for illustrative purposes and not recommended to run RAPIDS on Summit since it underutilizes resources. If your RAPIDS code is single GPU, consider `Jupyter <https://docs.olcf.ornl.gov/services_and_applications/jupyter/overview.html#example-creating-a-conda-environment-for-rapids>`_ or the concurrent job steps option.

RAPIDS on Summit
================

RAPIDS is provided on Summit through the ``module load`` command:

.. code-block:: bash

    module load ums
    module load ums-gen119
    module load nvidia-rapids/0.18

The RAPIDS module loads ``gcc/7.4.0``, ``cuda/10.1.243`` and ``python/3.7.0-anaconda3-5.3.0`` modules. For a complete list of available packages, use ``conda list`` command after loading this module. 

The RAPIDS module also defines a set of environment variables to take advantage of `UCX <https://dask-cuda.readthedocs.io/en/latest/ucx.html>`_, an optimized communication framework for high-performance networking including Summit's NVLink and Infiniband communication interfaces.

RAPIDS basic execution
----------------

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

Note this option is for illustrative purposes and is not recommended to run RAPIDS since it underutilizes Summit's resources. If your RAPIDS code is single GPU, consider the concurrent job steps option.

Concurrent job steps with RAPIDS
--------------------------------

In cases (e.g. extract statistics) where the RAPIDS libraries are used to post-process datasets and each of the datasets' partition or time step fits comfortably in GPU memory. It is recommended to execute `concurrent job steps <https://docs.olcf.ornl.gov/systems/summit_user_guide.html?highlight=jsrun%20steps#concurrent-job-steps>`_ on each partition or time step.

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

Distributed RAPIDS LSF Script
-----------------------------


