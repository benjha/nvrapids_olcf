import os
import sys
import time
import numpy as np
import cupy as cp
from cupy.cuda.memory import malloc_managed


def genMatrix (n, m):
    x = cp.random.random ((10000*n, 1000*m))
    return x


def SVD (x):
    tAccum = 0
    t0 = time.time()
    u, s, v = cp.linalg.svd (x)
    t1 = time.time()
    dt = t1 - t0
    return dt


if __name__ == '__main__': 

    cp.cuda.set_allocator(malloc_managed)

    print ('SVD Cupy \n')
    print ('Matrix Size\t\tMB\t\tTime(s)\n')

    j = 1
    for i in range (5):
        x = genMatrix (j,1)
        mb = x.nbytes/(1024*1024)
        dt=SVD(x)
        print(x.shape, '\t\t', mb, '\t\t', dt);
        j*=2;
