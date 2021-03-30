"""
Coordinate IOR parameter sweep
==============================

Facilitates the execution of multiple IOR runs sweeping over a specified
parameter.
"""

import argparse
import itertools
import logging  # TODO: Log to stdout and stderr respectively, rather than print
import numpy as np
import pathlib
import subprocess
import time

from pathlib import Path
from subprocess import Popen

IOR_PATH = str(Path('~/ior-3.3.0/src/ior').expanduser())
DEFAULTS = {  # These are the same as running IOR without and options
    'b': '1m',
    't': '256k',
    's': 1,
    'tasks': 1
}

def sweep(param, start, end, steps, logbase=None, unit='', ior_path=IOR_PATH, options=DEFAULTS):
    """
    Parameters
    ----------
    param : string
        The parameter to sweep over. Can be 'blocksize', 'transfersize',
        'segments', 'tasks', or any valid IOR option.
    start : scalar
        The starting value for the parameter.
    end : scalar
        The ending value for the parameter.
    steps : int
        How many steps there should be between start and end, inclusive.
    logbase : scalar, optional
        If specified, will make a range from logbase**start to logbase**end. If
        left as None, steps will be linear.
    unit : string, optional
        The unit of the parameter, e.g. 'm' for mebibytes when working with
        block size or transfer size. Segments and tasks do not need units.
    ior_path : path
        Path to the IOR executable.
    options : dictionary
        Mapping of option flags and values for everything except the parameter
        of interest.

        See: https://ior.readthedocs.io/en/latest/userDoc/options.html
    """

    # Create the range of parameters to test out.
    if logbase:
        param_range = np.logspace(start, end, num=steps, base=logbase)
    else:
        param_range = np.linspace(start, end, num=steps)

    # Add the unit, if any
    param_range = [str(v) + unit for v in param_range]

    # Time to actually execute the sweep

    opt_mapping = {
        'blocksize':'b', 'transfersize':'t', 'segments':'s'
    }

    for idx, value in enumerate(param_range):

        print('*** Starting test with {:s}={:s} ({:d} of {:d}) ***'.format(param, value, idx, steps))

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
            [v for v in opts.values()]
        ))

        # Execute the IOR test with the given parameter
        cmd = ['mpirun', '-np', mpiprocs, IOR_PATH, *itertools.chain(*opt_list)]
       # process = Popen(cmd, stdout=subproccess.PIPE, stderr=subprocess.PIPE)
       # # Then wait for it to complete
       # process.wait()
       # # Finally log the stdout and stderr
       # o = process.stdout.read().decode()
       # print(o)
       # e = process.stderr.read().decode()
       # print(e)
        print(cmd)
        time.sleep(1)

        print('*** End ***')

