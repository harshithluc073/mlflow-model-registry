#!/bin/bash
set -e

echo "Starting FastAPI Inference Service..."

# Wait for MLflow to be ready
echo "Waiting for MLflow server..."
until curl -f http://mlflow:5000/health > /dev/null 2>&1; do
    echo "MLflow not ready yet..."
    sleep 2
done

echo "MLflow is ready!"

# Start FastAPI
exec uvicorn api.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4