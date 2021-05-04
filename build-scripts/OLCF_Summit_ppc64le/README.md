# RAPIDS deployment on Summit

RAPIDS deployment involves three steps:

- Create a conda environment from a base environment and install ppc64le RAPIDS dependencies available in the conda-forge channel.
- Build from source and/or install RAPIDS dependencies that are not available in the conda-forge channel. Build from source and/or install RAPIDS dependencies that require optimizations.
- Build from source and install RAPIDS and BlazingSQL.

## Manual deployment

### Setting-up RAPIDS

The script `create_conda_environment_rapids.sh` will create a new conda environment and install the ppc64le RAPIDS dependencies available in the conda-forge channel. Note that dependencies are listed in the `rapids_0.19_cuda11.0.3_ppc64le.yml` file.

Follow the next instructions to set-up the RAPIDS environment in your preferred path:

```
export ENV_DIR=<MY_PATH>
./create_conda_environment_rapids.sh
```
