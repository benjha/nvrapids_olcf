# RAPIDS deployment on Summit

RAPIDS deployment involves three steps:

- Create a conda environment from a base environment and install ppc64le RAPIDS dependencies available in the conda-forge channel.
- Build from source and/or install RAPIDS dependencies that are not available in the conda-forge channel. Build from source and/or install RAPIDS dependencies that require optimizations.
- Build from source and install CuPy, RAPIDS and BlazingSQL.

### Automatic deployment

`super_script.sh` packs all the scripts necessary to build from source and deploy RMM, cuDF, cuML, cuGRAPH, BLAZING SQL and CuPy. To start the installation process use the next command:

```
./super_script.sh
```

For your own deployments, you'll need to modify the environment variables defined at the beginning of this script. Hopefully all the directory paths are solved correctly and the build will succeed, otherwise feel free to add your own modifications that fits your system. Our intention is only to support clusters at the DOE's Leadership Computing Facilities.

The scripts are getting some generalization to support deployments on `ppc64le`, `armv8` and `x86_64` architectures. Currently, this script has been tested on OLCF's Summit supercomputer which is a ppc64le machine. 

To learn more about how this scipt works check the "Supervised deployment" section.

### Automatic deployment cuCIM

cuCIM 21.08 has different dependencies with respect to RAPIDS, thus it should be deployed in a different conda environment. To start its installation process use the next command:

```
./super_script_cucim.sh
```

For your own deployments, you'll need to modify the environment variables defined at the beginning of this script.

## Supervised deployment

Clone this repository in a temporal directory an go to `OLCF_Summit_ppc64le` directory.

```
git clone https://github.com/benjha/nvrapids_olcf.git tmp
cd tmp/build-scripts/OLCF_Summit_ppc64le
```

### Setting-up RAPIDS environment

The script `create_conda_environment_rapids.sh` will create a new conda environment and install the ppc64le RAPIDS dependencies available in the conda-forge channel. Note that dependencies are listed in the `rapids_21.08_cuda11.0.3.yml` file.

Follow the next instructions to set-up the RAPIDS environment in your preferred path:

```
export ENV_DIR=<MY_PATH>
./create_conda_environment_rapids.sh
```

Note the script is using `python/3.7.0-anaconda3-5.3.0`.

### Setting-up the building environment

Once the RAPIDS environment has been created, we need to set-up the building environment. For this RAPIDS version, we are using GCC 9.3.0 and CUDA 11.0.3. The building environment is set-up by typing the next command:

```
source load_rapids_dev.sh
```

In addition to load the required modules and environment variables to build from source, `load_rapids_dev.sh` also activates the RAPIDS environment that previously was created in `ENV_DIR`.

### Building and/or installing RAPIDS dependencies

Once the RAPIDS environment and the building environment is enabled, the next steps consist in building and/or installing RAPIDS dependencies that are not available in the conda-forge channel or require specific configurations from Summit.

Most of these dependencies are configured to be installed in `CONDA_PREFIX` directory.


#### Build/Install NCCL

This is a requirement for CuPy and RAPIDS.

```
./nccl.sh $NCCL_VER
```

#### Install cuTENSOR (requires nvidia developer account)

cuTENSOR 1.3.0 can't be distributable by third-parties thus you need to download it from developer.nvidia.com. This is a requirement for CuPy.

```
./cutensor.sh $CUTENSOR_VER
```

#### Build/Install CuPy 

This is a requirement for RAPIDS.

```
./cupy.sh $CUPY_VER
```

#### Build/Install UCX

This is a requirement for RAPIDS and Blazing SQL.

```
./ucx.sh UCX_VER
```

#### Build/Install UCX-py

This is a requirement for RAPIDS and Blazing SQL.

```
./ucx-py.sh $UCX_PY_VER
```

#### Install apache-maven

This is a requirement for BlazingSQL.

```
./maven.sh $MAVEN_DIR
```

#### Build/Install LIBcypher-parser v0.6.2

This is a requirement for RAPIDS.

```
./libcypher-parser.sh
```

#### Build/Install FAISS

This is a requirement for RAPIDS.

```
./faiss.sh $FAISS_VER
```

#### Build/Install Arrow

This is a requirement for RAPIDS.

```
./arrow.sh $ARROW_VER
```

### Build and Install RAPIDS and BlazingSQL

#### Build/Install RMM

```
./rmm.sh $RMM_VER
```

#### Build/Install cudf

```
./cudf.sh $CUDF_VER
```

#### Build/Install cuML

```
./cuml.sh $CUML_VER
```

#### Build/Install cuGraph

```
./cugraph.sh $CUGRAPH_VER
```

#### Build/Install dask-cuda

```
./dask-cuda.sh $DASK_CUDA_VER
```

#### Build/Install BlazingSQL

```
./blazingsql.sh $BSQL_DIR
```
