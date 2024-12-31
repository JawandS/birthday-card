#!/bin/bash

# Create a virtual environment in the current directory
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install necessary packages (if any)
pip install openai reportlab PIL flask

echo "Virtual environment setup complete and activated."