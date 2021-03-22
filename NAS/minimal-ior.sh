#!/bin/sh
#PBS -q devel
#PBS -l select=1:ncpus=8:mpiprocs=8:mem=2gb:model=san
#PBS -N MinimalIOR

module load mpi-sgi mpi-hpcx comp-intel

cd "$PBS_O_WORKDIR/ior-3.3.0"

# Should write and read a total of 2gb (8 procs * 16 segments of * 16mb)
mpirun -np 8 ./src/ior -t 1m -b 16m -s 16

