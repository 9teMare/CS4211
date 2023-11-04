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
#SBATCH --mail-type=ALL
#SBATCH --cpus-per-task=24

input_file="$1"

echo "DEBUG: All Slurm environment variables for this job"
printenv | grep SLURM

echo "Job is running on $(hostname), started at $(date)"

echo "Installing Python packages from requirements.txt..."
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt

echo "Removing previously generated models..."
# Check if input file was provided
if [ -z "$input_file" ]; then
    echo "No input file provided, using base template..."
    # Remove base directory if no input file
    rm -rf models/generated_models/template_base_new/*
else
    # Extract file name without last 5 characters
    base_name="${input_file%?????}"
    echo "Input file provided, using $base_name..."
    # Remove directory based on input file name
    rm -rf "models/generated_models/$base_name"/*
fi

# Run model generation script with or without input file
if [ -z "$input_file" ]; then
    echo "Running model generation without input file..."
    ./create_pcsp_models.py
else
    echo "Running model generation with input file $input_file..."
    ./create_pcsp_models.py "$input_file"
fi

echo -e "\n====> Finished running.\n"

echo -e "\nJob completed at $(date)"
