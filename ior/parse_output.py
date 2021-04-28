"""
IOR Output Parsing
==================

Parses the PBS output file resulting from multiple IOR runs
"""

import json
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
import pandas as pd
import re

KIBI = 1024
MEBI = 1024**2
GIBI = 1024**3

def parse_ior(fp, summary=True, print_elapsed=True):
    """
    Parses an IOR output file which may contain multiple tests.
    """
    with open(fp, 'r') as infile:
        data = json.load(infile)
     
    if print_elapsed:
        elapsed = (
            pd.to_datetime(data['Finished']) - pd.to_datetime(data['Began'])
        )
        print(elapsed)
    
    if summary:
        return pd.DataFrame.from_dict(data['summary'])
    else:
        return data

def extract_runs(fp, to_df=True):
    """
    Extracts IOR run JSONs from a stdout file and parses them as Python dicts
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

def make_plot(data, param, value, errors=None, xsep=0.02):
    """
    Plots the read and write performance of some value over a shared parameter.
    Returns the fig, ax. `errors` can be specified to a std feature to add
    error bars.
    
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
    
    #! NOTE: Shifting by multiplying by small amount...
    XMULT=xsep/2

    color = 'tab:blue'
    if errors:
        ax.errorbar(read[param]*(1+XMULT), read[value], read[errors], color=color, label='Read')        
    else:
        ax.plot(read[param]*(1+XMULT), read[value], color=color, label='Read')
    ax.tick_params(axis='y', labelcolor=color)

    color = 'tab:orange'
    # We want to share the x axis but have a secondary y axis for write values
    ax2 = ax.twinx()
    
    if errors:
        ax2.errorbar(write[param]*(1-XMULT), write[value], write[errors], color=color, label='Write')
    else:
        ax2.plot(write[param]*(1-XMULT), write[value], color=color, label='Write')
    ax2.tick_params(axis='y', labelcolor=color)

    # Place the legend underneath the figure
    fig.legend(loc='upper center', ncol=2, bbox_to_anchor=(0.5,0))

    fig.suptitle('{value} versus {param}'.format(value=value, param=param));

    return fig, (ax, ax2)

def rescale_axis(fig, axes, axis='x', factor=1, logbase=None, lim=None, sharey=False):
    """
    Parameters
    ----------
    axis : str, 'x' or 'y', default 'x'
        The axis to rescale.
    factor : scalar, default 1
        Factor to linearly scale the axis by. If None, no linear scaling will
        be done.
    logbase : scalar, default None
        Base to logarithmically scale the axis by. If None, no log scaling
        will be done.
    lim : tuple, default None
        Specific limits to set on the axis. Will be scaled by the inverse of
        `factor`.
    sharey : boolean, default False
        Whether to make the two y-axes shared. Only applies if axis='y'.
    """

    if logbase:
        if axis == 'x':
            axes[0].set_xscale('log', base=logbase)
        elif axis == 'y':
            axes[0].set_yscale('log', base=logbase)

    if factor:
        ticks = matplotlib.ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x*factor))
        if axis == 'x':
            axes[0].xaxis.set_major_formatter(ticks)
        elif axis == 'y':
            axes[0].yaxis.set_major_formatter(ticks)
        
    
    if axis == 'y' and sharey:
        axes[0].get_shared_y_axes().join(*axes)
        
    if lim:
        if axis == 'x':
            axes[0].set_xlim(*[li/factor for li in lim])
        elif axis == 'y':
            for a in axes:
                a.set_ylim(*[li/factor for li in lim])
        
    return fig, axes


