import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
from parse_output import *

def quick_plot(data, param='infer', measure='bandwidth', sharey=True):

    if type(data) == pd.DataFrame:
        df = data
        fp = False
    else:
        # Assume this is a filepath. We can also check to see if it's a glob
        fp = data
        if '*' in fp:
            df = pd.concat([parse_ior(f) for f in sorted(glob(fp))])
        else:
            df = parse_ior(fp)

    if param == 'infer':
        assert fp, 'Parameter cannot be inferred from a dataframe. Please specify param= as second argument.'
        if 'transferSize' in fp:
            param = 'transferSize'
        elif 'blockSize' in fp:
            param = 'blockSize'
        elif 'numTasks' in fp:
            param = 'numTasks'
        elif 'segmentCount' in fp:
            param = 'segmentCount'
        else:
            print('Could not infer parameter. Please specify param= as second argument.')
            return

    if measure == 'bandwidth':
        f,a = make_plot(df, param, 'bwMeanMIB', 'bwStdMIB')
    elif measure == 'latency':
        f,a = make_plot(df, param, 'MeanTime')

    if param == 'transferSize':
        f,a = rescale_axis(f,a,'x',factor=1/KIBI,logbase=2)
    elif param == 'blockSize':
        f,a = rescale_axis(f,a,'x',factor=1/MEBI,logbase=2)

    f,a = rescale_axis(f,a,'y',lim=(0,),sharey=sharey)

    return f,a

