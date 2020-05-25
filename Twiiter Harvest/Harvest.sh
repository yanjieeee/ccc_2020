#!/bin/bash

#SBATCH --partition=physical
#SBATCH --time=00:02:00
#SBATCH --nodes=1
#SBATCH --ntasks=8

module load Python/3.7.1-GCC-6.2.0

python3 TweetsHarvester.py