#!/bin/bash

#SBATCH --partition=physical
#SBATCH --time=00:20:00
#SBATCH --nodes=2
#SBATCH --ntasks=8

module load Python/3.4.3-goolf-2015a

mpirun python Assign1_Final.py
