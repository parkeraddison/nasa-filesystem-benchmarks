#!/bin/sh
#PBS -q devel
#PBS -l select=1:ncpus=8:mpiprocs=8:mem=2gb:model=san
#PBS -N BasicIOR

# ^ Directives (same as `qsub` options):
#
# - Use the specified job queue (devel only for debugging purposes!)
# - Select n chunks of m cpus and p gb of ram from a specific model of node
# - Name it
#
# See: https://www.nas.nasa.gov/hecc/support/kb/commonly-used-qsub-command-options_175.html
# See: `man qsub`
#

# `mpi-hpcx` loads in the necessary MPI libraries, `comp-intel` loads in some
# required math libraries. See "### Dependency issues" in notes.
#
# Turns out mpi-sgi is not needed -- the hpcx module loads in mpirun and all
# hpcx libraries appear to be favored over sgi libraries.
module load mpi-hpcx comp-intel

# We can't run `make install` because we don't have permissions for
# `/usr/local/bin`, but we can just use the path to the file directly.
#
# We're not quoting the ~/ so that it has a chance to expand, but we do quote
# the rest of the path just in case it as has spaces (it doesn't, but habit).
path_to_ior=~/"ior-3.3.0/src/ior"

# Whichever directory we run `ior` from will be used for the filesystem test,
# unless we specify different files with the options. So, we navigate to our
# desired filesystem directory now.
#
# For now, let's just assume that whatever directory this job is being submitted
# from is the desired directory. We can add to this later with some config using
# environment variables or multiple different scripts.
#
# By default we already start out in the working directory where `qsub` was run,
# but it doesn't hurt to be explicit (again, we'll revisit this later).
cd "$PBS_O_WORKDIR"

# Finally, let's actually run IOR. Without any options, a call to IOR will read
# and write 1 mebibyte for each process.
#
# Note that we can use environment variables set by PBS to reference the number
# of cpus and mpiprocs we have available.
# See: https://www.nas.nasa.gov/hecc/support/kb/default-variables-set-by-pbs_189.html

# Does a read and write on 1 mebibyte of data for each process, 8MiB total.
mpirun -np 8 "$path_to_ior"

