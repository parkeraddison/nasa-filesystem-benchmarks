NAS HECC
========

- [Getting started](#getting-started)
  - [Running code](#running-code)
  - [Dependencies](#dependencies)
- [Development](#development)
  - [VNC Desktop](#vnc-desktop)
  - [Jupyter Notebooks](#jupyter-notebooks)
  - [Transferring files](#transferring-files)
- [Old](#old)
- [Benchmark script](#benchmark-script)
- [Running](#running)
  - [On NFS](#on-nfs)
  - [On Lustre](#on-lustre)
  - [Parameter sweep configuration](#parameter-sweep-configuration)
  - [Checking the status of your job](#checking-the-status-of-your-job)
- [Output](#output)
  - [Parsing and visualizing output](#parsing-and-visualizing-output)

## Getting started

The NAS-operated High-End Computing Capability (HECC) Project uses an [HPC environment with a separate front-end and compute nodes](https://www.nas.nasa.gov/hecc/support/kb/hpc-environment-overview_25.html). To do anything, first remote into a front-end node, either the general secure front end `ssh sfe` or directly to a Pleiades front end `ssh pfe` (preferred).

First time working with NAS should see https://www.nas.nasa.gov/hecc/support/kb/new-user-orientation-161/.

### Running code

We can run some code on a front end node, like compiling software, moving items about, and launching a VNC desktop environment. However, when its time to run an intensive application, it's best to use a compute node. This can be done by using a PBS job, PBS interactive session, or requesting a dedicated compute node.

- [PBS Jobs and Interactive sessions](https://www.nas.nasa.gov/hecc/support/kb/pbs-on-pleiades-122/)
  - `qsub -N UsesJobScript -l select=1:model=san:ncpus=1 -q devel`
  - `qsub -I -q devel`
- [Dedicated compute nodes](https://www.nas.nasa.gov/hecc/support/kb/reserving-a-dedicated-compute-node_556.html)
  - `pbs_rfe --model san --duration 3`

### Dependencies

Software dependencies are typically loaded via modules.

- [Software modules](https://www.nas.nasa.gov/hecc/support/kb/using-software-modules_115.html)
  - `module load mpi-hpe`
  - `module load pkgsrc` (see https://www.nas.nasa.gov/hecc/support/kb/software-on-nas-systems_116.html)

## Development

### VNC Desktop

A VNC desktop environment can be run from any node to provide a graphical interface -- very helpful for things like viewing images or pdfs, or doing manual file reorganization/renaming that would be tedious on the command line.

```bash
vncserver -localhost
# "New desktop is at pfe:XX"
# Port-forward. ~C will escape to the ssh shell
~C
-L 59XX:localhost:59XX

# On local machine, use VNC client to connect to localhost:59XX

# When finished
vncserver -kill :XX
```

- [VNC documentation](https://www.nas.nasa.gov/hecc/support/kb/vnc-a-faster-alternative-to-x11_257.html)

### Jupyter Notebooks

The de-facto method of developing, visualizing, and sometimes even running Python code is (should be) through Jupyter notebooks. A Jupyter Lab enviroment allows you to run an integrated terminal and view multiple files at once. Jupyter must be run from a compute node, either from an interactive PBS session or a reserved node.

First time working with Jupyter on NAS should see https://www.nas.nasa.gov/hecc/support/kb/secure-setup-for-using-jupyter-notebook-on-nas-systems_622.html

```bash
qsub -I -l select=1:model=san:ncpus=8 # Use `-q devel` if you'll be working for under 2 hours
# Note the pfeXX number and the rXX node name
module use -a /swbuild/analytix/tools/modulefiles
module load miniconda3/v4
source activate pyt1_8 # PyTorch; Can use other conda environments,
jupyter lab --no-browser
```

On the local machine, we must ssh directly to the compute node in order to access Jupyter
```bash
function nasjupyter {
    ssh -o "StrictHostKeyChecking ask" -L 8888:localhost:8888 -o ProxyJump=sfe,"$1" "$2"
}

nasjupyter pfeXX rXX
```

Now, go to `https://localhost:8888` in a browser, accept the unverified certificate warning (some browsers don't show this... I had the best luck with Firefox), and then finally go on and use Jupyter!

- [Jupyter for machine learning on NAS](https://www.nas.nasa.gov/hecc/support/kb/using-jupyter-notebook-for-machine-learning-development-on-nas-systems_576.html)
- [Conda environments](https://www.nas.nasa.gov/hecc/support/kb/machine-learning-overview_572.html)

### Transferring files

Front end nodes have internet access, so tools like `wget` or `git` can be used to download datasets or software. To transfer files to and from the local system, a few tools can be used, including `scp` (small files) and `shift` (massive files).

- [Remote transfers documentation](https://www.nas.nasa.gov/hecc/support/kb/remote-file-transfer-commands_142.html)
  - `scp file_to_upload pfe:path_for_file`
  - `scp -r pfe:directory_to_download path_for_directory`

---
Old
---

## Benchmark script

 The process to run a benchmark is the following:
1. Create a script to load dependencies and run the benchmark
2. Submit the benchmark script as a batch job using the Portable Batch System (PBS)

There are multiple supercomputers within the NAS HPC environment. For now, only **Pleiades** is being explored.

You will need to have an NAS account and have access to the secure enclave to do anything. See https://www.nas.nasa.gov/hecc/support/kb/

A script is responsible for loading any software dependencies and running the actual commands -- in this case, loading openmpi-related modules and executing the IOR benchmark.

Additionally, a script can specify `qsub` options, also known as PBS directives which determine things like how many resources to request.

The following scripts are currently included in this directory:
- `ior-atloc.sh` -- loads dependencies and runs a small IOR test starting in whichever directory the `qsub` command was run from.
- `ior-sweep.sh` -- runs multiple IOR tests sweeping over a single parameter specified in `parameter_sweep.py`. Uses whichever directory the `qsub` command was run from.

## Running

To run the script, simply use `qsub <path_to_script>` from whichever directory you want to serve as the testing grounds. The script `ior-atloc.sh` can be submitted to do so.

Additional PBS directives such as which queue to run on, how many resources to request, and what type of node to run on can all be modified within the script file itself on lines prefixed by `#PBS` or when submitting the job using `qsub` options. They are equivalent.

See: https://www.nas.nasa.gov/hecc/support/kb/commonly-used-qsub-command-options_175.html

### On NFS

For example, to run the IOR benchmark on an NFS mounted filesystem, navigate to some directory at your home folder
```bash
cd ~
```
then submit the IOR job
```bash
qsub ~/path/to/ior-script.sh
```

### On Lustre

To run the benchmark on the Lustre filesystem instead, simply navigate to the Lustre nobackup folder before submitting the job
```bash
cd ~/nobackup/$USER
```
then submit the job
```bash
qsub ~/path/to/ior-script.sh
```

### Parameter sweep configuration

To run a parameter sweep, create a job json as seen in [/benchmarks/ior/](/benchmarks/ior/) and submit `ior-sweep.sh` with an environment variable named IORFILE which points to that jobfile. Optionally override PBS directives (the queue, the number of resources selected, the job name, etc).

For example, the following command will submit a job from a make-believe job json in the current directory, while also changing the PBS job name and resource selection.
```bash
qsub -v IORFILE=$(pwd)/make-believe.json -N MakeBelieveName -l select=1:ncpus=1:mpiprocs=1:model=bro ~/path/to/ior-sweep.sh
```

### Checking the status of your job

It's useful to make sure that the job is running or see that it's still queued by running
```bash
watch qstat -u $USER
```

## Output

Code to parse and visualize the output will come later. For now, you will see two files show up in the directory where you ran `qsub`. Both files will be prefixed by the name (-N option) of the script (probably "BasicIOR") followed by a `.e` or `.o` and some numbers. These are the *error* and *output* files, respectively. The full stderr will be shown in the `e` file. The PBS request, then stdout, then PBS summary will be shown in the `o` file.

If all is right in the world, the `e` file should be empty, and the `o` file should look something like this:
<details>
  <summary>BasicIOR.o10864291</summary>

```
Job 10864291.pbspl1.nas.nasa.gov started on Sat Mar 27 15:44:35 PDT 2021
The job requested the following resources:
    mem=2gb
    ncpus=8
    place=scatter:excl
    walltime=02:00:00

PBS set the following environment variables:
        FORT_BUFFERED = 1
                   TZ = PST8PDT

On *****:
Current directory is /nobackup/paddison
IOR-3.3.0: MPI Coordinated Test of Parallel I/O
Began               : Sat Mar 27 15:44:43 2021
Command line        : /home6/paddison/ior-3.3.0/src/ior
Machine             : Linux *****
TestID              : 0
StartTime           : Sat Mar 27 15:44:43 2021
Path                : /nobackupp12/paddison
FS                  : 1625.2 TiB   Used FS: 31.3%   Inodes: 381.2 Mi   Used Inodes: 12.6%

Options:
api                 : POSIX
apiVersion          :
test filename       : testFile
access              : single-shared-file
type                : independent
segments            : 1
ordering in a file  : sequential
ordering inter file : no tasks offsets
nodes               : 1
tasks               : 8
clients per node    : 8
repetitions         : 1
xfersize            : 262144 bytes
blocksize           : 1 MiB
aggregate filesize  : 8 MiB

Results:

access    bw(MiB/s)  IOPS       Latency(s)  block(KiB) xfer(KiB)  open(s)    wr/rd(s)   close(s)   total(s)   iter
------    ---------  ----       ----------  ---------- ---------  --------   --------   --------   --------   ----
write     912.40     4282       0.001868    1024.00    256.00     0.001203   0.007473   0.000973   0.008768   0
read      495.76     2259.33    0.000031    1024.00    256.00     0.015838   0.014163   0.014007   0.016137   0
remove    -          -          -           -          -          -          -          -          0.006066   0
Max Write: 912.40 MiB/sec (956.72 MB/sec)
Max Read:  495.76 MiB/sec (519.84 MB/sec)

Summary of all tests:
Operation   Max(MiB)   Min(MiB)  Mean(MiB)     StdDev   Max(OPs)   Min(OPs)  Mean(OPs)     StdDev    Mean(s) Stonewall(s) Stonewall(MiB) Test# #Tasks tPN reps fPP reord reordoff reordrand seed segcnt   blksiz    xsize aggs(MiB)   API RefNum
write         912.40     912.40     912.40       0.00    3649.62    3649.62    3649.62       0.00    0.00877         NA            NA     0      8   8    1   0     0        1         0    0      1  1048576   262144       8.0 POSIX      0
read          495.76     495.76     495.76       0.00    1983.04    1983.04    1983.04       0.00    0.01614         NA            NA     0      8   8    1   0     0        1         0    0      1  1048576   262144       8.0 POSIX      0
Finished            : Sat Mar 27 15:44:43 2021

____________________________________________________________________
Job Resource Usage Summary for 10864291.pbspl1.nas.nasa.gov

    CPU Time Used            : 00:00:04
    Real Memory Used         : 2288kb
    Walltime Used            : 00:00:04
    Exit Status              : 0

    Memory Requested         : 2gb
    Number of CPUs Requested : 8
    Walltime Requested       : 02:00:00

    Execution Queue          : devel
    Charged To               : *****

    Job Stopped              : Sat Mar 27 15:44:47 2021
____________________________________________________________________
```

</details>

### Parsing and visualizing output

The functions provided in benchmarks/ior/parse_output.py can be used to quickly parse and plot the output ('o') files resulting from an IOR test or parameter sweep run as a PBS job. The following code loads in the data and plots a desired value versus the swept parameter.
```python
from parse_output.py import *

# Parse the data into a table (DataFrame)
data = extract_runs('path/to/IOROutput.o...')
# Plot read and write performance values versus the swept parameter
# (in this case, mean operations per second versus number of concurrent tasks)
fig, ax = make_plot(data, 'tasks', 'OPsMean')
```

