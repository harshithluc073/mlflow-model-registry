# CI/CD Pipeline Documentation

## Overview

The project uses GitHub Actions for continuous integration and deployment.

## Workflows

### 1. Tests (`test.yml`)

**Triggers:** Push/PR to main or develop

**Steps:**
- Lint code (flake8, black)
- Run unit tests
- Generate coverage report
- Upload to Codecov

### 2. Model Validation (`model_validation.yml`)

**Triggers:** PR affecting models or registry code

**Steps:**
- Train sample model
- Validate metrics (accuracy threshold)
- Validate required tags
- Check model metadata

### 3. Deployment (`deploy.yml`)

**Triggers:** Push to main (API/Docker changes)

**Steps:**
- Build Docker images
- Push to GitHub Container Registry
- Tag with version/SHA
- Cache layers for faster builds

## Setting Up CI/CD

### 1. Enable GitHub Actions

Go to repository Settings → Actions → Enable

### 2. Configure Secrets

Settings → Secrets → Actions:

- `GITHUB_TOKEN` (auto-provided)
- Add any additional secrets

### 3. Configure Branch Protection

Settings → Branches → Add rule:

- Require status checks
- Require review before merging
- Require tests to pass

## Local Testing

### Run tests locally
```bash
pytest tests/ -v --cov
```

### Validate formatting
```bash
black --check .
flake8 .
```

### Test Docker build
```bash
docker-compose build
docker-compose up
```

## CD4ML - Continuous Deployment for ML

### Model Promotion Flow

1. Train model → Development
2. PR with validation checks
3. Merge → Auto-promote to Staging
4. Manual approval → Production
5. Auto-deploy API with new model

### Automated Checks

- ✅ Accuracy >= threshold
- ✅ Required tags present
- ✅ Model metadata complete
- ✅ Tests pass
- ✅ Code quality checks