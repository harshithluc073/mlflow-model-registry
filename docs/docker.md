# Docker Deployment Guide

## Quick Start

### Using Docker Compose (Recommended)
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Access Services

- MLflow UI: http://localhost:5000
- API Docs: http://localhost:8000/docs
- API Health: http://localhost:8000/health/health

## Building Images

### Build all images
```bash
bash scripts/docker_build.sh
```

### Build individual images
```bash
# MLflow server
docker build -f docker/mlflow/Dockerfile -t mlflow-server:latest .

# API service
docker build -f docker/api/Dockerfile -t mlflow-api:latest .
```

## Running Containers

### Run MLflow server
```bash
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  --name mlflow-server \
  mlflow-server:latest
```

### Run API service
```bash
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -e MLFLOW_TRACKING_URI=http://mlflow-server:5000 \
  --link mlflow-server \
  --name mlflow-api \
  mlflow-api:latest
```

## Production Deployment

### Using Docker Swarm
```bash
docker stack deploy -c docker-compose.yml mlflow-stack
```

### Using Kubernetes

See `kubernetes/` directory for manifests.

## Troubleshooting

### View container logs
```bash
docker-compose logs mlflow
docker-compose logs api
```

### Restart services
```bash
docker-compose restart
```

### Remove all containers and volumes
```bash
docker-compose down -v
```