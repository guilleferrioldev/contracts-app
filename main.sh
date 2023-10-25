# !/bin/sh
#
# This script will be executed *after* all the other init scripts.
# You can put your own initialization stuff in here if you don't
# want to do the full Sys V style init stuff.

# Run the demo script on every boot:

# Activate the virtual environment
source ./bin/activate

# Change directory to app
cd app

# Run the application
python app.py
