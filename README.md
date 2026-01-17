# ML Training & Evaluation Platform (Mini-ML Infra)

## Overview
This project is a lightweight machine learning experimentation platform inspired by MLflow and Weights & Biases.

It enables:
- Dataset versioning
- Experiment tracking
- Metric logging
- Experiment comparison
- Model registry
- Regression detection with tolerance handling

## Why This Project?
Most ML projects focus only on model accuracy.  
This project focuses on **ML systems, reproducibility, and decision-making**, which are critical in real-world ML deployments.

## Features
- Version-controlled datasets
- Config-driven experiments
- Persistent metric tracking
- Automated experiment comparison
- Model registry with metadata
- Regression detection with numeric tolerance
- Interactive Streamlit dashboard

## Dataset
Credit Card Fraud Detection dataset (highly imbalanced, real-world).

## How to Run
```bash
pip install -r requirements.txt
python train.py
python regression_check.py
streamlit run dashboard.py
