FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose MLflow port
EXPOSE 5000

# Set environment variables
ENV MLFLOW_BACKEND_STORE_URI=/app/data/mlruns
ENV MLFLOW_ARTIFACT_ROOT=/app/data/mlartifacts

# Create data directories
RUN mkdir -p /app/data/mlruns /app/data/mlartifacts /app/data/models

# Run MLflow server
CMD ["mlflow", "server", \
     "--backend-store-uri", "file:///app/data/mlruns", \
     "--default-artifact-root", "/app/data/mlartifacts", \
     "--host", "0.0.0.0", \
     "--port", "5000"]