#!/bin/bash
#SBATCH -N 1
#SBATCH -t 1:00:00
#SBATCH -p pdebug
#SBATCH --output=job%J.out
#SBATCH --error=job%J.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=scullyalliso1@llnl.gov

#--------#
# Quartz #
#--------#

srun -n 1 profile_driver.py

#
