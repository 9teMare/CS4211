#!/bin/bash

# The directory containing your zip files
ZIP_DIR="models/compressed_models"

# The directory where you want to extract them
EXTRACT_DIR="models/generated_models"

# Create the EXTRACT_DIR if it does not exist
mkdir -p "$EXTRACT_DIR"

# Iterate over each zip file in ZIP_DIR
for zip_file in "$ZIP_DIR"/*.zip; do
  # Extract the base name of the zip file
  base_name=$(basename "$zip_file" .zip)

  # Create a directory for the zip file's contents
  mkdir -p "$EXTRACT_DIR/$base_name"

  # Unzip the file to the directory
  unzip -o "$zip_file" -d "$EXTRACT_DIR/$base_name"
done
