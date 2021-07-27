import time

time_fixed = time.time()

import argparse
import multiprocessing
import multiprocessing.pool
import pandas as pd
import pickle as pkl

from pathlib import Path

fixed_cost = time.time() - time_fixed

print(f'FIXED COST: {fixed_cost}')

def process_file(fp):

    with open(fp, 'rb') as infile:
        data = pkl.load(infile)

    meta = data['meta_data']
    df = data['data']

    timestamp = df['GREENWICH MEAN TIME (HOUR)']
    touchdown = timestamp.max()

    landing_seconds = 160
    landing = timestamp > (touchdown - landing_seconds / 60 / 60)

    desired_cols = [
        'OIL TEMPERATURE 2', 'OIL TEMPERATURE 3', 'OIL TEMPERATURE 4',
        'PACK AIR CONDITIONING ALL', 'FLIGHT PHASE FROM ACMS',
        'IMPACT PRESSURE LSP', 'POWER LEVER ANGLE 1',
        'POWER LEVER ANGLE 4', 'PYLON OVERHEAT ALL ENGINES',
        'STATIC PRESSURE LSP', 'AVARAGE STATIC PRESSURE LSP',
        'TOTAL PRESSURE LSP', 'PITCH ANGLE LSP', 'PITCH TRIM POSITION',
        'STICK PUSHER', 'RADIO ALTITUDE LSP', 'ROLL ANGLE LSP',
        'RUDDER POSITION', 'RUDDER PEDAL POSITION',
    ]

    processed = df.loc[landing, desired_cols]
    
    return (processed, meta)

def main(pkl_dir=None, parallel=False):
    """
    Load in tons of pkl files
    """
    time_start = time.time()

    filepaths = pkl_dir.glob('*.pkl')

    workers = multiprocessing.cpu_count() * 2

    if parallel == 'threads':
        print('Preprocessing with threading')
        with multiprocessing.pool.ThreadPool(workers) as pool:
            r = pool.map(process_file, filepaths)

    elif parallel == 'procs':
        print('Preprocessing with multiprocessing')
        with multiprocessing.Pool(workers) as pool:
            r = pool.map(process_file, filepaths)

    else:
        print('Preprocessing with no parallelization')
        r = []
        for fp in filepaths:
            r.append(process_file(fp))

    print('Writing output')
    with open('out.pkl', 'wb') as outfile:
        pkl.dump(r, outfile)

    time_end = time.time()
    print(f'ELAPSED: {time_end - time_start}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('pkl_dir', type=Path,
                        help='Directory of pickle files to preprocess')

    parser.add_argument('--threads', action='store_true',
                        help='Use multithreading')
    parser.add_argument('--procs', action='store_true',
                        help='Use multiprocessing')

    args = parser.parse_args()

    if args.threads and args.procs:
        raise Exception('Only one of threading or multiprocessing is allowed.')
    elif args.threads:
        parallel='threads'
    elif args.procs:
        parallel='procs'
    else:
        parallel=False

    main(pkl_dir=args.pkl_dir, parallel=parallel)
