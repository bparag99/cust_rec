#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt
pip install -U flask-cors
pip install pandas
pip install pgvector
