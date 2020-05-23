# Groupby Aggregations with Dask and cuDF
import sys
import os
import argparse
import time
from warnings import filterwarnings
# Suppress the annoying future warnings
filterwarnings("ignore")
import numpy as np
import pandas as pd
import dask
from dask.datasets import timeseries
from dask.utils import format_bytes, format_time
import dask.dataframe as dd
import dask.array as da
from dask.distributed import Client, wait
# RAPIDS SPECIFIC:
import rmm
import cudf
import dask_cudf

ben_data_path = '/gpfs/alpine/proj-shared/stf011/benjha/datasets/dataset.csv'
dask_dir = os.path.join(os.path.join(os.getenv('MEMBERWORK'), 
                                     'stf011'), 
                        'dask')

sched_json_for_pack = {'dask-cudf': os.path.join(dask_dir, 'my-scheduler-gpu.json'),
                       'dask': os.path.join(dask_dir, 'my-scheduler.json'),
                       'cudf': None,
                       'pandas': None}

package_name_to_handle = {'dask-cudf': dask_cudf,
                          'dask': dd,
                          'cudf': cudf,
                          'pandas': pd}

# -------------------------------------------- DATA GENERATION FUNC -----------------------------------------

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

# ----------------------------------- PARTITIONING FUNCTIONS -----------------------------------------
    
def get_default_num_partitions(file_size_mb, package_name):
    # In order to improve read_csv times, the chunk / block size could be varied
    # However, the resultant number of partitions is always suboptimal
    # Optimal - set partition size equal to default
    if package_name =='cudf' or package_name == 'pandas':
        return None
    part_size = 256
    if package_name == 'dask':
        part_size = 64
    return int(np.ceil(file_size_mb / part_size))

def get_partitions_by_scaling_workers(client, scale_partitions_by_workers):
    num_dask_workers = len(client.scheduler_info()['workers'])
    return int(num_dask_workers * scale_by_workers)

# --------------------------------- CSV READING FUNCTIONS -----------------------------------------
        
def set_chunksize(read_chunk_mb, file_size_mb):
        
    if read_chunk_mb is None:
        return None
    elif not isinstance(read_chunk_mb, int):
        raise TypeError('Invalid chunksize argument: {} provided. Provide a whole number, leave as None or set to -1 for best size'.format(read_chunk_mb))
    else:
        if read_chunk_mb <= 0:
            # dask - very easy - 1 GB
            # dask-cudf - except for 25 GB all else show best performance at 1 GB
            chunksize_mb = 1024 # min(int(file_size_mb), 1024)
        else:
            chunksize_mb = read_chunk_mb
            
        return chunksize_mb
    
def read_csv(csv_path, package_handle, package_name, chunksize_mb=1024, **kwargs):
    #kwargs = dict()
    if isinstance(chunksize_mb, int) and chunksize_mb > 32:
        if package_name == 'dask-cudf':
            kwargs['chunksize'] = str(chunksize_mb) + 'MiB'
        elif package_name == 'dask':
            kwargs['blocksize'] = str(chunksize_mb) + 'MB'
    print('read_csv will be given: {}'.format(kwargs))

    t0 = time.time()
    dframe = package_handle.read_csv('file://' + csv_path, **kwargs)
    persist = kwargs.pop('persist', True)
    if package_name in ['dask', 'dask-cudf']:
        if persist:
            dframe = dframe.persist()
        else:
            print('Dataframe requested to not persist in memory')
    print('Time to load a {} file with {}: {}'.format(format_bytes(os.stat(csv_path).st_size), package_name, format_time(time.time() - t0)))

    print('Dataframe object of type: {}'.format(type(dframe)))
    
    return dframe

# ----------------------------- MAIN BENCHMARKING FUNCTION -----------------------------------------

