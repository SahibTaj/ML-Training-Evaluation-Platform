from tracking.db import fetch_one
from typing import Tuple, List

TOLERANCE = 1e-4


def get_production_metrics(model_name: str):
    """
    Fetch metrics of the production model.
    """
    row = fetch_one(
        """
        SELECT m.experiment_id
        FROM models m
        WHERE m.model_name = ? AND m.stage = 'production'
        ORDER BY m.id DESC
        LIMIT 1
        """,
        (model_name,)
    )

    if row is None:
        return None

    experiment_id = row[0]

    return fetch_one(
        """
        SELECT accuracy, precision, recall, f1, roc_auc
        FROM metrics
        WHERE experiment_id = ?
        """,
        (experiment_id,)
    )


def get_experiment_metrics(experiment_id: int):
    return fetch_one(
        """
        SELECT accuracy, precision, recall, f1, roc_auc
        FROM metrics
        WHERE experiment_id = ?
        """,
        (experiment_id,)
    )


def check_regression(
    model_name: str,
    candidate_experiment_id: int
) -> Tuple[bool, List[str]]:
    """
    Returns (passed, reasons)
    """

    baseline = get_production_metrics(model_name)

    # No production model yet → allow
    if baseline is None:
        return True, ["No production model exists"]

    candidate = get_experiment_metrics(candidate_experiment_id)

    reasons = []

    # Index mapping:
    # 0: accuracy, 1: precision, 2: recall, 3: f1, 4: roc_auc

    if candidate[2] < baseline[2] - TOLERANCE:
        reasons.append("Recall regression")

    if candidate[4] < baseline[4] - TOLERANCE:
        reasons.append("ROC-AUC regression")

    if reasons:
        return False, reasons

    return True, ["Passed regression checks"]
