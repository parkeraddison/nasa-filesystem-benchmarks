import darshan
import sys
import datetime
from glob import glob
from pathlib import Path

darshan.enable_experimental()

LOGPATH = Path(sys.env['darshan_log_dir'], '2021')

today = datetime.date.today().strftime(r'%-m/%-d')
nonemptydates = set(p.parts[-3:-1] for p in Path(LOGPATH).glob('*/*/*'))
listing = ' | '.join(f'{d[0]}/{d[1]}' for d in sorted(nonemptydates))
date = input(f"""Desired date [{today}]:
{listing}
""") or today

def choose_log(curr_path):
    logs = glob(str(Path(curr_path, '*')))
    if len(logs) == 0:
        print(f'No logs found in {curr_path}')
        exit(1)
    elif len(logs) == 1:
        file = logs[0]
        print(f'File: {file}')
    else:
        listing = '\n'.join(f'({i+1}) {fname}' for i, fname in enumerate(logs))
        loc = input(f"""Desired file [1]:
{listing}
""") or 1
        file = logs[int(loc)-1]
    return file

path = Path(LOGPATH, date)
while Path(path).is_dir():
    path = choose_log(path)

report = darshan.DarshanReport(str(path))

report.info()

job = report.metadata['job']

nprocs = job['nprocs']
runtime = job['end_time'] - job['start_time']

pdf = report.records['POSIX'].to_df()
pf = pdf['fcounters']
ps = pf.sum(axis=0)

sdf = report.records['STDIO'].to_df()
sf = sdf['fcounters']
ss = sf.sum(axis=0)

hist = report.mod_agg_iohist('POSIX')

io = report.agg_ioops('POSIX')