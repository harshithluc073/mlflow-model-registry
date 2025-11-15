# Project Structure

This document describes the organization and purpose of each directory in the MLflow Model Registry project.

## 📁 Directory Layout

```
mlflow-model-registry/
│
├── 📦 registry/                 # Core model registry logic
│   ├── core/                    # Model management & versioning
│   │   ├── model_manager.py     # Main model operations
│   │   ├── experiment_tracker.py # MLflow experiment handling
│   │   └── stage_manager.py     # Stage transition logic
│   ├── validation/              # Model validation
│   │   ├── validators.py        # Accuracy & metadata validators
│   │   └── promotion_rules.py   # Stage promotion rules
│   └── utils/                   # Helper utilities
│       ├── logging_utils.py     # Logging configuration
│       └── metadata_utils.py    # Metadata handling
│
├── 🌐 api/                      # FastAPI inference service
│   ├── routers/                 # API route definitions
│   │   ├── inference.py         # Prediction endpoints
│   │   ├── models.py            # Model metadata endpoints
│   │   └── health.py            # Health check endpoints
│   ├── schemas/                 # Pydantic models
│   │   ├── prediction.py        # Prediction request/response
│   │   └── model_info.py        # Model metadata schemas
│   ├── services/                # Business logic
│   │   └── model_service.py     # Model loading & serving
│   └── main.py                  # FastAPI application entry
│
├── 🖥️  cli/                      # Command-line interface
│   ├── commands/                # CLI command implementations
│   │   ├── register.py          # Model registration commands
│   │   ├── promote.py           # Stage promotion commands
│   │   ├── list.py              # Listing commands
│   │   └── compare.py           # Experiment comparison
│   └── main.py                  # Typer CLI entry point
│
├── 🔬 workflows/                # Training & examples
│   ├── examples/                # Example notebooks
│   │   └── end_to_end_demo.py   # Complete workflow demo
│   └── training/                # Training scripts
│       └── sample_model.py      # Sample model training
│
├── 🧪 tests/                    # Test suite
│   ├── unit/                    # Unit tests
│   │   ├── test_model_manager.py
│   │   ├── test_validators.py
│   │   └── test_api.py
│   ├── integration/             # Integration tests
│   │   └── test_workflow.py
│   └── fixtures/                # Test fixtures
│       └── sample_data.py
│
├── 🐳 docker/                   # Docker configurations
│   ├── mlflow/                  # MLflow server Docker
│   │   ├── Dockerfile
│   │   └── entrypoint.sh
│   ├── api/                     # API service Docker
│   │   ├── Dockerfile
│   │   └── entrypoint.sh
│   └── docker-compose.yml       # Multi-container setup
│
├── 📚 docs/                     # Documentation
│   ├── guides/                  # User guides
│   │   ├── installation.md
│   │   ├── quick_start.md
│   │   └── deployment.md
│   ├── diagrams/                # Architecture diagrams
│   └── api_reference.md         # API documentation
│
├── ⚙️  config/                   # Configuration files
│   ├── settings.py              # Application settings
│   └── __init__.py
│
├── 💾 data/                     # Data storage (gitignored)
│   ├── mlruns/                  # MLflow experiment runs
│   ├── mlartifacts/             # Model artifacts
│   └── models/                  # Exported models
│
├── 🔧 scripts/                  # Utility scripts
│   ├── start_mlflow.sh          # Start MLflow server
│   ├── init_db.py               # Initialize database
│   └── cleanup.sh               # Cleanup utilities
│
├── 🤖 .github/                  # GitHub Actions CI/CD
│   └── workflows/
│       ├── test.yml             # Testing workflow
│       ├── validate.yml         # Model validation
│       └── deploy.yml           # Deployment workflow
│
├── 📄 Configuration Files
│   ├── .gitignore               # Git ignore rules
│   ├── .gitattributes           # Git LFS configuration
│   ├── requirements.txt         # Python dependencies
│   ├── requirements-dev.txt     # Development dependencies
│   ├── setup.py                 # Package setup
│   ├── pytest.ini               # Pytest configuration
│   └── .env.example             # Environment variables template
│
└── 📖 Documentation
    ├── README.md                # Project overview
    ├── LICENSE                  # MIT License
    ├── STRUCTURE.md             # This file
    └── CONTRIBUTING.md          # Contribution guidelines
```

## 🎯 Module Purposes

### Registry Module
- **Purpose**: Core model lifecycle management
- **Key Features**: Version control, stage transitions, metadata validation
- **Entry Point**: `registry.core.ModelManager`

### API Module
- **Purpose**: Production model serving
- **Key Features**: REST endpoints, batch predictions, health checks
- **Entry Point**: `api.main:app`

### CLI Module
- **Purpose**: Terminal-based management
- **Key Features**: Model registration, promotion, comparison
- **Entry Point**: `cli.main:app`

### Workflows Module
- **Purpose**: Training examples and demonstrations
- **Key Features**: End-to-end examples, sample models
- **Entry Point**: `workflows.training.sample_model`

## 🔄 Data Flow

```
Training Script
      ↓
MLflow Tracking Server (data/mlruns)
      ↓
Model Registry (registry module)
      ↓
Validation (registry/validation)
      ↓
Stage Promotion (Development → Staging → Production)
      ↓
FastAPI Service (api module)
      ↓
Model Serving
```

## 🚀 Quick Navigation

- **Start MLflow Server**: `scripts/start_mlflow.sh`
- **Train Sample Model**: `workflows/training/sample_model.py`
- **Run API**: `api/main.py`
- **Use CLI**: `cli/main.py`
- **Run Tests**: `pytest tests/`

## 📝 Notes

- All Python packages have `__init__.py` files
- Configuration is centralized in `config/settings.py`
- Environment variables override default settings
- Data directories are gitignored but structure is preserved with `.gitkeep`