#!/bin/bash
#SBATCH --partition=kura
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=20
#SBATCH --job-name="pw0"
#SBATCH --output=test.out
#SBATCH --mail-user=elmer.barquero@ucr.ac.cr
#SBATCH --mail-type=END,FAIL
. /opt/Modules/3.2.10/init/sh
module load quantum-espresso/7.2-oneAPI-2021.1-parallel
srun pw.x -i pw0.in > pw0.out 20