def single_benchmark(package_name, targ_size, client,
                     stop_at_read=False,
                     read_chunk_mb=None, 
                     scale_partitions_by_workers=None, num_partitions=None, default_partitions=True):
    """
    single GPU benchmarked up to 1E+8 rows but unknown number of columns
    """   
    print('\n'*2 + '~'*10 + ' BENCHMARKING START ' + '~'*10)
    print('Target dataframe size: {}. package_name: {}\n'.format(targ_size, package_name))
    print('Optional arguments: stop_at_read={}, read_chunk_mb={}, scale_partitions_by_workers={}, num_partitions={}, '
          'default_partitions={}, client={}'
          ''.format(stop_at_read, read_chunk_mb, scale_partitions_by_workers, num_partitions, default_partitions, client))
    
    package_handle = package_name_to_handle[package_name]
            
    # --------------- GET RANDOM DATA FILE PATH---------------------
    kwargs = dict()
    if targ_size == 'ben':
        col_name = 'x'
        csv_path = ben_data_path
        kwargs.update({'delimiter': ' ', 'persist': True})
    else:
        col_name = 'id'
        csv_path = get_timeseries_path(get_frequency(targ_size), num_ids=1000)

    # ----------------- READ FROM FILE -----------------------------
    t_start = time.time()
    
    file_size_mb = os.stat(csv_path).st_size / (1024 **2)
    
    chunksize_mb = None
    if 'dask' in package_name:
        chunksize = set_chunksize(read_chunk_mb, file_size_mb)
            
    dframe = read_csv(csv_path, package_handle, package_name, chunksize_mb=chunksize_mb, **kwargs)
    
    if stop_at_read:
        print('~'*10 + ' BENCHMARKING END ' + '~'*10 + '\n'*2)
        return
    
    # ---------- RE-PARTITION DATAFRAME -------------------------------
    # This does NOT appear to be optimized in any sensible way for either dask or dask-cudf 
    if 'dask' in package_name:
        print('Dataframe currently has {} partitions'.format(dframe.npartitions))
        
        if default_partitions and chunksize_mb is not None:
            num_partitions = get_default_num_partitions(file_size_mb, package_name)
            print('Recommended default partitions = ' + str(num_partitions))
        
        elif scale_partitions_by_workers is not None:
            num_partitions = get_partitions_by_scaling_workers(client, scale_partitions_by_workers)
            print('Scaling partitions by number of workers gives ' + str(num_partitions))
        
        if isinstance(num_partitions, int) and num_partitions > 0 and num_partitions != dframe.npartitions:
            print('Setting number of partitions to: {}'.format(num_partitions))
            dframe = dframe.repartition(npartitions=num_partitions)
            
    # ----------------- SEE HEAD -----------------------------

    # print(dframe.head().to_pandas())

    # -------------- QUERY SIZE OF DATAFRAME ------------------------

    t0 = time.time()
    print('Dataframe has {} rows and {} columns'.format(len(dframe), len(dframe.columns)))
    print('Time to calculate number of rows using {}: {}'.format(package_name, format_time(time.time() - t0)))

    # -------------- COMPUTE UNIQUE IDs ------------------------

    t0 = time.time()
    uniq_ids = dframe[col_name].nunique()
    if 'dask' in package_name:
        uniq_ids = uniq_ids.compute()
    print('Time to compute unique values: {} using {}: {}'.format(uniq_ids, package_name, format_time(time.time() - t0)))

    # -------------- COMPUTE GROUPBY ------------------------

    t0 = time.time()
    if 'dask' in package_name:
        vals = dask.compute(
            dframe.groupby(col_name).min(),
            dframe.groupby(col_name).max(),
            dframe.groupby(col_name).mean(),
            dframe.groupby(col_name).count(),
        )
    else:
        vals = (
            dframe.groupby(col_name).min(),
            dframe.groupby(col_name).max(),
            dframe.groupby(col_name).mean(),
            dframe.groupby(col_name).count(),
        )

    print('Time to compute Groupby using {}: {}'.format(package_name, format_time(time.time() - t0)))
    
    if targ_size == 'ben': 
        # Can't do merge operation
        return
    
    # --------------- GET RANDOM DATA FILE PATH FOR RIGHT -----------------
    smaller_freq = get_right_freq_from_left(targ_size)
    csv_right = get_timeseries_path(smaller_freq, num_ids=1001)

    # ----------------- READ FROM SMALLER FILE -----------------------------
    
    dframe_right = read_csv(csv_right, package_handle, package_name, chunksize_mb=None)
    if 'dask' in package_name:
        print('Dataframe (right) has {} partitions'.format(dframe_right.npartitions))
    
    # cudf doesn't handle datetime indexes well yet, so we convert to integer dtype
    dframe.index = dframe.index.astype(int)
    dframe_right.index = dframe_right.index.astype(int)
    
    # ----------------- PERFORM THE MERGE -----------------------------
    t0 = time.time()
    dframe_out = dframe.merge(dframe_right, left_index=True, right_index=True, how='inner')
    if 'dask' in package_name:
        dframe_out = dframe_out.persist()
        _ = wait(dframe_out)
    print('Time to perform merge using {}: {}'.format(package_name, format_time(time.time() - t0)))
    
    # -------------- END ------------------------
    print('~'*10 + ' BENCHMARKING END ' + '~'*10 + '\n'*2)
    

# ----------------------------------- CLUSTER SET UP FUNCTIONS -----------------------------------------        
        
