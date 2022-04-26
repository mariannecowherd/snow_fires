#!/bin/bash
#SBATCH -t 00:30:00  # time requested in hour:minute:second
#SBATCH -N 1      # nodes requested
# Partition:
#SBATCH --partition=savio
# Account
#SBATCH --account=fc_mgirotto



module load python
#run the application:
source activate snow
python /global/home/users/cowherd/snow_fires/scripts/prep_data.py
