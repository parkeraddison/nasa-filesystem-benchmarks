import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import json
import glob
# import darshan
# darshan.enable_experimental()

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

def plot_bw(default, striped=None, ax=None):
    
    if ax is not None:
        plot = ax
    else:
        plot = plt
    
    plot.plot(default.transferSize/1024**1, default.bwMeanMIB, label='Default configuration')
    plot.fill_between(default.transferSize/1024,
                 default.bwMeanMIB - default.bwStdMIB,
                 default.bwMeanMIB + default.bwStdMIB,
                 alpha=0.1
                )
    
    if striped is not None:
        plot.plot(striped.transferSize/1024**1+(striped.transferSize/1024/15), striped.bwMeanMIB, label='Stripe count = 1')

        plot.fill_between(striped.transferSize/1024,
                         striped.bwMeanMIB - striped.bwStdMIB,
                         striped.bwMeanMIB + striped.bwStdMIB,
                         alpha=0.1
                        )
        
    plot.fill_between([4],[4],[4],alpha=0.1,color='black',label='Standard Deviation')
    plot.legend(loc='upper left')
    plot.xscale('log')
    ticks = matplotlib.ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x*100))
    plot.xticks(default.transferSize/1024, ['4K', '16K', '64K', '256K', '512K', '1M', '2M', '4M', '8M', '16M', '32M'], rotation=-60)
    plot.xlabel('Transaction size')
    plot.ylabel('Mean  Read Bandwidth (MiB/s)')
    plot.title(f'{default.fs[0]} {default.API[0]}')
    
    
    plt.ylim(0,1600)