def set_up_dask_client(scheduler_json_path, num_exp_workers=None, max_wait_secs=120, wait_secs=10):

    if scheduler_json_path is None:
        return None
    
    client = Client(scheduler_file=scheduler_json_path)
    
    # print(dir(client))
    # print(client.scheduler_info())
    
    if num_exp_workers is None:
        num_exp_workers = 1
        
    # use built-in function instead
    print('Scheduler currently has {} workers. Waiting for {} workers to arrive'.format(len(client.scheduler_info()['workers']), num_exp_workers))
    # client.wait_for_workers(n_workers=num_exp_workers)
    wait_for_workers(client, num_exp_workers, max_wait_secs=120, wait_secs=10)
    
    print("client information {}".format(client))
    """    
    client.run(
               rmm.reinitialize,
               pool_allocator=True,
               managed_memory=False,
               initial_pool_size=2**31,
               )"""
    return client
    
    
def wait_for_workers(client, num_exp_workers, max_wait_secs=120, wait_secs=10):
    # This function is no longer necessary given dask.distributed.client's built in function
    if len(client.scheduler_info()['workers']) < num_exp_workers:
        print('Dask workers have not yet arrived. Waiting for at most {} sec'.format(max_wait_secs))

    t0 = time.time()
    while len(client.scheduler_info()['workers']) < num_exp_workers and time.time()-t0 < max_wait_secs:
        time.sleep(wait_secs)

    if len(client.scheduler_info()['workers']) < num_exp_workers:
        raise ValueError('Dask workers have not connected with the scheduler')
        
    print('All workers arrived')
    
    
def manually_add_workers_jsrun(client, num_workers, cuda=True, scheduler_file_path=None):    
    if not isinstance(num_workers, int):
        raise TypeError('add_workers: num_workers should be a positive integer. Provided: {}'.format(num_workers))
    if num_workers < 1:
        raise ValueError('add_workers: num_workers should be > 0. Provided: ' + str(num_workers))
    if cuda:
        jsrun_cmd = "jsrun -n {} -c 1 -g 1 -r {} -a 1 --smpiargs='off' dask-cuda-worker --scheduler-file {}  --nthreads 1 --memory-limit 85GB --device-memory-limit 16GB  --death-timeout 60 --interface ib0  --enable-infiniband --enable-nvlink"
    else:
        jsrun_cmd = "jsrun -n {} -c 1 -a 1 -r {} --bind rs dask-worker --scheduler-file {} --nthreads 1  --memory-limit 12GB  --nanny --death-timeout 60 --interface ib0"

    jsrun_cmd = jsrun_cmd.format(num_workers, 1, scheduler_file_path)

    os.system(jsrun_cmd)
    
def manually_add_workers_bsub(client, num_workers, cuda=True, scheduler_file_path=None):    
    if not isinstance(num_workers, int):
        raise TypeError('add_workers: num_workers should be a positive integer. Provided: {}'.format(num_workers))
    if num_workers < 1:
        raise ValueError('add_workers: num_workers should be > 0. Provided: ' + str(num_workers))
    
    directory = '/gpfs/alpine/world-shared/stf011/somnaths/rapids/nvrapids_olcf/dask-cuda-batch'
    
    if cuda:
        job_script = os.path.join(directory, 'launch_dask_cuda_worker_1_node.lsf')
    else:
        job_script = os.path.join(directory, 'launch_dask_worker_1_node.lsf')

    jsrun_cmd = jsrun_cmd.format(num_workers, num_resource_sets, scheduler_file_path)

    os.system(jsrun_cmd)  
    
# ----------------------------- SCALING FUNCTION -----------------------------------------

def main(package_name, file_sizes, scheduler_file_path, worker_sizes, **kwargs):
    
    if 'dask' not in package_name:
        worker_sizes = [1]
        client = None
    else:
        if worker_sizes is None:
            worker_sizes = [1]
        # remove duplicates
        worker_sizes = list(set(worker_sizes))
        # sort ascending
        worker_sizes.sort()
        
        print('Calling Client setup with: scheduler json: {}, expected workers: {}'.format(scheduler_file_path, worker_sizes[0]))
        client = set_up_dask_client(scheduler_file_path, num_exp_workers=worker_sizes[0])
        
    print('Will benchmark package: {} on file sizes: {} over dask workers: {}'.format(package_name, file_sizes, worker_sizes))
        
    for num_workers in worker_sizes:
        if 'dask' in package_name:
            # Not sure how well this function will work
            #client.cluster.scale(num_workers)
            extra_workers = num_workers - len(client.scheduler_info()['workers'])
            if extra_workers > 0:
                manually_add_workers(client, num_workers, cuda=package_name == 'dask_cudf', scheduler_file_path=scheduler_file_path)
            
            #client.wait_for_workers(n_workers=num_workers)
            wait_for_workers(client, num_exp_workers, max_wait_secs=120, wait_secs=10)
        
        for dsize in file_sizes:
            single_benchmark(package_name, dsize, client, **kwargs)

            
