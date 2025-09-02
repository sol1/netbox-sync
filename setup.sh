#!/bin/bash
set -e

# Prerequsite package for pip install
sudo apt install python3-venv

# Set venv directory
VENV_DIR="./venv"

# Check if venv already exists
if [[ -d "$VENV_DIR" ]]; then
  echo "Virtual environment already exists at $VENV_DIR"
else
  echo "Creating virtual environment in $VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
echo "Upgrading pip"
python3 -m pip install --upgrade pip
echo "Installing wheel"
python3 -m pip install wheel 
echo "Installing python libaries"
python3 -m pip install -r requirements.txt

# ensure session.sh exists by copying from example if missing
if [ ! -f "session.sh" ]; then
    cp "session.sh.example" "session.sh"
    chmod +x "session.sh"
    echo " "
    echo "New session.sh created from session.sh.example"
fi