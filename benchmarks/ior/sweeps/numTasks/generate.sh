#!/bin/bash

cd default/

for idx in {0..3}; do

    numTasks=16

    toAdd=$(($idx*$numTasks))

    # Rename old written files that would be overwritten
    for i in {0..15}; do
        rename $(printf %08d $i) $(printf %08d $(($i + ${toAdd}))) *
    done

    # Write new files
    mpiexec -np 16 ~/bin/ior -O summaryFile=write-default_$(($idx+1)).json -f ../write.ior
done

cd ../stripe1/

for idx in {0..3}; do

    numTasks=16

    toAdd=$(($idx*$numTasks))

    # Rename old written files that would be overwritten
    for i in {0..15}; do
        rename $(printf %08d $i) $(printf %08d $(($i + ${toAdd}))) *
    done

    # Write new files
    mpiexec -np 16 ~/bin/ior -O summaryFile=write-stripe1_$(($idx+1)).json -f ../write.ior
done
