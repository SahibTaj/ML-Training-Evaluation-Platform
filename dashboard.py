import os
import json
import pandas as pd
import streamlit as st

st.title("ML Experiment Comparison Dashboard")

EXPERIMENTS_DIR = "experiments"

experiment_data = []

for exp_id in os.listdir(EXPERIMENTS_DIR):
    exp_path = os.path.join(EXPERIMENTS_DIR, exp_id)

    metrics_path = os.path.join(exp_path, "metrics.json")
    config_path = os.path.join(exp_path, "config.json")

    if os.path.exists(metrics_path) and os.path.exists(config_path):
        with open(metrics_path) as f:
            metrics = json.load(f)

        with open(config_path) as f:
            config = json.load(f)

        if metrics:
            row = {
                "experiment_id": exp_id,
                "dataset_version": config["dataset_version"],
                "threshold": config["threshold"],
                **metrics
            }
            experiment_data.append(row)

df = pd.DataFrame(experiment_data)

if df.empty:
    st.warning("No completed experiments found.")
else:
    st.subheader("📋 Experiment Metrics")
    st.dataframe(df)

    st.subheader("🏆 Best Experiment (Highest Recall)")
    best_exp = df.sort_values("recall", ascending=False).iloc[0]
    st.json(best_exp.to_dict())