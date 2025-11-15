# FastAPI Inference Service - Usage Guide

## Overview

The FastAPI inference service provides REST endpoints for serving ML models from the MLflow registry.

## Starting the API

### Option 1: Python Script
```bash
python scripts/start_api.py
```

### Option 2: Windows Batch File
```bash
scripts\start_api.bat
```

### Option 3: Direct Uvicorn
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

## Endpoints

### Health Check
```bash
GET /health/health
GET /health/ready
GET /health/live
```

### List Models
```bash
GET /models/
```

### Get Model Info
```bash
GET /models/{model_name}
GET /models/{model_name}/version/{version}
```

### Make Predictions

#### Single Prediction
```bash
POST /predict/{model_name}
Content-Type: application/json

{
  "instances": [[1.0, 2.0, 3.0, 4.0]]
}
```

#### Prediction with Specific Version
```bash
POST /predict/{model_name}/version/{version}
Content-Type: application/json

{
  "instances": [[1.0, 2.0, 3.0, 4.0]]
}
```

#### Prediction from Specific Stage
```bash
POST /predict/{model_name}/stage/{stage}
Content-Type: application/json

{
  "instances": [[1.0, 2.0, 3.0, 4.0]]
}
```

#### Batch Prediction with Probabilities
```bash
POST /predict/{model_name}/batch
Content-Type: application/json

{
  "instances": [
    [1.0, 2.0, 3.0, 4.0],
    [5.0, 6.0, 7.0, 8.0]
  ],
  "return_probabilities": true
}
```

## Example Usage

### Using cURL

```bash
# Health check
curl http://localhost:8000/health/health

# List models
curl http://localhost:8000/models/

# Make prediction
curl -X POST http://localhost:8000/predict/sample_classifier \
  -H "Content-Type: application/json" \
  -d '{"instances": [[1.0, 2.0, 3.0, 4.0]]}'
```

### Using Python Requests

```python
import requests

# API base URL
API_URL = "http://localhost:8000"

# Health check
response = requests.get(f"{API_URL}/health/health")
print(response.json())

# List models
response = requests.get(f"{API_URL}/models/")
print(response.json())

# Make prediction
data = {
    "instances": [[1.0, 2.0, 3.0, 4.0]]
}
response = requests.post(
    f"{API_URL}/predict/sample_classifier",
    json=data
)
print(response.json())
```

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Response Formats

### Success Response
```json
{
  "predictions": [1],
  "model_name": "sample_classifier",
  "model_version": "1",
  "model_stage": "Production"
}
```

### Error Response
```json
{
  "error": "ModelNotFound",
  "detail": "Model 'invalid_model' not found",
  "timestamp": "2025-11-15T12:00:00"
}
```

## Configuration

API settings can be configured in `.env`:

```bash
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true
```

## Production Deployment

For production deployment, disable reload and use multiple workers:

```bash
uvicorn api.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --no-reload
```

## Monitoring

Monitor API health using the health check endpoints:

- **Liveness**: `/health/live` - Basic service availability
- **Readiness**: `/health/ready` - MLflow connection check
- **Health**: `/health/health` - Comprehensive status