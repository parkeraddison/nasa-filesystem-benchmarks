#!/bin/sh
#PBS -l select=4:ncpus=16:mpiprocs=16:model=san
#PBS -N IORSweep

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
#mpirun -np 8 "$path_to_ior"


#> Now we go ahead and run an IOR parameter sweep with a python script.
# First load in the python module, then run the script.
module load python3/3.7.0

# TODO: This needs to be revised -- right now we're just checking to see if any
# parameter_sweep.py exists at the current working directory, if not we run one
# from the home directory... but this is just in lieu of proper configuration
# for the parameter sweep (rather than hard-coding options in the Python file)
if test -f "parameter_sweep.py"; then
    python3 parameter_sweep.py
else
    python3 ~/parameter_sweep.py
fi

