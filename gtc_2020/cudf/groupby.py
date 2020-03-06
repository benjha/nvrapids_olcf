# Groupby Aggregations with Dask and cuDF
import sys
import os
import time
import numpy as np
import pandas as pd
import dask
from dask.datasets import timeseries
from dask.utils import format_bytes, format_time
import dask.dataframe as dd
import dask.array as da
from dask.distributed import Client
# RAPIDS SPECIFIC:
import cudf
import dask_cudf

# -------------- DATA GENERATION FUNC --------------------------------

def generate_timeseries(num_ids=1000, freq='1d', seed=1, csv_path=None, **kwargs):
    coll_names = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    coll_dict = dict()
    for prefix in [''] + coll_names[:9]:
        for this_name in coll_names:
            coll_dict[prefix + this_name] = float
    coll_dict['id'] = int
    
    dask_df = timeseries(start='2000', 
                         end='2001', 
                         dtypes=coll_dict,
                         freq=freq, # Frequency. Eg - '2s' or '1H' or '12W'
                         #partition_freq=part_freq, # like '1M' or '2Y' to divide the dataframe into partitions
                         id_lam=num_ids, # number of (unique) items in "id" column
                         seed=seed,
                         **kwargs
                        ).reset_index(drop=True)
    if isinstance(csv_path, str):
        t0 = time.time()
        dask_df.to_csv(csv_path, single_file=True)
        print('Took {} to write timeseries to csv'.format(format_time(time.time() - t0)))
        
    return dask_df

def generate_data(targ_size, num_ids=1000):
    freq_mapper = {'1G': '163s',
               '2.5G': '65s',
               '5G': '33s',
               '10G': '16s',
               '25G': '6500ms',
               '50G': '3260ms',
               '100G': '1630ms',
               '250G': '652ms',
               '500G': '326ms',
               '1T': '163ms',
               '2.5T': '65ms',
               '5T': '33ms',
               '10T': '16ms'}

    #num_ids = 1000 # Not sure if this number should be changed
    freq = freq_mapper[targ_size]
    csv_path = '/gpfs/alpine/world-shared/stf011/somnaths/rapids/data/timeseries_{}_ids_{}_freq.csv'.format(num_ids, freq)

    if os.path.exists(csv_path):
        print('Reading existing csv file')
    else:
        print('Generating data using dask.dataset.timeseries for frequency: {}. This can take a few minutes'.format(freq))
        _ = generate_timeseries(num_ids=num_ids, freq=freq, csv_path=csv_path)
    return csv_path

"""
'1day' = 365
'1hour' = 8784 or 8.8E+3
----- WITH 261 COLUMNS ---------
'3min' = 1.75680E+5 = 0.9 GB  -> 163 sec for 1 GB
'1min' = 5.27040E+5 = 2.7 GB -> 65sec for 2.5 GB
'30s' = 1.054,080E+6 <----------- 5.41 GB. Use 
'15s' = ~ ?? <----------- ~ 10 GB Use 16.23
'6s' = ~ ?? <----------- ~ 25 GB
'3s' = ~ 10M <----------- ~ 50 GB
'1500ms' = ????? <----------- ~ 100 GB
???? = ????? <----------- ~ 250 GB
???? = ????? <----------- ~ 500 GB
???? = ????? <----------- ~ 1.0 TB
???? = ????? <----------- ~ 2.5 TB
???? = ????? <----------- ~ 5.0 TB
'1sec' = 3.162E+7

milliseconds = 3.162E+10

single GPU benchmarked up to 1E+8 rows but unknown number of columns
"""

def benchmark_groupby(hardware, targ_size):
    if not isinstance(targ_size, str):
        raise TypeError('targ_size should be of type str. Provided object ({}) of type ({})'.format(targ_size, type(targ_size)))
    if not isinstance(hardware, str):
        raise TypeError('hardware should be of type str. Provided object ({}) of type ({})'.format(hardware, type(hardware)))
    
    print('\n'*2 + '~'*10 + ' RAPIDS BENCHMARKING - GROUPBY START ' + '~'*10)
    print('Target dataframe size: {}. Hardware: {}\n'.format(targ_size, hardware))
    
    if hardware == 'gpu':
        package_name = 'dask-cudf'
        package_handle = dask_cudf
        scheduler_json_name = 'my-scheduler-gpu.json'
    elif hardware == 'cpu':
        package_name = 'dask'
        package_handle = dd
        scheduler_json_name = 'my-scheduler.json'
        
    # -------------- SET UP CLUSTER --------------------------------

    file = os.getenv('MEMBERWORK') + '/stf011/' + scheduler_json_name 
    client = Client(scheduler_file=file)
    print("client information {}".format(client))

    # ----------------- GENERATE RANDOM DATA ------------------------
    csv_path = generate_data(targ_size, num_ids=1000)

    # ----------------- READ FROM FILE -----------------------------
    t0 = time.time()
    t_start = t0
    dc_df = package_handle.read_csv('file://' + csv_path).persist()
    print('Time to load a {} file with {}: {}'.format(format_bytes(os.stat(csv_path).st_size), package_name, format_time(time.time() - t0)))

    print('Dataframe object of type: {}'.format(type(dc_df)))

    # ----------------- SEE HEAD -----------------------------

    # print(dc_df.head().to_pandas())

    # -------------- QUERY SIZE OF DATAFRAME ------------------------

    t0 = time.time()
    print('Dataframe has {} rows and {} columns'.format(len(dc_df), len(dc_df.columns)))
    print('Time to calculate number of rows using {}: {}'.format(package_name, format_time(time.time() - t0)))

    # -------------- COMPUTE UNIQUE IDs ------------------------

    t0 = time.time()
    uniq_ids = dc_df.id.nunique().compute()
    print('Time to compute unique values: {} using {}: {}'.format(uniq_ids, package_name, format_time(time.time() - t0)))

    # -------------- COMPUTE GROUPBY ------------------------

    t0 = time.time()
    vals = dask.compute(
        dc_df.groupby('id').min(),
        dc_df.groupby('id').max(),
        dc_df.groupby('id').mean(),
        dc_df.groupby('id').count(),
    )

    print('Time to compute Groupby using {}: {}'.format(package_name, format_time(time.time() - t0)))

    # -------------- REPORT ------------------------
    
        
    _ = client.profile(start=t_start, filename=package_name + '-groupby-aggregations-profile_'+ targ_size + '.html')
    print('~'*10 + ' RAPIDS BENCHMARKING - GROUPBY END ' + '~'*10 + '\n'*2)
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('please run as "python <script_name>.py <mode> <size>"\n\t<mode> = gpu or cpu\n\t<size> = 1G, 2.5G, 5G, ....')
    else:
        benchmark_groupby(sys.argv[1], sys.argv[2])
