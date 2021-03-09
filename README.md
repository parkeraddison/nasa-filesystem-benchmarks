# filesystem-benchmarks

## Deploy
```
k create -f volumes/block.yml
k create -f minimal-deploy.yml
```

## Installing

These commands are run in the pod.

Dependencies. See: https://github.com/hpc/ior/blob/main/testing/docker/ubuntu16.04/Dockerfile

```
apt-get update
apt-get install -y libopenmpi-dev openmpi-bin mpich git pkg-config gcc git vim less curl wget
apt-get install -y sudo
```

Configuration. See `./configure --help`.

```
./configure
```

Installation
```
make
```

<!-- 
This didn't seem to work!

I think there's now supposed to be an IOR file that I can run.

Ah, there is one in `src`...
 -->

## Running

See: https://ior.readthedocs.io/en/latest/userDoc/tutorial.html

```
cd src
./ior ...
```
or
```
mpirun ...
```
<!-- 
Not sure how to really use it yet.

When I run ior it does a test instantly it seems.

When I tried doing
```
mpirun -n 64 ./ior -t 1m -b 16m -s 16
```
I got a ton of:
```
ior ERROR: open64("testFile", 66, 0664) failed, errno 13, Permission denied (aiori-POSIX.c:412)
...
[filebench-574869c787-pdn62:07749] PMIX ERROR: UNREACHABLE in file ../../../src/server/pmix_server.c at line 2193
...
```

Also note that I ran `useradd testu` and `su testu` because MPIrun doesn't want to be run as a root user. But this user has no permissions! I think that's the issue.

Seems like a `chmod -R 777 .` as the root fixed this!
-->

For example, run 10 tasks with a transfer size of 1m(egabyte?), a block size of 16m(egabyte?), and a segment count of 16:
```
mpirun -n 10 ./src/ior -t 1m -b 16m -s 16
```

<details>
    <summary>
        Output:
    </summary>

```raw
IOR-3.3.0: MPI Coordinated Test of Parallel I/O
Began               : Mon Mar  8 23:08:17 2021
Command line        : ./src/ior -t 1m -b 16m -s 16
Machine             : Linux filebench-574869c787-pdn62
TestID              : 0
StartTime           : Mon Mar  8 23:08:17 2021
Path                : /storage/ior-3.3.0
FS                  : 8.0 GiB   Used FS: 0.5%   Inodes: 4.0 Mi   Used Inodes: 0.0%

Options: 
api                 : POSIX
apiVersion          : 
test filename       : testFile
access              : single-shared-file
type                : independent
segments            : 16
ordering in a file  : sequential
ordering inter file : no tasks offsets
nodes               : 1
tasks               : 10
clients per node    : 10
repetitions         : 1
xfersize            : 1 MiB
blocksize           : 16 MiB
aggregate filesize  : 2.50 GiB

Results: 

access    bw(MiB/s)  IOPS       Latency(s)  block(KiB) xfer(KiB)  open(s)    wr/rd(s)   close(s)   total(s)   iter
------    ---------  ----       ----------  ---------- ---------  --------   --------   --------   --------   ----
write     678.06     678.07     0.118931    16384      1024.00    0.770489   3.78       3.59       3.78       0   
read      4233       4234       0.019146    16384      1024.00    0.000035   0.604695   0.298354   0.604706   0   
remove    -          -          -           -          -          -          -          -          3.20       0   
Max Write: 678.06 MiB/sec (711.00 MB/sec)
Max Read:  4233.46 MiB/sec (4439.11 MB/sec)

Summary of all tests:
Operation   Max(MiB)   Min(MiB)  Mean(MiB)     StdDev   Max(OPs)   Min(OPs)  Mean(OPs)     StdDev    Mean(s) Stonewall(s) Stonewall(MiB) Test# #Tasks tPN reps fPP reord reordoff reordrand seed segcnt   blksiz    xsize aggs(MiB)   API RefNum
write         678.06     678.06     678.06       0.00     678.06     678.06     678.06       0.00    3.77548         NA            NA     0     10  10    1   0     0        1         0    0     16 16777216  1048576    2560.0 POSIX      0
read         4233.46    4233.46    4233.46       0.00    4233.46    4233.46    4233.46       0.00    0.60471         NA            NA     0     10  10    1   0     0        1         0    0     16 16777216  1048576    2560.0 POSIX      0
Finished            : Mon Mar  8 23:08:25 2021
```
</details>


