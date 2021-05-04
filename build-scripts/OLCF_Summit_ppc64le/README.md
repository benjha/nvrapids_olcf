# RAPIDS deployment on Summit

RAPIDS deployment involves three steps:

- Create a conda environment from a base environment and install ppc64le RAPIDS dependencies available in the conda-forge channel.
- Build from source and/or install RAPIDS dependencies that are not available in the conda-forge channel. Build from source and/or install RAPIDS dependencies that require optimizations.
- Build from source and install CuPy, RAPIDS and BlazingSQL.

## Manual deployment

### Setting-up RAPIDS environment

The script `create_conda_environment_rapids.sh` will create a new conda environment and install the ppc64le RAPIDS dependencies available in the conda-forge channel. Note that dependencies are listed in the `rapids_0.19_cuda11.0.3_ppc64le.yml` file.

Follow the next instructions to set-up the RAPIDS environment in your preferred path:

```
export ENV_DIR=<MY_PATH>
./create_conda_environment_rapids.sh
```

Note the script is using `python/3.7.0-anaconda3-5.3.0`.

### Setting-up the building environment

Once the RAPIDS environment has been created, we need to set-up the building environment. For this RAPIDS version, we are using GCC 9.3.0 and CUDA 11.0.3. The building environment is set-up by typing the next command:

```
source load_rapids_0.19_dev.sh
```

In addition to load the required modules and environment variables to build from source, `load_rapids_0.19_dev.sh` also activates the RAPIDS environment that previously was created in `ENV_DIR`.
