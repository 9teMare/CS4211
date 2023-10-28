#!/bin/bash

# Name of job
#SBATCH --job-name=cs4211_model_creator

# Just use the standard partition, we can use all cpus on the partition
#SBATCH --partition=standard

# Time for job, probably need something less tbh
#SBATCH --time=00:30:00

# Good to check on jobs and their success
#SBATCH --output=logs/cs4211_model_creator_%j.slurmlog
#SBATCH --error=logs/cs4211_model_creator_%j.slurmlog

#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --mail-type=ALL

echo "DEBUG: All Slurm environment variables for this job"
printenv | grep SLURM

echo "Job is running on $(hostname), started at $(date)"

echo "Installing Python packages from requirements.txt..."
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt

echo "Removing previously generated models..."
rm -rf models/generated_models/*

echo "Running model generation!"
./create_pcsp_models.py

echo -e "\n====> Finished running.\n"

echo -e "\nJob completed at $(date)"
