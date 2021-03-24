# NVIDIA RAPIDS at OLCF

## Getting Started

NVIDIA RAPIDS is provided on Summit through the `module load` command:

```
module load ums
module load ums-gen119
module load nvidia-rapids/0.18
```

This repository is meant to share recipes to build, install, maintain and execute NVIDIA Rapids Framework in OLCF's SUMMIT
supercomputer.

## Repository Organization

This repository has the next directories:

- build-scripts

build-scripts directory includes scripts to build from source NVIDIA Rapids in SUMMIT.

- dask-batch

dask-batch directory includes scripts to execute DASK distributed workloads in batch mode.

- dask-cuda-batch

dask-cuda-batch directory  includes scripts to execute NVIDIA Rapids workloads with dask-cuda in batch mode.

## DISCLAIMER

The documentation and scripts of this repositiory are not suported by OLCF nor NVIDIA.
