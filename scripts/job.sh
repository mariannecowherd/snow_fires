#!/bin/bash
#SBATCH -t 0:01:00  # time requested in hour:minute:second
#SBATCH -N 1      # nodes requested
# Partition:
#SBATCH --partition=savio
# Account
#SBATCH --account=fc_mgirotto



module load python
#run the application:
source activate snow
python /global/home/users/cowherd/snow_fires/scripts/test.py
source deactivate
