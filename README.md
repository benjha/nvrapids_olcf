# NVIDIA RAPIDS at OLCF

This repository is meant to share recipes to build, install, maintain and execute NVIDIA RAPIDS in OLCF's SUMMIT supercomputer.

## Repository Organization

This repository includes the next directories:

- docs

[`docs`] provides documentation for the OLCF's user community to execute NVIDIA RAPIDS in Summit.

- examples

[`examples`] provides the LSF scripts and python examples discussed in the documentation.

- build-scripts

[`build-scripts`](https://github.com/benjha/nvrapids_olcf/tree/branch-0.18/build_scripts) directory includes scripts to build from source NVIDIA RAPIDS in Summit. This directory is meant to be used by mantainers.







## Getting Started

NVIDIA RAPIDS is provided on Summit through the `module load` command:

```
module load ums
module load ums-gen119
module load nvidia-rapids/0.18
```

This repository is meant to share recipes to build, install, maintain and execute NVIDIA Rapids Framework in OLCF's SUMMIT
supercomputer.

