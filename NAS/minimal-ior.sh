#!/bin/sh
#PBS -q devel
#PBS -l select=1:ncpus=8:mpiprocs=8:mem=2gb:model=san
#PBS -N MinimalIOR

module load mpi-sgi mpi-hpcx comp-intel

cd "$PBS_O_WORKDIR/ior-3.3.0"

# Writes and reads 1mebibyte of data per processor
mpirun -np 8 ./src/ior

