import os
from dask.distributed import Client

if __name__ == '__main__': 
    file = os.getenv('MEMBERWORK') + '/stf011/my-scheduler-gpu.json'
    client = Client(scheduler_file=file)
    print("client information ",client)
    print("Done!") 
#Next line will shutdown the DASK Cluster and eventually the LSF jobs
#   client.shutdown ()
