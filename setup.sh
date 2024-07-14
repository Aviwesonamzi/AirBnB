#!/bin/bash
# Setup script for AirBnB_clone_v2 project

# Install necessary packages
sudo apt-get update
sudo apt-get install -y python3 python3-pip

# Install pycodestyle
pip3 install pycodestyle==2.8.*

# Ensure all Python files are executable
chmod +x *.py
chmod +x tests/*.py
