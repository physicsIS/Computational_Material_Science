#!/bin/bash
#SBATCH --partition=parallel
#SBATCH --account=parallel-24h   # <-- IMPORTANTE añadir esta línea correctamente
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64
#SBATCH --job-name="1v"
#SBATCH --output=qe_output.%j.out
#SBATCH --mail-user=tomas.rojas_s@ucr.ac.cr
#SBATCH --mail-type=END,FAIL

module purge
module load qe/7.3.1-cpu

cd /home/tomas.rojas_s/vertical/1

mpirun -np $SLURM_NTASKS pw.x -in pw.in > pw.out

