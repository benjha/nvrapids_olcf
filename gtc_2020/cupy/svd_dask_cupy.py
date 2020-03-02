
import os
import time
import numpy as np
import cupy
from cupy.cuda.memory import malloc_managed

import dask
import dask.array as da
from dask.distributed import Client
from dask.diagnostics import ProgressBar

def genMatrix (n, m):
    rs = da.random.RandomState(RandomState=cupy.random.RandomState)
    x = rs.random ((10000*n, 1000*m), chunks=(1000,1000))
    print ("MB ", x.nbytes/(1024*1024))
    return x


def SVD (x):
    tAccum = 0
    
    #t0 = time.time()
    #d = da.from_array(x,chunks=(1024,32))
    #t1 = time.time()
    #dt = t1 - t0
    #print('np to da ',  dt,  ' sec')
    #tAccum += dt

    t0 = time.time()
    u, s, v = da.linalg.svd (x)
    u, s, v = dask.compute(u,s,v)
    t1 = time.time()
    dt = t1 - t0
    print('SVD ', dt, ' sec')

    tAccum += dt

    #t0 = time.time()
    #u = cp.asnumpy(d_u)
    #s = cp.asnumpy(d_s)
    #v = cp.asnumpy(d_v)
    #t1 = time.time()
    #dt = t1 - t0
    #print('D to H transfer ',  dt, ' sec')

    #tAccum += dt
    print ('Total ', tAccum, ' sec')


if __name__ == '__main__': 

    file = os.getenv('MEMBERWORK') + '/stf011/my-scheduler-gpu.json'
    client = Client(scheduler_file=file)
    print("client information ",client)

    #client.submit(cupy.cuda.set_allocator,malloc_managed).result()

    j = 1
    for i in range (12):
        x = genMatrix (j,1)
        SVD(x)
        j*=2;
