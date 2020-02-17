import os
import socket
from dask.distributed import Client

#
# script based on
# http://pangeo.io/setup_guides/hpc.html
#

def start_jlab(dask_scheduler):
    import subprocess
    proc = subprocess.Popen(['jupyter', 'lab', '--ip', host, '--no-browser', '--NotebookApp.token=' '','--NotebookApp.password=' ''])
    dask_scheduler.jlab_proc = proc

if __name__ == '__main__': 
    file = os.getenv('MEMBERWORK') + '/stf011/my-scheduler-gpu.json'
    client = Client(scheduler_file=file)
    
    print("\nclient information\n",client)
    host = client.run_on_scheduler(socket.gethostname)

    client.run_on_scheduler(start_jlab)
    
    print("\nInstructions: \n")
    print("1. In a new terminal, open a tunneling connection to Summit:\n") 
    print("   ssh -N -L 8888:%s:8888  -L 8787:%s:8787 -l username summit.olcf.ornl.gov\n\n" % (host, host))
    print("2. Open a web browser and use the next links to connect to Jupyter Lab and Dask's dashboard:\n")
    print("   Jupyter Lab: http://localhost:8888")
    print("   Dask's dashboard: http://localhost:8787\n\n") 
