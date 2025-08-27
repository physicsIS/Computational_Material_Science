#!/bin/bash
#SBATCH --partition=parallel
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8          # Request 8 MPI tasks
#SBATCH --cpus-per-task=8            # Allocate 8 CPUs for each task
#SBATCH --job-name="2v"
#SBATCH --output=qe_output.%j.out
#SBATCH --mail-user=tomas.rojas_s@ucr.ac.cr
#SBATCH --mail-type=END,FAIL

module purge
module load qe/7.3.1-cpu

cd /home/tomas.rojas_s/vertical/2

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

mpirun pw.x -in pw.in > pw.out
