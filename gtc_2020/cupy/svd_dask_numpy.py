
import os
import sys
import time
import numpy as np

import dask
import dask.array as da
from dask.distributed import Client

def genMatrix (n, m, chunk):
    rs = da.random.RandomState(RandomState=np.random.RandomState)
    x = rs.random ((10000*n, 1000*m), chunks=(chunk,chunk))
    return x


def SVD (x):
    t0 = time.time()
    u, s, v = da.linalg.svd (x)
    u, s, v = dask.compute(u,s,v)
    t1 = time.time()
    dt = t1 - t0
    return dt

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Usage:\n')
        print('\tpython svd_dask_numpy.py <chunksize>\n')
        sys.exit(0)

    chunk = int(sys.argv[1])

    file = os.getenv('MEMBERWORK') + '/stf011/dask/my-scheduler.json'
    client = Client(scheduler_file=file)
    print("client information ",client)

    print ('SVD Dask NumPy, chunk size = (%d, %d)\n' % (chunk, chunk))
    print ('Matrix Size\t\tMB\t\tTime(s)\n')

    j = 1
    for i in range (12):
        x = genMatrix (j,1, chunk)
        mb = x.nbytes/(1024*1024)
        t=SVD(x)
        print(x.shape, '\t\t', mb, '\t\t', t);
        j*=2;
