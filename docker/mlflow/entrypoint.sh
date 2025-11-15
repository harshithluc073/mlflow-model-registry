#!/bin/bash
set -e

echo "Starting MLflow Tracking Server..."

# Initialize MLflow directories
mkdir -p /app/data/mlruns
mkdir -p /app/data/mlartifacts
mkdir -p /app/data/models

# Initialize database if needed
python scripts/init_mlflow.py

# Start MLflow server
exec mlflow server \
    --backend-store-uri "file:///app/data/mlruns" \
    --default-artifact-root "/app/data/mlartifacts" \
    --host 0.0.0.0 \
    --port 5000