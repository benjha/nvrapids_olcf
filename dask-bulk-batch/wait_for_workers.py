#!/usr/bin/env python3
"""
This utility will block on the scheduler until a certain number of workers
have registered.  This is useful for summit batch jobs to block in LSF scripts
until all the workers are spun up for work.
"""
import time
import argparse
import time
import sys

from distributed import Client

# How many seconds to sleep between polling scheduler for number of workers
DEFAULT_SLEEP = 5

# How many seconds should we wait on the dask scheduler?
DEFAULT_TIMEOUT = 30


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
    parser.add_argument('--scheduler-timeout', type=int,
                        default=DEFAULT_TIMEOUT,
                        help='How long to wait on the scheduler')
    parser.add_argument('--maximum-wait-time', type=int,
                        help='Optional parameter for maximum amount of time '
                             'to wait in minutes before proceeding')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose output')
    parser.add_argument('scheduler_file',
                        help='Scheduler file for the running scheduler')

    args = parser.parse_args()

    # Track start time if we have a secondary termination criteria of a dead-
    # line.
    if args.maximum_wait_time is not None and args.verbose:
        print(f'Deadline set for {args.maximum_wait_time} minutes')

    if args.verbose:
        print(f'Target workers: {args.target_workers}')
        print(f'Scheduler timeout: {args.scheduler_timeout} secs')
        print(f'Pause time: {args.pause_time} secs')
        print(f'Scheduler file: {args.scheduler_file}')

    try:
        with Client(scheduler_file=args.scheduler_file,
                    timeout=args.scheduler_timeout) as client:

            if args.target_workers is None:
                print(f'{get_num_workers(client)} workers')
                # Now exit since this means we just wanted the current total
                # number of workers, and didn't want to wait for a target
                # set number of workers, after all.
            else:
                start_time = time.time()

                if args.verbose:
                    print('seconds\tnumber of workers')

                prev_curr_num_workers = 0
                curr_num_workers = get_num_workers(client)

                while curr_num_workers < args.target_workers:

                    if args.maximum_wait_time is not None and \
                            args.maximum_wait_time < (time.time() - start_time) / 60:
                        print(f'Maximum time of {args.maximum_wait_time} minute met.  Exiting.')
                        break

                    if args.verbose and prev_curr_num_workers != curr_num_workers:
                        # Just echo the time in seconds since we started and
                        # the current number of workers so we get a sense of how
                        # quickly workers are being added over time
                        print(
                            f'{time.time() - start_time:.2f}\t{curr_num_workers}')

                    time.sleep(args.pause_time)

                    prev_curr_num_workers = curr_num_workers
                    curr_num_workers = get_num_workers(client)

                if args.verbose:
                    print(f'{time.time() - start_time:.2f} seconds to register '
                          f'{curr_num_workers} workers')
    except Exception as e:
        print(f'Raised {e!r} during execution')
        sys.exit(1)
