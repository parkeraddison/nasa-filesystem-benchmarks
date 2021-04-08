"""
IOR parameter sweep
===================

Facilitates the execution of multiple IOR runs sweeping over a specified
parameter.
"""

import argparse
import itertools
import logging
import numpy as np
import pathlib
import subprocess
import time

from pathlib import Path
from subprocess import Popen

IOR_PATH = str(Path('~/ior-3.3.0/src/ior').expanduser())
DEFAULTS = {  # These are the same as running IOR without any options
    'b': '1m',
    't': '256k',
    's': 1,
    'tasks': 1
}

def sweep(param, start=None, end=None, steps=None, logbase=None, unit='', values=None, ior_path=IOR_PATH, options=DEFAULTS):
    """
    Parameters
    ----------
    param : string
        The parameter to sweep over. Can be 'blocksize', 'transfersize',
        'segments', 'tasks', or any valid IOR option.
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

    # Time to actually execute the sweep

    opt_mapping = {
        'blocksize':'b', 'transfersize':'t', 'segments':'s'
    }

    for idx, value in enumerate(param_range):

        print('*** Starting test with {:s}={:s} ({:d} of {:d}) ***'.format(param, value, idx, len(param_range)))

        # Ensure that our desired parameter is set, then format the options for
        # execution.
        opt = opt_mapping.get(param) or param  # Fall back to any valid option
        opts = {**options}
        opts[opt] = value
        # Always pop out the number of MPI processes to feed in directly to
        # mpirun
        mpiprocs = opts.pop('tasks')
        # The rest of the options are formatted to be passed as arguments to IOR
        opt_list = list(zip(
            ['-{}'.format(k) for k in opts.keys()],
            [str(v) for v in opts.values()]
        ))

        # Execute the IOR test with the given parameter
        cmd = [
            'mpirun', '-np', str(mpiprocs),
            IOR_PATH, *itertools.chain(*opt_list),
            # TODO: Better support for passing in flags in options, rather than
            # hard-coded here.
            '-C', '-e', # Reorder and fsync
            '-O', 'SummaryFormat=JSON' # Output as a JSON
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
        '-p', '--param',
        help='Parameter to sweep over.'
    )

    args = parser.parse_args()

    # TODO: Replace with argparse or config file so this doesn't need to be hard
    # coded.
    sweep('tasks', values=[4,8,16,32,64],
          options={
              **DEFAULTS,
              't': '1m', 'b': '16m', 's': 16, # Writes/reads 0.25GiB per task
              'a': 'MPIIO',
          }
     )

