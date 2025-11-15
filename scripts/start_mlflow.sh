#!/bin/bash

# Start MLflow Tracking Server

echo "========================================"
echo "Starting MLflow Tracking Server"
echo "========================================"

# Activate virtual environment
source venv/bin/activate

# Start MLflow server
python scripts/start_mlflow.py --host 127.0.0.1 --port 5000