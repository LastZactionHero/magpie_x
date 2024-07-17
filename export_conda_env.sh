#!/bin/bash

ENV_NAME=magpiex

# Activate the specified Conda environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate $ENV_NAME

# Check if the environment was successfully activated
if [ $? -ne 0 ]; then
  echo "Failed to activate environment: $ENV_NAME"
  exit 1
fi

# Export the environment configuration to a YAML file
conda env export > environment.yml

# Check if the export was successful
if [ $? -ne 0 ]; then
  echo "Failed to export environment: $ENV_NAME"
  exit 1
fi

# Add the YAML file to Git and commit
git add environment.yml

# Check if there are any changes to commit
if git diff-index --quiet HEAD; then
  echo "No changes to commit"
else
  git commit -m "Update Conda environment configuration for $ENV_NAME"
  git push
fi

echo "Conda environment updated and changes pushed to Git."

