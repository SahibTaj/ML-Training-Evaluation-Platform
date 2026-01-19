from datetime import datetime
from tracking.db import execute, fetch_one, fetch_all


def register_model(
    model_name: str,
    experiment_id: int,
    stage: str = "staging"
) -> int:
    """
    Register a new model version linked to an experiment.
    Version is auto-incremented per model name.
    """

    # Get latest version for this model
    row = fetch_one(
        """
        SELECT version FROM models
        WHERE model_name = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (model_name,)
    )

    if row is None:
        version = "v1"
    else:
        last_version_num = int(row[0].replace("v", ""))
        version = f"v{last_version_num + 1}"

    created_at = datetime.utcnow().isoformat()

    execute(
        """
        INSERT INTO models (model_name, version, experiment_id, stage, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (model_name, version, experiment_id, stage, created_at)
    )

    model_row = fetch_one(
        """
        SELECT id FROM models
        WHERE model_name = ? AND version = ?
        """,
        (model_name, version)
    )

    return model_row[0]


def promote_model(model_id: int, new_stage: str):
    """
    Promote or demote a model (e.g., staging → production).
    """

    if new_stage not in {"staging", "production", "archived"}:
        raise ValueError("Invalid model stage")

    execute(
        """
        UPDATE models
        SET stage = ?
        WHERE id = ?
        """,
        (new_stage, model_id)
    )


def get_active_model(model_name: str):
    """
    Fetch the production model for a given model name.
    """

    return fetch_one(
        """
        SELECT * FROM models
        WHERE model_name = ? AND stage = 'production'
        ORDER BY id DESC
        LIMIT 1
        """,
        (model_name,)
    )


def list_models(model_name: str):
    """
    List all versions of a model.
    """

    return fetch_all(
        """
        SELECT * FROM models
        WHERE model_name = ?
        ORDER BY id ASC
        """,
        (model_name,)
    )
