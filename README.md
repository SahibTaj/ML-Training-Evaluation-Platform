# ML Training & Evaluation Platform (Mini ML Infra)

## Overview
This project is a lightweight, end-to-end machine learning experimentation platform inspired by production MLOps systems such as MLflow.

Unlike typical ML projects that focus only on training models, this platform focuses on **ML system design, experiment governance, and model lifecycle control**.

The system is built as a mini ML infrastructure layer rather than a notebook-based workflow.

---

## What This Platform Does
- Registers datasets with explicit versioning
- Tracks experiments and their lifecycle states (CREATED, RUNNING, COMPLETED, FAILED)
- Persists experiment metrics in a relational database
- Registers models with explicit lifecycle stages (staging, production, archived)
- Performs automated regression detection before allowing model promotion
- Uses config-driven orchestration for reproducibility

---

## Architecture Overview
- **SQLite** is used as the single source of truth for metadata
- Training logic is fully decoupled from tracking and registry logic
- All experiments, metrics, datasets, and models are DB-backed
- File system is treated as non-authoritative (no JSON-based tracking)

Key architectural principle:
> The database, not the filesystem, defines the state of the ML system.

---

## Core Components
- `tracking/`  
  Core platform logic for dataset registry, experiment tracking, model registry, and regression detection

- `run_experiment.py`  
  Single orchestrator entry point for running experiments

- `train.py`  
  Model training engine (stateless, DB-agnostic)

- `db/`  
  Database initialization and metadata storage

- `configs/`  
  YAML-based experiment definitions for reproducibility

---

## Experiment Lifecycle
1. Dataset is registered in the platform
2. Experiment is created via the orchestrator
3. Training runs and metrics are logged
4. Regression detection compares against the current production model
5. Model is registered and staged only if regression checks pass

This enforces safety against silent performance degradation.

---
## Dataset
Credit Card Fraud Detection dataset (highly imbalanced classification).

Due to GitHub size limits, the dataset is not included in the repository.

Expected local path:

## How to Run — ML Training & Evaluation Platform

### Prerequisites
- Python 3.9+
- pip
- Dataset downloaded locally (see Dataset section)

---

### 1. Clone the Repository
```bash
git clone https://github.com/SahibTaj/ML-Training-Evaluation-Platform.git
cd ML-Training-Evaluation-Platform
````

---

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
```

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Setup Dataset (Required)

This repository does **not** include datasets by design.

Steps:

1. Download the *Credit Card Fraud Detection* dataset from Kaggle
2. Create the following directory structure:

```text
data/
└── versions/
    └── v1/
        └── creditcard.csv
```

Expected dataset path:

```text
data/versions/v1/creditcard.csv
```

---

### 5. Initialize the Platform Database (One-Time)

```bash
python db/init_db.py
```

This creates:

```text
db/ml_platform.db
```

---

### 6. Register Dataset in the Platform (One-Time)

```bash
python tests/test_dataset_registry.py
```

This step:

* Registers `credit_card_fraud:v1` in the database
* Enables dataset validation for experiments

---

### 7. Run an Experiment (MAIN ENTRY POINT)

⚠️ **Do NOT run `train.py` directly**

Use the orchestrator:

```bash
python run_experiment.py --config configs/fraud_baseline.yaml
```

Internal flow:

* Dataset is validated
* Experiment is created
* Training runs
* Metrics are logged
* Regression detection is applied
* Model registration is gated

---

### 8. View Experiment Results (Optional)

```bash
python
```

```python
from tracking.db import fetch_all

fetch_all("SELECT * FROM experiments;")
fetch_all("SELECT * FROM metrics;")
fetch_all("SELECT * FROM models;")
```

---

### 9. Launch Dashboard (Optional)

```bash
streamlit run dashboard.py
```

This shows:

* Experiment comparisons
* Metric summaries
* System state

---

### What NOT to Do

* ❌ Do NOT commit datasets
* ❌ Do NOT run `train.py` directly
* ❌ Do NOT edit the database manually
* ❌ Do NOT use legacy JSON-based experiment folders

---

### Minimal Run Checklist (Quick Start)

```bash
pip install -r requirements.txt
python db/init_db.py
python tests/test_dataset_registry.py
python run_experiment.py --config configs/fraud_baseline.yaml
```


