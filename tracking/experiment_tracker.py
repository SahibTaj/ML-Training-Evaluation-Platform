from datetime import datetime
from tracking.db import execute, fetch_one


def create_experiment(
    experiment_name: str,
    dataset_version: str,
    model_type: str
) -> int:
    created_at = datetime.utcnow().isoformat()

    execute(
        """
        INSERT INTO experiments (experiment_name, dataset_version, model_type, status, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (experiment_name, dataset_version, model_type, "CREATED", created_at)
    )

    row = fetch_one(
        """
        SELECT id FROM experiments
        WHERE experiment_name = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (experiment_name,)
    )

    return row[0]


def update_experiment_status(experiment_id: int, status: str):
    """
    Update experiment status.
    """
    execute(
        """
        UPDATE experiments
        SET status = ?
        WHERE id = ?
        """,
        (status, experiment_id)
    )


def log_metrics(
    experiment_id: int,
    accuracy: float,
    precision: float,
    recall: float,
    f1: float,
    roc_auc: float,
    training_time: float
):
    """
    Store metrics for a completed experiment.
    """
    execute(
        """
        INSERT INTO metrics (
            experiment_id, accuracy, precision, recall, f1, roc_auc, training_time
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            experiment_id,
            accuracy,
            precision,
            recall,
            f1,
            roc_auc,
            training_time
        )
    )
