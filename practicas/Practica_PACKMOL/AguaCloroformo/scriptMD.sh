#!/bin/bash
#SBATCH --partition=nu-long
#SBATCH --time=72:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=64
#SBATCH --job-name="MD_Simulation"
#SBATCH --output=test.out
#SBATCH --mail-user=jose.alvarezcastrillo@ucr.ac.cr
#SBATCH --mail-type=END,FAIL

module load quantum-espresso/7.2-oneAPI-2021.1-parallel
srun pw.x -i pw.in > pw.out 64

