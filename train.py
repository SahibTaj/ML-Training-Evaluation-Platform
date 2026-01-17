import json
import os
import time
import joblib

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

EXPERIMENT_ID = "exp_001"
EXPERIMENT_PATH = os.path.join("experiments", EXPERIMENT_ID)

CONFIG_PATH = os.path.join(EXPERIMENT_PATH, "config.json")
STATUS_PATH = os.path.join(EXPERIMENT_PATH, "status.txt")
METRICS_PATH = os.path.join(EXPERIMENT_PATH, "metrics.json")

with open(CONFIG_PATH,"r") as f:
    config = json.load(f)

dataset_version = config["dataset_version"]
threshold = config["threshold"]

with open(STATUS_PATH, "w") as f:
    f.write("RUNNING")

DATASET_PATH = os.path.join(
    "data",
    "versions",
    dataset_version,
    "creditcard.csv"
)

df = pd.read_csv(DATASET_PATH)

X = df.drop("Class", axis=1)
y = df["Class"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

start_time = time.time()

model = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=3000, class_weight="balanced"))
])

model.fit(X_train, y_train)

MODEL_REGISTRY_PATH = os.path.join(
    "models",
    "registry",
    "fraud_detector",
    "v1"
)

os.makedirs(MODEL_REGISTRY_PATH, exist_ok=True)

joblib.dump(
    model,
    os.path.join(MODEL_REGISTRY_PATH, "model.pkl")
)

training_time = time.time() - start_time

y_prob = model.predict_proba(X_test)[:, 1]
y_pred = (y_prob >= threshold).astype(int)

metrics = {
    "accuracy": accuracy_score(y_test, y_pred),
    "precision": precision_score(y_test, y_pred),
    "recall": recall_score(y_test, y_pred),
    "f1": f1_score(y_test, y_pred),
    "roc_auc": roc_auc_score(y_test, y_prob),
    "training_time_seconds": round(training_time, 2)
}

with open(METRICS_PATH, "w") as f:
    json.dump(metrics, f, indent=4)

with open(STATUS_PATH, "w") as f:
    f.write("COMPLETED")
