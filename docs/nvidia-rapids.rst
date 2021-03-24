*************************************************************************************
NVIDIA RAPIDS
*************************************************************************************

`RAPIDS <https://rapids.ai/>`_ is a suite of libraries to execute end-to-end data science and analytics pipelines on GPUs. RAPIDS utilizes NVIDIA CUDA primitives for low-level compute optimization through user-friendly Python interfaces.

Getting Started
===============

RAPIDS is provided on Summit through the ``module load`` command:

.. code-block:: bash

    module load ums
    module load ums-gen119
    module load nvidia-rapids/0.18

The RAPIDS module loads ``gcc/7.4.0``, ``cuda/10.1.243`` and ``python/3.7.0-anaconda3-5.3.0`` modules. This module includes cuDF, a pandas-like dataframe manipulation library; cuML, a collection of machine learning libraries that will provide GPU versions of algorithms available in scikit-learn; cuGraph, a NetworkX-like accelerated graph analytics library; and Dask, for RAPIDS multi-gpu and multi-node GPU workloads. For a complete list of available packages, use ``conda list`` command after loading the RAPIDS module.

cudf
----

cuml
----

cugraph
-------


Recommeded Approach
===================


