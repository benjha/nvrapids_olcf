
import os
import sys
import time
import numpy as np
import cupy
from cupy.cuda.memory import malloc_managed

import dask
import dask.array as da
from dask.distributed import Client
from dask.diagnostics import ProgressBar

def genMatrix (n, m, chunk):
    rs = da.random.RandomState(RandomState=cupy.random.RandomState)
    x = rs.random ((10000*n, 1000*m), chunks=(chunk, chunk))
    return x


def SVD (x):
    tAccum = 0
    t0 = time.time()
    u, s, v = da.linalg.svd (x)
    u, s, v = dask.compute(u,s,v)
    t1 = time.time()
    dt = t1 - t0
    return dt


if __name__ == '__main__': 

    if len(sys.argv) < 2:
        print('Usage:\n')
        print('\tpython svd_dask_cupy.py <chunksize>\n')
        sys.exit(0)

    chunk = int(sys.argv[1])

    cupy.cuda.set_allocator (cupy.cuda.MemoryPool(malloc_managed).malloc)
    #cupy.cuda.set_allocator(malloc_managed)

    
    file = os.getenv('MEMBERWORK') + '/stf011/dask/my-scheduler-gpu.json'
    client = Client(scheduler_file=file)
    print("client information ",client)
    
    #client.submit(cupy.cuda.set_allocator,malloc_managed).result()

    print ('SVD Dask Cupy, chunk size = (%d, %d)\n' % (chunk, chunk))
    print ('Matrix Size\t\tMB\t\tTime(s)\n')

    j = 1
    for i in range (12):
        x = genMatrix (j,1,chunk)
        mb = x.nbytes/(1024*1024)
        dt=SVD(x)
        print(x.shape, '\t\t', mb, '\t\t', dt);
        j*=2;

    client.shutdown ()
