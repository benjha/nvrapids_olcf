NUM_WORKERS=3
PACKAGE="dask_cudf"
SCRIPT="cudf_bench_v0.py"
PROJ_ID="stf011"
SCHEDULER_JSON="$MEMBERWORK/$PROJ_ID/dask/my-scheduler-gpu_$NUM_WORKERS.json"

# I/O - TESTING CHUNKING

python $SCRIPT --package $PACKAGE --num_dask_workers $NUM_WORKERS --scheduler_json_path $SCHEDULER_JSON --read_chunk_mb 32 64 128 256 512 1024 --stop_at_read True

python $SCRIPT --package $PACKAGE --num_dask_workers $NUM_WORKERS --scheduler_json_path $SCHEDULER_JSON --file_size 2.5G 5G 10G 25G --read_chunk_mb 2048 --stop_at_read True

python $SCRIPT --package $PACKAGE --num_dask_workers $NUM_WORKERS --scheduler_json_path $SCHEDULER_JSON --file_size 5G 10G 25G --read_chunk_mb 4096 --stop_at_read True

python $SCRIPT --package $PACKAGE --num_dask_workers $NUM_WORKERS --scheduler_json_path $SCHEDULER_JSON --file_size 10G 25G --read_chunk_mb 8192 --stop_at_read True

# Partitioning

python $SCRIPT --package $PACKAGE --num_dask_workers $NUM_WORKERS --scheduler_json_path $SCHEDULER_JSON --file_size 1G 2.5G 5G 10G 25G

python $SCRIPT --package $PACKAGE --num_dask_workers $NUM_WORKERS --scheduler_json_path $SCHEDULER_JSON --file_size 1G 2.5G 5G 10G 25G --num_partitions 3 6 12 24 48 96
