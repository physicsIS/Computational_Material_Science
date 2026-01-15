#!/bin/bash
#SBATCH --partition=gpu                  
#SBATCH --time=24:00:00
#SBATCH --nodes=1                       
#SBATCH --ntasks-per-node=4             
#SBATCH --cpus-per-task=16              
#SBATCH --gpus-per-node=4          
#SBATCH --job-name="gpu_1node"
#SBATCH --output=qe_output_gpu.%j.out
#SBATCH --mail-user=tomas.rojas_s@ucr.ac.cr
#SBATCH --mail-type=END,FAIL

module purge
module load qe/7.3.1-gpu # Make sure this is the correct name for the GPU version

cd /home/tomas.rojas_s/interface

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

mpirun pw.x -in pw.in > pw.out
