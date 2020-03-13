#!/usr/bin/env python3
"""
This utility will block on the scheduler until a specified number of workers
have registered.  This is useful for summit batch jobs to block in LSF scripts
until all the workers are spun up for work.

Mark Coletti
colettima@ornl.gov
Oak Ridge National Laboratory
"""
import argparse
import time

from distributed import Client

# How many seconds to sleep between polling scheduler for number of workers
DEFAULT_SLEEP = 5


def get_num_workers(client):
    """
    :param client: active dask client
    :return: the number of workers registered to the scheduler
    """
    scheduler_info = client.scheduler_info()

    return len(scheduler_info['workers'].keys())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='dask utility for blocking '
                                                 'until set target of workers '
                                                 'is registered')
    parser.add_argument('--target-workers', '-t',
                        type=int,
                        help='The target total number of workers on which to '
                             'wait; if not specified, just dump out the '
                             'worker count.')
    parser.add_argument('--pause-time', '-p', type=int, default=DEFAULT_SLEEP,
                        help='How long to pause between polling scheduler for '
                             'number of workers')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose output')
    parser.add_argument('scheduler_file',
                        help='Scheduler file for the running scheduler')

    args = parser.parse_args()

    if args.verbose:
        print(f'Target workers: {args.target_workers}')
        print(f'Scheduler file: {args.scheduler_file}')

    with Client(scheduler_file=args.scheduler_file) as client:

        if args.target_workers is None:
            print(f'{get_num_workers(client)} workers')
        else:
            curr_num_workers = 0

            start_time = time.time()

            while curr_num_workers < args.target_workers:
                curr_num_workers = get_num_workers(client)

                time.sleep(args.pause_time)

            if args.verbose:
                print(f'{time.time() - start_time} seconds to register '
                      f'{curr_num_workers} workers')
