#!/bin/bash

# Install script to set up the environment and install dependencies

echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Installation complete."

echo "Creating necessary directories..."
mkdir -p chroma_db projects

echo "To get started, please source the start script:"
echo "    source start.sh"
