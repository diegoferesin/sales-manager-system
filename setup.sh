#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create necessary directories if they don't exist
mkdir -p data
mkdir -p scripts
mkdir -p sql

# Create .env file for environment variables
touch .env

echo "Project setup completed successfully!"
echo "Don't forget to activate the virtual environment with: source venv/bin/activate"
