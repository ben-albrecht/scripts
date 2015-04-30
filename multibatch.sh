#!/bin/bash -l
#PBS -N test_multi
#####PBS -q debug
#PBS -l nodes=9:ppn=16,walltime=30:00
#PBS -j oe

cd $PBS_O_WORKDIR

# Job parameters
let total_cores=144
let cores_per_job=16
let jobs_per_batch=`expr $total_cores / $cores_per_job`
echo "Total number of cores: " $total_cores
echo "Cores per job: " $cores_per_job
echo "Jobs per batch: " $jobs_per_batch

# Load modules
module load cp2k
PROGRAM=`which cp2k.popt`
JOB=Pt55_SiO2

echo "Begin:"
date

#for n in $(seq 0 10); do
  #Assume jobs run in separate directories, job1, job2, ...
#  for i in $(seq $jobs_per_batch); do
    #cd job.$n.$i

for i in $(seq 0 9); do
  for j in $(seq 0 8); do
    #write hostfile for i-th job to use
    let lstart=($i-1)*${cores_per_job}+1
    let lend=${lstart}+${cores_per_job}-1
    sed -n ${lstart},${lend}'p' < $PBS_NODEFILE >nodefile$i

    mpirun -np $cores_per_job -hostfile nodefile$i $PROGRAM $JOB.$n.$i_opt.in >& $JOB.$n.$i_opt.out &

    #cd ..
  done

  wait
done

echo "End:"
date
