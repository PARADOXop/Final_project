#!/bin/bash
set -ex

ENV_NAME=".venv"

echo "SCRIPT STARTED"

echo "Creating virtual environment: $ENV_NAME"
python -m venv $ENV_NAME

echo "Activating virtual environment"
source $ENV_NAME/Scripts/activate

echo "Upgrading pip"
python -m pip install --upgrade pip

echo "Installing requirements"
python -m pip install -r requirements.txt

echo "Setup complete."