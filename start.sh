#!/bin/bash

# This script is intended to be sourced so that the activated environment persists.
# Usage: source start.sh

# Check if the script is being sourced.
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  echo "Please source this script (e.g., 'source start.sh') so that the environment remains activated."
  exit 1
fi

# Activate the virtual environment
if [ -f venv/bin/activate ]; then
  echo "Activating virtual environment..."
  source venv/bin/activate
else
  echo "Virtual environment not found. Please run setup.sh first."
  return 1
fi

echo ""
echo "Environment activated!"
echo ""

echo "Usage Instructions:"
echo "--------------------"
echo "1. Make sure you have created a project directory under './projects' containing your .txt files."
echo ""
echo "2. Choose one ingestion method:"
echo "   - Option A: Ingest entire documents (without chunking):"
echo "         python ingest.py <project_name>"
echo "   - Option B: Ingest documents using chunking (splits documents into overlapping chunks):"
echo "         python ingest_chunk.py <project_name>"
echo ""
echo "   Note: You should run only one of these ingestion methods for your project."
echo ""
echo "3. After ingestion, run inference with:"
echo "         python infer.py <project_name>"
echo ""
echo "Follow the above steps to prepare your data and then query your model."
