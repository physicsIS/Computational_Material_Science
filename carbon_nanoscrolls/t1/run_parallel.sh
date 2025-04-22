#!/bin/bash
#SBATCH --partition=gpu
#SBATCH --account=gpu-24h
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=4                # 1 MPI task per node
#SBATCH --gpus-per-node=4         # Request 1 GPU could be 2 or more
#SBATCH --job-name="c1_md"
#SBATCH --output=qe_output.%j.out
#SBATCH --mail-user=elmer.barquero@ucr.ac.cr
#SBATCH --mail-type=END,FAIL

# Move to working directory
cd /home/elmer.barquero/carbon_nn

# Load required modules
module purge
module load qe/7.3.1-gpu
module list 

# Set environment variables
export OMP_NUM_THREADS=1

# Run Quantum Espresso with MPI
mpirun -n $SLURM_NTASKS pw.x -i pw.in > pw.out

