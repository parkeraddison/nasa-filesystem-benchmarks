"""
IOR parameter sweep
===================

Facilitates the execution of multiple IOR runs sweeping over a specified
parameter.
"""

import argparse
import itertools
import json
import numpy as np
import pathlib
import subprocess
import time

from pathlib import Path
from subprocess import Popen

IOR_PATH = str(Path('~/benchmarks/ior/ior-3.3.0/src/ior').expanduser())
# These are the same as running IOR without any options except for outputting
# JSON format
#
# See: https://github.com/hpc/ior/blob/main/doc/USER_GUIDE
DEFAULTS = {  
    'b': '1m',
    't': '256k',
    's': 1,
    'N': 1,
    # Directives and flags (options without a value) can be specified here
    'directives': {
        'summaryFormat': 'JSON', # output as a JSON for ease of parsing
    },
    'flags': [
        'w', 'r', # perform both a write and read test
    ]
}

def sweep(param, start=None, end=None, steps=None, logbase=None, unit='', values=None, ior_path=IOR_PATH, options=DEFAULTS):
    """
    Parameters
    ----------
    param : string
        The parameter to sweep over, must be a valid IOR option. For example,
        'b' for blockSize, 't' for transferSize, 's' for numSegments, or 'N'
        for numTasks.
    start : int
        The starting value for the parameter.
    end : int
        The ending value for the parameter.
    steps : int, optional
        How many steps there should be between start and end, inclusive. If left
        as None, steps will have a size of 1, equal to `end - start + 1`.
    logbase : scalar, optional
        If specified, will make a range from logbase**start to logbase**end. If
        left as None, steps will be linear.
    unit : string, optional
        The unit of the parameter, e.g. 'm' for mebibytes when working with
        block size or transfer size. Segments and tasks do not need units.
    ior_path : string
        Path to the IOR executable.
    options : dictionary
        Mapping of option flags and values for everything except the parameter
        of interest.

        See: https://ior.readthedocs.io/en/latest/userDoc/options.html
    """
    
    # If we're given values, just use those (and convert to strings).
    if values:
        param_range = [str(v) for v in values]
    else:
    
        if steps is None:
            steps = end - start + 1
    
        # Create the range of parameters to test out.
        if logbase:
            param_range = np.logspace(start, end, num=steps, base=logbase)
        else:
            param_range = np.linspace(start, end, num=steps)

        # Add the unit, if any
        #
        # NOTE: IOR expects integer values, hence our casting to int
        param_range = [str(int(v)) + unit for v in param_range]

    print('Will sweep {:s} over {}'.format(param, param_range))

    ## Time to actually execute the sweep

    opts = {**DEFAULTS, **options}
    directives = opts.pop('directives')
    flags = opts.pop('flags')
    
    for idx, value in enumerate(param_range):

        print('*** Starting test with {:s}={:s} ({:d} of {:d}) ***'.format(param, value, idx, len(param_range)))
        
        opts[param] = value
        
        # Now we format our options, flags, and directives to be passed in
        # argument form (a list of args).
        opt_list = list(itertools.chain(*zip(
            ['-{}'.format(k) for k in opts.keys()],
            [str(v) for v in opts.values()]
        )))
        # Flags and directives get treated a bit differently, but follow the
        # same concept
        opt_list.extend(['-{}'.format(f) for f in flags])
        opt_list.append('-O')
        opt_list.append(','.join([
            '{}={}'.format(k,v) for k,v in directives.items()
        ]))
        
        # The number of MPI processes (# tasks) can be found in the options
        mpiprocs = opts['N']
        
        # Execute the IOR test with the given parameter
        cmd = [
            'mpiexec', '-np', str(mpiprocs),
            IOR_PATH,
            *opt_list # All other options specified
        ]
        print('Command: {:s}\n'.format(' '.join(cmd)))
        process = Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Then wait for it to complete
        process.wait()
      
        # Finally log the stdout and stderr
        o = process.stdout.read().decode()
        print(o)
        e = process.stderr.read().decode()
        print(e)
      
        # If it exited non-zero, we should exit, too
        if process.returncode != 0:
            raise Exception('Non-zero exit code {} seen above, exiting.'.format(process.returncode))

        print('*** End ***')

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument(
        'jobfile', type=str,
        help='Path to a JSON file specifying the sweep and IOR options to run.'
    )
    
    args = parser.parse_args()
    
    with open(Path(args.jobfile), 'r') as jobfile:
        job = json.load(jobfile)
        
    sweep(**job)

