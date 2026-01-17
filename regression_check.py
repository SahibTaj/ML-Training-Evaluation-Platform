import json
import os

TOLERANCE = 1e-4  

BASELINE_METADATA_PATH = os.path.join(
    "models",
    "registry",
    "fraud_detector",
    "v1",
    "metadata.json"
)

with open(BASELINE_METADATA_PATH, "r") as f:
    baseline = json.load(f)

baseline_metrics = baseline["metrics"]

EXPERIMENT_ID = "exp_002"

EXPERIMENT_METRICS_PATH = os.path.join(
    "experiments",
    EXPERIMENT_ID,
    "metrics.json"
)

with open(EXPERIMENT_METRICS_PATH, "r") as f:
    new_metrics = json.load(f)

regression_reasons = []

if new_metrics["recall"] < baseline_metrics["recall"] - TOLERANCE:
    regression_reasons.append("Recall dropped beyond tolerance")

if new_metrics["roc_auc"] < baseline_metrics["roc_auc"] - TOLERANCE:
    regression_reasons.append("ROC-AUC dropped beyond tolerance")

if regression_reasons:
    decision = "FAILED"
else:
    decision = "PASSED"

delta_auc = new_metrics["roc_auc"] - baseline_metrics["roc_auc"]
print(f"ROC-AUC delta: {delta_auc:.6f}")

print("Regression Check:", decision)

if regression_reasons:
    print("Reasons:")
    for reason in regression_reasons:
        print("-", reason)
