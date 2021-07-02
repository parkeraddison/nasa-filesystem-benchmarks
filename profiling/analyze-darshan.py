import darshan
import sys
import datetime
from glob import glob
from pathlib import Path

darshan.enable_experimental()

LOGPATH = Path(sys.env['darshan_log_dir'], '2021')

today = datetime.date.today().strftime(r'%-m/%-d')
nonemptydates = set(p.parts[-3:-1] for p in LOGPATH.glob('*/*/*'))
listing = ' | '.join(f'{d[0]}/{d[1]}' for d in sorted(nonemptydates))
date = input(f"""Desired date [{today}]:
{listing}
""") or today

logs = glob(str(Path(LOGPATH, date, '*')))
if len(logs) == 0:
    print(f'No logs found for {date}')
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

report = darshan.DarshanReport(file)

report.info()

job = report.metadata['job']

nprocs = job['nprocs']
runtime = job['end_time'] - job['start_time']

pdf = report.records['POSIX'].to_df()
pf = pdf['fcounters']
ps = pf.sum(axis=0)

hist = report.mod_agg_iohist('POSIX')

io = report.agg_ioops('POSIX')
