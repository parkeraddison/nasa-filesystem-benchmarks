NAS HECC
========

The NAS High-End Computing Capability (HECC) Project uses an [HPC environment with a separate front-end and compute nodes](https://www.nas.nasa.gov/hecc/support/kb/hpc-environment-overview_25.html). The process to run a benchmark is the following:
1. Create a script to load dependencies and run the benchmark
2. Submit the benchmark script as a batch job using the Portable Batch System (PBS)

There are multiple supercomputers within the NAS HPC environment. For now, only **Pleiades** is being explored.

You will need to have an NAS account and have access to the secure enclave to do anything. See https://www.nas.nasa.gov/hecc/support/kb/

## Benchmark script

A script is responsible for loading any software dependencies and running the actual commands -- in this case, loading openmpi-related modules and executing the IOR benchmark.

Additionally, a script can specify `qsub` options, also known as PBS directives which determine things like how many resources to request.

The following scripts are currently included in this directory:
- `ior-atloc.sh` -- loads dependencies and runs a small IOR test starting in whichever directory the `qsub` command was run from.

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
qsub ~/path/to/ior-atloc.sh
```

### On Lustre

To run the benchmark on the Lustre filesystem instead, simply navigate to the Lustre nobackup folder before submitting the job
```bash
cd ~/nobackup/$USER
```
then submit the job
```bash
qsub ~/path/to/ior-atloc.sh
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

On r301i1n10:
Current directory is /nobackup/paddison
IOR-3.3.0: MPI Coordinated Test of Parallel I/O
Began               : Sat Mar 27 15:44:43 2021
Command line        : /home6/paddison/ior-3.3.0/src/ior
Machine             : Linux r301i1n10
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
    Charged To               : g1119

    Job Stopped              : Sat Mar 27 15:44:47 2021
____________________________________________________________________
```

</details>

