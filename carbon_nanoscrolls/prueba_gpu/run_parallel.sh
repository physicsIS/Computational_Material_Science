#!/bin/bash
#SBATCH --partition=gpu
#SBATCH --time=24:00:00
#SBATCH --nodes=2                   # Use 2 nodes
#SBATCH --ntasks-per-node=3         # Run 3 MPI tasks on each node
#SBATCH --gpus-per-node=3           # Request 3 GPUs on each node
#SBATCH --cpus-per-task=16          # Allocate 16 CPU cores to each MPI task
#SBATCH --job-name="2"
#SBATCH --output=qe_output.%j.out
#SBATCH --mail-user=tomas.rojas_s@ucr.ac.cr
#SBATCH --mail-type=END,FAIL

# Move to working directory
cd /home/tomas.rojas_s/alcl4/c2

# Load required modules
module purge
module load qe/7.3.1-gpu

# Set OpenMP threads to match the cpus requested per task
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

# Run Quantum Espresso using 6 GPUs with 3 k-pools
# Total MPI tasks ($SLURM_NTASKS) will be 6.
# Each of the 3 k-pools will be handled by 2 MPI tasks (2 GPUs).
mpirun pw.x -npool 3 -in pw.in > pw.out
