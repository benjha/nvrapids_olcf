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
from dask.distributed import Client, wait
# RAPIDS SPECIFIC:
import cudf
import dask_cudf

# -------------- DATA GENERATION FUNC --------------------------------

def generate_timeseries(num_ids=1000, freq='1d', seed=1, csv_path=None, prefixes_left=True, keep_id=True, **kwargs):
    
    alphabets = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

    if prefixes_left:
        prefixes = alphabets[:10]
    else:
        prefixes = alphabets[-10:]

    coll_dict = dict()
    for prefix in prefixes:
        for this_name in alphabets:
            coll_dict[prefix + this_name] = float

    if keep_id:
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
    
    #num_ids = 1000 # Not sure if this number should be changed
    freq = get_frequency(targ_size)
    
    csv_path = get_timeseries_path(freq, num_ids)

    if os.path.exists(csv_path):
        print('Reading existing csv file')
    else:
        print('Generating data using dask.dataset.timeseries for frequency: {}. This can take a few minutes'.format(freq))
        _ = generate_timeseries(num_ids=num_ids, freq=freq, csv_path=csv_path)
    return csv_path

def get_frequency(targ_size):
    
    size_2_freq = {'1G': '163s',
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
    
    return size_2_freq[targ_size]

def get_right_freq_from_left(left_size):
    left_2_right = {'1G': '1630s',
            '2.5G': '650s',
            '5G': '330s',
            '10G': '160s',
            '25G': '65000ms',
            '50G': '32600ms',
            '100G': '16300ms',
            '250G': '6520ms',
            '500G': '3260ms',
            '1T': '1630ms',
            '2.5T': '650ms',
            '5T': '330ms',
            '10T': '160ms'}
    return left_2_right[left_size]

def generate_right_data(left_size, num_ids=1001):
    
    # Pick a size that is 1/10th the size of left
    # ie - pick 10x the frequency
    freq = get_right_freq_from_left(left_size)
        
    csv_path = get_timeseries_path(freq, num_ids=num_ids)

    if os.path.exists(csv_path):
        print('Reading existing csv file')
    else:
        print('Generating data using dask.dataset.timeseries for frequency: {}. This can take a few minutes'.format(freq))
        _ = generate_timeseries(num_ids=num_ids, freq=freq, csv_path=csv_path, prefixes_left=False, keep_id=False)
    return csv_path

def get_timeseries_path(freq, num_ids=1000):
    
    return '/gpfs/alpine/world-shared/stf011/somnaths/rapids/data/timeseries_{}_ids_{}_freq.csv'.format(num_ids, freq)

def validate_inputs(package_name, targ_size):

    if not isinstance(targ_size, str):
        raise TypeError('targ_size should be of type str. Provided object ({}) of type ({})'.format(targ_size, type(targ_size)))
    if targ_size not in ['1G', '2.5G', '5G' , '10G', '25G', 'all']: 
        raise ValueError('Requested data size: "' +  targ_size + '" is not valid')
        
    if not isinstance(package_name, str):
        raise TypeError('package_name should be of type str. Provided object ({}) of type ({})'.format(package_name, type(package_name)))
    if package_name not in ['dask-cudf', 'dask', 'cudf', 'pandas']:
        raise ValueError('Requested package: "' +  package_name + '" is not valid')
        
def get_package_scheduler(package_name):
        
    package_dict = {'dask-cudf': (dask_cudf, 'my-scheduler-gpu.json'),
                           'dask': (dd, 'my-scheduler.json'),
                           'cudf': (cudf, None),
                           'pandas': (pd, None),
                          }
    
    return package_dict[package_name]

def set_up_dask_client(scheduler_json_name):
    client = None
    if scheduler_json_name is not None:
        scheduler_file = os.getenv('MEMBERWORK') + '/stf011/' + scheduler_json_name 
        client = Client(scheduler_file=scheduler_file)
        print("client information {}".format(client))
    return client
        
def read_csv(csv_path, package_handle, package_name):
    t0 = time.time()
    dframe = package_handle.read_csv('file://' + csv_path)
    if package_name in ['dask', 'dask-cudf']:
        dframe = dframe.persist()
    print('Time to load a {} file with {}: {}'.format(format_bytes(os.stat(csv_path).st_size), package_name, format_time(time.time() - t0)))

    print('Dataframe object of type: {}'.format(type(dframe)))
    
    return dframe

# -------------- JOIN INDEXED --------------------------------

def benchmark_join_indexed(package_name, targ_size):
    
    package_handle, scheduler_json_name = get_package_scheduler(package_name)
    
    print('\n'*2 + '~'*10 + ' RAPIDS BENCHMARKING - JOIN INDEXED START ' + '~'*10)
    print('Target dataframe size: {}. package_name: {}\n'.format(targ_size, package_name))
    
    # -------------- SET UP CLUSTER --------------------------------
    client = set_up_dask_client(scheduler_json_name)
    
    # --------------- GET RANDOM DATA FILE PATH---------------------
    csv_left = get_timeseries_path(get_frequency(targ_size), num_ids=1000)
    csv_right = get_timeseries_path(get_right_freq_from_left(targ_size), num_ids=1001)

    # ----------------- READ FROM FILE -----------------------------
    t_start = time.time()
    
    dframe_left = read_csv(csv_left, package_handle, package_name)
    dframe_right = read_csv(csv_right, package_handle, package_name)
    
    # cudf doesn't handle datetime indexes well yet, so we convert to integer dtype
    dframe_left.index = dframe_left.index.astype(int)
    dframe_right.index = dframe_right.index.astype(int)
    
    # ----------------- PERFORM THE MERGE -----------------------------
    t0 = time.time()
    dframe_out = dframe_left.merge(dframe_right, left_index=True, right_index=True, how='inner')
    if scheduler_json_name is not None:
        dframe_out = dframe_out.persist()
        _ = wait(dframe_out)
    print('Time to perform merge using {}: {}'.format(package_name, format_time(time.time() - t0)))
    
    # -------------- REPORT ------------------------
    if scheduler_json_name is not None:
        _ = client.profile(start=t_start, filename=package_name + '-join-indexed-profile_'+ targ_size + '.html')
    
    print('\n'*2 + '~'*10 + ' RAPIDS BENCHMARKING - JOIN INDEXED END ' + '~'*10)
    
# -------------- GROUPBY --------------------------------

def benchmark_groupby(package_name, targ_size):
    """
    single GPU benchmarked up to 1E+8 rows but unknown number of columns
    """    
    package_handle, scheduler_json_name = get_package_scheduler(package_name)
    
    print('\n'*2 + '~'*10 + ' RAPIDS BENCHMARKING - GROUPBY START ' + '~'*10)
    print('Target dataframe size: {}. package_name: {}\n'.format(targ_size, package_name))
        
    # -------------- SET UP CLUSTER --------------------------------
    client = set_up_dask_client(scheduler_json_name)
    
    # --------------- GET RANDOM DATA FILE PATH---------------------
    csv_path = get_timeseries_path(get_frequency(targ_size), num_ids=1000)

    # ----------------- READ FROM FILE -----------------------------
    t_start = time.time()
    
    dframe = read_csv(csv_path, package_handle, package_name)

    if 'dask' in package_name:
        print('Dataframe has {} partitions'.format(dframe.npartitions))
        # Repartition to maximize performance
        num_dask_workers = len(client.scheduler_info()['workers'])
        num_partitions = num_dask_workers
        dframe = dframe.repartition(npartitions=num_partitions)
        print('Setting number of partitions to: {}'.format(dframe.npartitions))
    
    # ----------------- SEE HEAD -----------------------------

    # print(dframe.head().to_pandas())

    # -------------- QUERY SIZE OF DATAFRAME ------------------------

    t0 = time.time()
    print('Dataframe has {} rows and {} columns'.format(len(dframe), len(dframe.columns)))
    print('Time to calculate number of rows using {}: {}'.format(package_name, format_time(time.time() - t0)))

    # -------------- COMPUTE UNIQUE IDs ------------------------

    t0 = time.time()
    uniq_ids = dframe.id.nunique()
    if scheduler_json_name is not None:
        uniq_ids = uniq_ids.compute()
    print('Time to compute unique values: {} using {}: {}'.format(uniq_ids, package_name, format_time(time.time() - t0)))

    # -------------- COMPUTE GROUPBY ------------------------

    t0 = time.time()
    if scheduler_json_name is not None:
        vals = dask.compute(
            dframe.groupby('id').min(),
            dframe.groupby('id').max(),
            dframe.groupby('id').mean(),
            dframe.groupby('id').count(),
        )
    else:
        vals = (
            dframe.groupby('id').min(),
            dframe.groupby('id').max(),
            dframe.groupby('id').mean(),
            dframe.groupby('id').count(),
        )

    print('Time to compute Groupby using {}: {}'.format(package_name, format_time(time.time() - t0)))

    # -------------- REPORT ------------------------
    if scheduler_json_name is not None:
        _ = client.profile(start=t_start, filename=package_name + '-groupby-aggregations-profile_'+ targ_size + '.html')
    
    print('~'*10 + ' RAPIDS BENCHMARKING - GROUPBY END ' + '~'*10 + '\n'*2)
    
    # -------------- END ------------------------
    
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('script was called as\n\t' + ' '.join(sys.argv))
        print('please run as "python <script_name>.py <task> <package> <size>"\n\t<task> = groupby or join-indexed\n\t<package> = dask, dask-cudf, cudf or pandas\n\t<size> = 1G, 2.5G, 5G, ...25G')
    else:
        if sys.argv[1] not in ['groupby', 'join-indexed']:
            raise ValueError('First argument should either be "groupby" or "join-indexed"')
        if sys.argv[1] == 'groupby':
            benchmark_func = benchmark_groupby
        elif sys.argv[1] == 'join-indexed':
            benchmark_func = benchmark_join_indexed
        
        validate_inputs(sys.argv[2], sys.argv[3])
        
        if sys.argv[3] == 'all':
            for dsize in ['1G', '2.5G', '5G' , '10G', '25G']:
                benchmark_func(sys.argv[2], dsize)
        else:
            benchmark_func(sys.argv[2], sys.argv[3])
