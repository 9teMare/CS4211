#!/bin/bash

# setup_environment.sh

if [ -f myenv/setup_complete ]; then
    rm -f myenv/setup_complete
fi

# Create a Python virtual environment if it doesn't exist
if [ ! -d "myenv" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv myenv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source myenv/bin/activate

# Upgrade pip to the latest version
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies from requirements.txt
echo "Installing Python packages from requirements.txt..."
pip install -r requirements.txt

# Remove previously generated models
echo "Removing previously generated models..."
rm -rf models/generated_models/*

echo "Environment setup completed. Ready to run jobs."
