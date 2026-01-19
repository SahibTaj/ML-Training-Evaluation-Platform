from datetime import datetime
from tracking.db import execute, fetch_one


def register_dataset(
    name: str,
    version: str,
    dataset_hash: str | None = None
) -> int:
    """
    Register a dataset version in the DB.
    Returns dataset_id.
    """
    created_at = datetime.utcnow().isoformat()

    execute(
        """
        INSERT INTO datasets (name, version, hash, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (name, version, dataset_hash, created_at)
    )

    row = fetch_one(
        """
        SELECT id FROM datasets
        WHERE name = ? AND version = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (name, version)
    )

    return row[0]


def get_dataset(name: str, version: str):
    """
    Fetch dataset metadata.
    """
    return fetch_one(
        """
        SELECT * FROM datasets
        WHERE name = ? AND version = ?
        """,
        (name, version)
    )
