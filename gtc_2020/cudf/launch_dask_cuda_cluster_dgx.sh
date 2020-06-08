# Only modify the next two lines as necessary
GPUS='6,7'
DASK_DIR="/raid/syz/rapids/dask"

INTERFACE="enp1s0f0"

if [ ! -d "$DASK_DIR" ] 
then
    mkdir $DASK_DIR
fi

# clean previous contents
rm -fr $DASK_DIR/*

# Explicit scheduler json file
SCHEDULER_FILE="$DASK_DIR/my_gpu_scheduler.json"

# random scheduler port - not necessary for DGX
PORT_SCHED=$(shuf -i 4000-6000 -n 1)

echo "dask-scheduler --port $PORT_SCHED --interface $INTERFACE --scheduler-file $SCHEDULER_FILE &"

# Remove local-directory for newer versions of dask
dask-scheduler --local-directory $DASK_DIR --port $PORT_SCHED --interface $INTERFACE --scheduler-file $SCHEDULER_FILE &

sleep 10

echo "CUDA_VISIBLE_DEVICES=$GPUS dask-cuda-worker --interface $INTERFACE --scheduler-file $SCHEDULER_FILE --nthreads 1 --memory-limit 40GB --device-memory-limit 16GB --death-timeout 180 --enable-nvlink"

# Remove local-directory for newer versions of dask
CUDA_VISIBLE_DEVICES=$GPUS dask-cuda-worker --local-directory $DASK_DIR --interface $INTERFACE --scheduler-file $SCHEDULER_FILE --nthreads 1 --memory-limit 40GB --device-memory-limit 16GB --death-timeout 180 --enable-nvlink

sleep 10
