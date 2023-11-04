#!/bin/bash

inputs=(
  ""
  "backpasses_seqlimit_template.pcsp"
  "backpasses_sidepasses_seqlimit_template.pcsp"
  "backpasses_sidepasses_template.pcsp"
  "only_backpass_template.pcsp"
  "only_seqlimit_template.pcsp"
  "only_sidepass_template.pcsp"
  "sidepasses_seqlimit_template.pcsp"
)

# Iterate over the inputs and submit a job for each one
for input in "${inputs[@]}"; do
  sbatch ./create_pcsp_models_slurm_job.sh "$input"
done
