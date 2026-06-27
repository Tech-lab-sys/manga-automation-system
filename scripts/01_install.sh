#!/bin/bash
echo "Running installation script..."
python3 scripts/01_install.py
echo "Installing requirements..."
pip install -r requirements.txt
echo "Done!"
