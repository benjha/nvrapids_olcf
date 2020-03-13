# Example code for large-scale dask workers on Summit
This provides an example batch submission script for 5,526 dask workers on 
Summit.

* `921_node_dask.lsr` -- sample Summit LSF batch submission script
* `wait_for_workers.py` -- simple utility script by batch scripts to wait until all the dask workers have been registered before running the dask client

Note, that as of 3/13/2020 the tests for these scripts are still waiting to
run on Summit.  I'll update this as soon as those run successfully.

I'll later expand this `README` to match the style of the sibling directories.

> Mark Coletti
> Oak Ridge National Laboratory
> `colettima@ornl.gov`
