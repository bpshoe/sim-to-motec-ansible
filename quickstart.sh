#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy config file if it doesn't exist
if [ ! -f "config.yml" ]; then
    cp config.yml.example config.yml
fi

# Run a sample parse and .ld export
python gt7.py

echo "Success: .ld file generated at path specified in config.yml"
