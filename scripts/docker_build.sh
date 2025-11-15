#!/bin/bash

echo "Building Docker images..."

# Build MLflow image
docker build -f docker/mlflow/Dockerfile -t mlflow-server:latest .

# Build API image
docker build -f docker/api/Dockerfile -t mlflow-api:latest .

echo "Docker images built successfully!"