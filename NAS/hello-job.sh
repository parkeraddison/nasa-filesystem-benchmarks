#!/bin/sh
#PBS -q devel
#PBS -l select=1:ncpus=1:mem=1gb:model=san
#PBS -N HelloJob
echo "Hello"

