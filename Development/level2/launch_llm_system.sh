#!/bin/bash

# Name of your Conda environment
CONDA_ENV="dash_lab"

# Path to conda.sh (adjust this if your Conda installation is in a different location)
CONDA_SH="$HOME/miniconda3/etc/profile.d/conda.sh"

# Source conda.sh to ensure conda command is available
source "$CONDA_SH"

# Activate Conda environment
conda activate $CONDA_ENV

# Start the server
python server.py &

# Wait for the server to start
sleep 2

# Start multiple clients
python client.py 1 "What is the capital of France?" &
python client.py 2 "Explain quantum computing" &
python client.py 3 "Who wrote Romeo and Juliet?" &

# Wait for all background processes to finish
wait

# Deactivate Conda environment
conda deactivate

echo "All processes completed"