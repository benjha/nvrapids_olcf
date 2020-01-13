import sys
import os
import time
import numpy as np
import dask.distributed

def task(seed):

    print("Start task",seed,"on",dask.distributed.get_worker().address, flush=True)

    rng = np.random.RandomState(seed)

    print("Task",seed,"has affinity",os.sched_getaffinity(0), flush=True)

    # Do some busy work so we (hopefully) spread work among the workers
    time.sleep(1)
    # Use NumPy to test how it affects CPU affinity
    s = 0.0
    for _ in range(100):
        x = rng.uniform(0.0,1.0)
        s += x

    print("Task",seed,"complete, sum =",s, flush=True)

def start(client):
    print(client)
    ftrs = []
    for i in range(42):
        ftrs.append(client.submit(task,i))
        print("Submitted task",i)
    dask.distributed.wait(ftrs)
    print("All tasks complete")


if __name__ == "__main__":
    scheduler_file=None

    for i in range(len(sys.argv)):
        if sys.argv[i] == '-s':
            scheduler_file=sys.argv[i+1]

    if scheduler_file is not None:
        print('Scheduler file:', scheduler_file)
        with dask.distributed.Client(scheduler_file=scheduler_file) as client:
            start(client)
    else:
        raise Exception("Specify a scheduler file with -s")
