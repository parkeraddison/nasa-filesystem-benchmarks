#!/bin/bash
set -e

# Minimal IOR test
# ================
#
# NOTE: Assumes this is being executed from the same directory which contains
# ior executable.
#

mpirun -n 10 ./ior -t 1m -b 16m -s 16