##

run benchmarking script as: 

```bash
python cudf_benchmarking.py <task> <package> <size>
```

Provide inputs as:
* `task`: 
  * `groupby` based on [this](https://github.com/mrocklin/dask-gpu-benchmarks/blob/master/groupby-aggregations.ipynb) notebook
  * `join-indexed` based on [this](https://github.com/mrocklin/dask-gpu-benchmarks/blob/master/join-indexed.ipynb) notebook
* `package`:
  * `dask`
  * `dask-cudf`
  * `cudf`
  * `pandas`
* `size`:
  * `all`
  * `1G`
  * `2.5G`
  * `5G`
  * `10G`
  * `25G`
  * more to come ...

