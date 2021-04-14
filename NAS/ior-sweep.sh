#!/bin/sh
#PBS -q devel
#PBS -l select=1:ncpus=8:mpiprocs=8:model=san
#PBS -N IORSweep

# IOR Sweep PBS job script
# ========================
#
# To run:
# ```
# qsub [<over-ride directives>] -v IORFILE=/path/to/iorfile.json path/to/ior-sweep.sh
# ```

# Directives (same as `qsub` options):
#
# - Use the specified job queue (devel only for debugging purposes!)
# - Select n chunks of m cpus and p gb of ram from a specific model of node
# - Name it
#
# See: https://www.nas.nasa.gov/hecc/support/kb/commonly-used-qsub-command-options_175.html
# See: `man qsub`
#

# The mpi-hpe/mpt module is the recommended MPI module.
module load mpi-hpe/mpt

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

# Now we go ahead and run an IOR parameter sweep with a python script. The full
# sweep job is defined by a JSON file which we pass as the argument.

# First load in the python module, then run the script.
module load python3/3.7.0
# NOTE: For now we're using the environment variable IORFILE.
python3 ~/benchmarks/ior/parameter_sweep.py "$IORFILE"

