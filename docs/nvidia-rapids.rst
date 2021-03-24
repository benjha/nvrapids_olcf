*************************************************************************************
NVIDIA RAPIDS
*************************************************************************************

Overview
========

`RAPIDS <https://rapids.ai/>`_ is a suite of libraries to execute end-to-end data science and analytics pipelines on GPUs. RAPIDS utilizes NVIDIA CUDA primitives for low-level compute optimization through user-friendly Python interfaces.

An overview of the RAPIDS libraries available at OLCF is given next. A more detailed explanation of each library, capabilities and APIs is available in the `official RAPIDS documentation <https://docs.rapids.ai/api>`_.

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

Getting Started
===============

RAPIDS is available at OLCF via `Jupyter <https://docs.olcf.ornl.gov/services_and_applications/jupyter/overview.html#example-creating-a-conda-environment-for-rapids>`_ and via ``module load`` command in Summit. 

We recommend to use Jupyter in the next situations:

- Script preparation.
- Workload fits comfortably on a single GPU.
- Interactive capabilities are needed. 

whereas Summit is recommended in the next situtations:

- Script has support for multi-gpu/multi-node execution via dask-cuda.
- Large workloads.  


RAPIDS is provided on Summit through the ``module load`` command:

.. code-block:: bash

    module load ums
    module load ums-gen119
    module load nvidia-rapids/0.18

The RAPIDS module loads ``gcc/7.4.0``, ``cuda/10.1.243`` and ``python/3.7.0-anaconda3-5.3.0`` modules. This module includes cuDF, a pandas-like dataframe manipulation library; cuML, a collection of machine learning libraries that will provide GPU versions of algorithms available in scikit-learn; cuGraph, a NetworkX-like accelerated graph analytics library; and dask-cuda, for RAPIDS multi-gpu and multi-node GPU workloads. For a complete list of available packages, use ``conda list`` command after loading the RAPIDS module.


