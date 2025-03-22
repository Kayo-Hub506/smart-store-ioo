# smart-store-ioo

Starter files to initialize the smart sales project.

Project Setup Guide (1-Mac/Linux)

Run all commands from a terminal in the root project folder.

Step 1A - Create a Local Project Virtual Environment

python3 -m venv .venv
Step 1B - Activate the Virtual Environment

source .venv/bin/activate
Step 1C - Install Packages

python3 -m pip install --upgrade -r requirements.txt
Step 1D - Optional: Verify .venv Setup

python3 -m datafun_venv_checker.venv_checker
Step 1E - Run the initial project script

python3 scripts/data_prep.py
