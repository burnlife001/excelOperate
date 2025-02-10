#!/bin/bash

echo "Creating Python virtual environment..."

python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Setup completed successfully!"