# ----------------------------------- GENERAL HELPER FUNCTIONS -----------------------------------------

def validate_file_sizes(file_sizes):
    
    if file_sizes is None:
        return ['1G', '2.5G', '5G' , '10G', '25G']
    for item in file_sizes:
        if item not in ['1G', '2.5G', '5G' , '10G', '25G', 'ben']:
            raise ValueError('Provided file size: {} is not a valid option.')
    return file_sizes
        
def validate_package_name(package_name):
    
    if not isinstance(package_name, str):
        raise TypeError('package_name should be of type str. Provided object ({}) of type ({})'.format(package_name, type(package_name)))
    if package_name not in ['dask-cudf', 'dask', 'cudf', 'pandas']:
        raise ValueError('Requested package: "' +  package_name + '" is not valid')    
    
if __name__ == '__main__':    
    args = argparse.ArgumentParser()
    args.add_argument('--package', default='pandas', type=str,
                      help='dataframe package. One of: dask, dask-cudf, cudf or pandas')
    args.add_argument('--file_size', default=None, type=str, nargs='+', 
                      help='Primary file size in GB. Use one (or list) of 1G, 2.5G, 5G, 10G, or 25G or leave unspecified to loop over all sizes')
    args.add_argument('--stop_at_read', default=False, type=bool,
                      help='Whether to stop benchmark after reading the primary CSV file. Use for testing I/O only')
    args.add_argument('--read_chunk_mb', default=None, type=int,
                      help='chunksize or blocksize in MB to be passed onto read_csv(). Set to < 0 for best block size. Note - this directly affects number of partitions. Applies to dask and dask-cudf only.')
    args.add_argument('--scale_partitions_by_workers', default=None, type=int,
                      help='Partitions the dataframe into scale_partitions_by_workers * number of dask workers. Applies to dask and dask-cudf only.')
    args.add_argument('--default_partitions', default=True, type=bool,
                      help='Sets number of partitions to default values according to package. Applies to dask and dask-cudf only.')
    args.add_argument('--num_partitions', default=None, type=int,
                      help='Partitions the dataframe into the specified number of partitions. Applies to dask and dask-cudf only.')
    
    args.add_argument('--num_dask_workers', default=None, type=int, nargs='+', 
                      help='Number of expected dask workers linked with the scheduler. Specify a list of (increasing) integers to instruct how the workers need to be varied. Example: "--num_dask_workers 4" will only use 4; "--num_dask_workers 1 2 4" scales over 1, 2, and 4. Applies to dask and dask-cudf only.')
    args.add_argument('--scheduler_json_path', default=None, type=str,
                      help='Absolute path to Dask scheduler JSON file. Applies to dask and dask-cudf only.')

    args = args.parse_args()
    
    validate_package_name(args.package)
    
    file_sizes = validate_file_sizes(args.file_size)
    
    if args.scheduler_json_path is None:
        scheduler_json_path = sched_json_for_pack[args.package]
    else:
        scheduler_json_path = args.scheduler_json_path
    if not os.path.exists(scheduler_json_path):
        raise FileNotFoundError('Dask scheduler JSON file does not exist: {}'.format(scheduler_file_path))
        
    if args.num_dask_workers is not None:
        if isinstance(args.num_dask_workers, int):
            args.num_dask_workers = [args.num_dask_workers]
        if isinstance(args.num_dask_workers, list):
            if not all([isinstance(x, int) and x > 0 for x in args.num_dask_workers]):
                raise TypeError('--num_dask_workers must be a list of positive integers')
        
    kwargs = {'stop_at_read': args.stop_at_read,
              'read_chunk_mb': args.read_chunk_mb, 
              'scale_partitions_by_workers': args.scale_partitions_by_workers, 
              'num_partitions': args.num_partitions, 
              'default_partitions': args.default_partitions}
    
    print('Validated all inputs. Calling main with: package_name: {}, file_sizes: {}, scheduler: {}, dask_workers: {}, kwargs: {}'.format(args.package, file_sizes, scheduler_json_path, args.num_dask_workers, kwargs))
    
    main(args.package, file_sizes, scheduler_json_path, args.num_dask_workers, **kwargs)
