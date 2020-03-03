##

Add CuPy / DASK scripts here

## System configuration

- IBM Power System AC922. 2x POWER9 CPU (84 smt cores each) 512 GB RAM, 6x NVIDIA Volta GPU with 16 GB HBM2
- GCC v6.4
- CUDA v10.1.168
- NVIDIA Driver v418.67
- NVIDIA Rapids v0.11
- CuPy v7.1.1
- NumPy v1.17.3
- DASK v2.9.1

## SVD Single-GPU vs POWER9 CPU

Results obtained from ```svd_dask_cupy.py``` and ```svd_dask_numpy.py``` scripts

![SVD](https://github.com/benjha/nvrapids_olcf/blob/branch-0.11/gtc_2020/plots/SVD_singleGPU_Power9.png)
