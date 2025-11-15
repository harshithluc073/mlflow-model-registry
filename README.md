# 🚀 MLflow Model Registry

> A production-ready, self-contained MLflow model registry with automated CI/CD, FastAPI inference service, and CLI management tools.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![MLflow](https://img.shields.io/badge/MLflow-2.9+-orange.svg)](https://mlflow.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.108+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Overview

This project implements a **centralized, file-based model registry** using MLflow, fully contained within a single repository. It provides:

- ✅ **Model Versioning & Tracking** - Complete lifecycle management from development to production
- ✅ **Automated Validation** - Accuracy thresholds, required tags, and metadata checks
- ✅ **FastAPI Inference Service** - Production-ready model serving endpoints
- ✅ **CLI Management** - Terminal-based model lifecycle operations
- ✅ **CI/CD Pipeline** - Automated testing, validation, and deployment
- ✅ **Docker Support** - One-command reproducibility
- ✅ **Database Flexibility** - Start file-based, scale to SQLite/PostgreSQL

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Model Training                           │
│  (Experiments, Hyperparameters, Metrics)                   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              MLflow Tracking Server                         │
│  • File-based artifact storage                              │
│  • SQLite/PostgreSQL backend (optional)                     │
│  • Version history & metadata                               │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│          Automated Validation (CI/CD)                       │
│  • Accuracy threshold checks                                │
│  • Required metadata validation                             │
│  • Stage promotion rules                                    │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│         Stage-Based Deployment                              │
│  Development → Staging → Production                         │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│     FastAPI Inference Service (Docker)                      │
│  • Version-specific serving                                 │
│  • Batch predictions                                        │
│  • Auto-deployment on promotion                             │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

**Coming soon...**

## 📦 Project Structure

```
mlflow-model-registry/
├── registry/           # Core model registry logic
├── api/               # FastAPI inference service
├── cli/               # Typer CLI interface
├── workflows/         # Training examples & demos
├── tests/             # Unit & integration tests
├── docker/            # Dockerfiles & compose configs
├── .github/           # CI/CD workflows
└── docs/              # Documentation & diagrams
```

## 🛠️ Features

### Model Registry
- **Version Control**: Track every model iteration with complete metadata
- **Stage Management**: Development → Staging → Production transitions
- **Metadata Validation**: Enforce accuracy thresholds and required tags
- **Audit Trail**: Full history of model changes and promotions

### CLI Interface
- Register models with metadata
- Promote models between stages
- Compare experiment results
- View model histories and audit logs

### FastAPI Service
- Load models by version or stage
- Batch and single predictions
- Health checks and metrics
- Auto-scaling ready

### CI/CD Pipeline
- Automated testing on PR
- Model validation checks
- Docker image building
- Container registry publishing

## 📊 Technology Stack

- **Registry**: MLflow 2.9+
- **API**: FastAPI 0.108+
- **CLI**: Typer 0.9+
- **Database**: SQLite (default), PostgreSQL (optional)
- **Container**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Python**: 3.9+

## 📖 Documentation

- [Installation Guide](docs/installation.md) *(Coming soon)*
- [Usage Examples](docs/examples.md) *(Coming soon)*
- [API Reference](docs/api.md) *(Coming soon)*
- [CLI Commands](docs/cli.md) *(Coming soon)*
- [Architecture Guide](docs/architecture.md) *(Coming soon)*

## 🤝 Contributing

Contributions welcome! This project demonstrates production MLOps practices and is designed for learning and real-world use.

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with [MLflow](https://mlflow.org/), [FastAPI](https://fastapi.tiangolo.com/), and [Typer](https://typer.tiangolo.com/).

---

**Status**: 🚧 Under Active Development

**Author**: Harshith  
**Repository**: [github.com/harshithluc073/mlflow-model-registry](https://github.com/harshithluc073/mlflow-model-registry)