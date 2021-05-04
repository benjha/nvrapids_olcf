# RAPIDS deployment on Summit

RAPIDS deployment involves three steps:

- Create a conda environment from a base environment and install ppc64le RAPIDS dependencies available in the conda-forge channel.
- Build from source and/or install RAPIDS dependencies that are not available in the conda-forge channel. Build from source and/or install RAPIDS dependencies that require optimizations.
- Build from source and install CuPy, RAPIDS and BlazingSQL.

## Supervised deployment

Clone this repository in a temporal directory an go to `OLCF_Summit_ppc64le` directory.

```
git clone https://github.com/benjha/nvrapids_olcf.git tmp
cd tmp/build-scripts/OLCF_Summit_ppc64le
```

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

### Building and/or installing RAPIDS dependencies

Once the RAPIDS environment and the building environment is enabled, the next steps consist in building and/or installing RAPIDS dependencies that are not available in the conda-forge channel or require specific configurations from Summit.

Most of these dependencies are configured to be installed in `CONDA_PREFIX` directory.

#### Install LLVM and clang 8.0.1

This is a requirement for RAPIDS.

```
./clang_8.0.1.sh
```

#### Build/Install NCCL

This is a requirement for CuPy and RAPIDS.

```
./nccl.sh v2.9.6-1
```

#### Install cuTENSOR (requires nvidia developer account)

cuTENSOR 1.2.0 can't be distributable by third-parties thus you need to download it from developer.nvidia.com. This is a requirement for CuPy.

```
./cutensor.sh
```

#### Build/Install CuPy 

This is a requirement for RAPIDS.

```
./cupy.sh v8.6.0
```

#### Build/Install UCX

This is a requirement for RAPIDS and Blazing SQL.

```
./ucx.sh v1.8.1
```

#### Install JAVA SDK 11

This is a requirement for BlazingSQL.

```
./java-jdk.sh
```

#### Install apache-maven-3.6.3

This is a requirement for BlazingSQL.

```
./maven.sh
```

#### Build/Install LIBcypher-parser v0.6.2

This is a requirement for RAPIDS.

```
./libcypher-parser.sh
```

#### Build/Install FAISS

This is a requirement for RAPIDS.

```
./faiss.sh v1.7.0
```

### Build and Install RAPIDS and BlazingSQL

#### Build/Install RMM

```
./rmm.sh v0.19.0
```

#### Build/Install cudf

```
./cudf.sh v0.19.0
```

#### Build/Install cuML

```
./cuml.sh v0.19.0
```

#### Build/Install cuGraph

```
./cugraph.sh v0.19.0
```

#### Build/Install dask-cuda

```
./dask-cuda.sh v0.19.0
```

#### Build/Install BlazingSQL

```
./blazingsql.sh v0.19.0
```

