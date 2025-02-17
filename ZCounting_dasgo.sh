#!/bin/bash

# Output file for the fetched files
output_file="missing_files_list.txt"

# Clear the output file if it exists
> $output_file

# Dataset to fetch files from
dataset="/Muon0/Run2024D-ZMu_PromptMUODPGNano-v2/NANOAOD"
#file dataset=/Muon0/Run2024D-ZMu_PromptMUODPGNano-v2/NANOAOD run=380626

# Function to fetch files and save to the output file
get_files() {
    local dataset=$1
    echo "Fetching files for dataset: $dataset"
    dasgoclient --query="file dataset=$dataset" --limit=0 >> $output_file
}

# Fetch files from the specified dataset
get_files $dataset

echo "File fetching complete."
