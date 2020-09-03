
import os
import sys
import time
import numpy as np
import cupy
from cupy.cuda.memory import malloc_managed

import dask
import dask.array as da
from dask.distributed import Client, wait
from dask.diagnostics import ProgressBar

def genMatrix (n, m, chunk):
    rs = da.random.RandomState(RandomState=cupy.random.RandomState)
    x = rs.random ((10000*n, 1000*m), chunks=(chunk, chunk))
    return x


def SVD (x, execMode):
    tAccum = 0
    t0 = time.time()
    u, s, v = da.linalg.svd (x)
    if execMode == 'compute':
    #with performance_report(filename="dask-report.html"):    
        u, s, v = dask.compute(u,s,v)
    elif execMode == 'persist':
        u, s, v = dask.persist(u,s,v)
        wait ([u, s, v])
    t1 = time.time()
    dt = t1 - t0
    return dt


if __name__ == '__main__': 

    if len(sys.argv) < 3:
        print('Usage:\n')
        print('\tpython svd_dask_cupy.py <chunksize> <persist | compute>\n')
        sys.exit(0)

    chunk = int(sys.argv[1])
    execMode = sys.argv[2]
    if execMode != 'persist' and execMode != 'compute':
        print('Execution mode should be persist or compute...\n')
        print('setting to compute\n')
        execMode = 'compute'

    #cupy.cuda.set_allocator (cupy.cuda.MemoryPool(malloc_managed).malloc)
    #cupy.cuda.set_allocator(malloc_managed)

    
    file = os.getenv('MEMBERWORK') + '/stf011/dask/my-scheduler.json'
    client = Client(scheduler_file=file)
    print("client information ",client)

    
    #client.submit(cupy.cuda.set_allocator,malloc_managed).result()
    #client.run (cupy.cuda.set_allocator, malloc_managed)

    print ('SVD Dask Cupy, chunk size = (%d, %d)\n' % (chunk, chunk), flush=True)
    print ('Matrix Size\t\tMB\t\tTime(s)\n', flush=True)

    j = 1
    #warm up
    x = genMatrix (j,1,chunk)
    dt=SVD(x, execMode)
    for i in range (12):
        x = genMatrix (j,1,chunk)
        mb = x.nbytes/(1024*1024)
        try:
            dt=SVD(x, execMode)
            print(x.shape, '\t\t', mb, '\t\t', dt, flush=True)
        except:
            client.restart ()
            sys.exit("svd_dask_cupy.py exiting...") 
        j*=2;

    client.restart ()
