import streamlit as st
import pandas as pd
from tracking.db import fetch_all

st.title("ML Experiment Comparison Dashboard")

# Fetch experiment + metric data from DB
rows = fetch_all("""
SELECT 
    e.id,
    e.experiment_name,
    e.dataset_version,
    e.status,
    m.accuracy,
    m.precision,
    m.recall,
    m.f1,
    m.roc_auc,
    m.training_time
FROM experiments e
JOIN metrics m ON e.id = m.experiment_id
WHERE e.status = 'COMPLETED'
ORDER BY e.id ASC
""")

if not rows:
    st.warning("No completed experiments found.")
else:
    df = pd.DataFrame(rows, columns=[
        "experiment_id",
        "experiment_name",
        "dataset_version",
        "status",
        "accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
        "training_time"
    ])

    st.subheader("📋 Experiment Metrics")
    st.dataframe(df)

    st.subheader("🏆 Best Experiment (Highest Recall)")
    best_exp = df.sort_values("recall", ascending=False).iloc[0]
    st.json(best_exp.to_dict())