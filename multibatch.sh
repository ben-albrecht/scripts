#!/bin/bash -l
#PBS -N test_multi
#####PBS -q debug
#PBS -l nodes=9:ppn=16,walltime=30:00
#PBS -q dist_big
#PBS -j oe

cd $PBS_O_WORKDIR

# Job parameters
let total_cores=144
let cores_per_job=16
let jobs_per_batch=`expr $total_cores / $cores_per_job`
echo "Total number of cores: " $total_cores
echo "Cores per job: " $cores_per_job
echo "Jobs per batch: " $jobs_per_batch

# Load Q-Chem Modules
module purge
module load intel/2013.0
module load qchem/dlambrecht
module load mpi

PROGRAM="$(which qchem) -nt $cores_per_job"
listofjobs=" "

echo "Begin:"
date

i=0
for job in $listofjobs; do
    #write hostfile for i-th job to use
    let node=($i)*$cores_per_job+1
    host=$(sed -n ${node}p $PBS_NODEFILE)
    echo "$job running on $host with $cores_per_job cores"
    mpirun -np 1 --host $host $PROGRAM $job.in $job.out &
    let i+=1
done

wait

echo "End:"
date
