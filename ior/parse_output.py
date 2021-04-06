"""
IOR Output Parsing
==================

Parses the PBS output file resulting from multiple IOR runs and facilitates
comparing/plotting the performance of the runs.
"""

import itertools
import json
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
import pandas as pd
import re

from io import StringIO

BYTES_PER_MEBIBYTE = 1024**2

def extract_runs(fp, to_df=True):
    """
    Extracts IOR run JSONs from a file and parses them as Python dictionaries
    and optionally returns the summaries as DataFrames.
    """
    
    with open(fp, 'r') as infile:
        data = infile.read()
    
    # Find the outer-most pair of brackets between a "*** Starting" and
    # "*** End" tag.
    matches = re.findall(r'\*\*\* Starting(?:.*\n)*?({(?:.*\n)*?}?).*\*\*\* End', data)
    
    dicts = [json.loads(m) for m in matches]
    
    if to_df:
        # Here are all of our parameter read and write tests.
        all_summaries = pd.concat([
            pd.DataFrame.from_dict(d['summary']) for d in dicts
        ])
        return all_summaries
    else:
        return dicts

def make_plot(data, param, value):
    """
    Plots the read and write performance of some value over a shared parameter.
    Returns the fig, ax.
    
    Possible params: 'segmentCount', 'blockSize', 'transferSize', 'numTasks',
        'tasksPerNode'
    
    Possible values: 'bwMaxMIB', 'bwMinMIB', 'bwMeanMIB', 'bwStdMIB', 'OPsMax',
        'OPsMin', 'OPsMean', 'OPsSD', 'MeanTime'
    """
    readwrite_mask = data.operation == 'read'
    fig, ax = plt.subplots()

    read = data[readwrite_mask]
    write = data[~readwrite_mask]

    ax.set_xlabel(param)
    ax.set_ylabel(value)

    color = 'tab:blue'
    ax.plot(read[param], read[value], color=color, label='Read')
    ax.tick_params(axis='y', labelcolor=color)

    color = 'tab:orange'
    # We want to share the x axis but have a secondary y axis for write values
    ax2 = ax.twinx()
    ax2.plot(write[param], write[value], color=color, label='Write')
    ax2.tick_params(axis='y', labelcolor=color)

    # Place the legend underneath the figure
    fig.legend(loc='upper center', ncol=2, bbox_to_anchor=(0.5,0))

    fig.suptitle('{value} versus {param}'.format(value=value, param=param));

    return fig, ax

def rescale_x(fig, ax, factor=1/BYTES_PER_MEBIBYTE, logbase=2):
    """
    Parameters
    ----------
    factor : scalar, default 1/BYTES_PER_MEBIBYTE
        Factor to linearly scale the x axis by. If None, no linear scaling will
        be done.
    logbase : scalar, default 2
        Base to logarithmically scale the x axis by. If None, no log scaling
        will be done.
    """

    if logbase:
        ax.set_xscale('log', base=logbase)

    if factor:
        ticks = matplotlib.ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x*factor))
        ax.xaxis.set_major_formatter(ticks)
        
    return fig, ax
    

