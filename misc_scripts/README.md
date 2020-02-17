# Instructions

```connect_jupyther_dask.py``` is a python script that allows to interact with DASK and DASK-cuda clusters using  Jupyter Notebooks and the DASK dashboard.

After any DASK based cluster has been started as explained in the corresponding sections, follow the next instructions:

### Step 1. Activate the Conda environment

DASK and NVIDIA Rapids has been deployed in a conda enviroment available in:

```
$WORLDWORK/stf011/nvrapids_0.11_gcc_6.4.0
```

You can activate this environment by first loading the next modules:

```
module load gcc/6.4.0
module load cuda/10.1.168
module load python/3.7.0-anaconda3-5.3.0
```

and then use the `source activate` command:

```
source activate $WORLDWORK/stf011/nvrapids_0.11_gcc_6.4.0
```

to deactivate the environment type:

```
source deactivate
```

### Step 2. Execute ```connect_jupyther_dask.py``` script


Once the Conda environment has been loaded, type the next command:

```
python connect_jupyther_dask.py
```

The script should output the DASK cluster configuration, for example:

``` 
client information  <Client: 'tcp://10.41.0.42:8786' processes=6 threads=6, memory=510.00 GB>
```

and a list of instructions  to connect to Jupyter Lab and DASK's dashboard. For example:

```
Instructions: 

1. In a new terminal, type the next command:

   ssh -N -L 8888:batch2:8888  -L 8787:batch2:8787 -l username summit.olcf.ornl.gov


2. Open a web browser and use the next links to connect to Jupyter Lab and Dask's dashboard:

   Jupyter Lab: http://localhost:8888
   Dask's dashboard: http://localhost:8787
```


First, a tunneling connection should be done between your machine a Summit. Then, using the ports given in the instructions, you should open two windows in your web browser using, in this example, ```http://localhost:8888``` to connect to Jupyter Lab and ```http://localhost:8787``` to connect to Dask's dashboard.

