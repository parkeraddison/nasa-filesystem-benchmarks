#!/bin/sh
#PBS -q devel
#PBS -l select=1:ncpus=8:mpiprocs=8:mem=2gb:model=san
#PBS -N MinimalIOR

module load mpi-hpcx comp-intel

cd "$PBS_O_WORKDIR/ior-3.3.0"

# Does a read and write on 1 mebibyte of data for each process, 8MiB in total
mpirun -np 8 ./src/ior

