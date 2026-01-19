import sqlite3
from pathlib import Path

DB_DIR = Path("db")
DB_DIR.mkdir(exist_ok=True)

DB_PATH = DB_DIR / "ml_platform.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # DATASETS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        version TEXT NOT NULL,
        hash TEXT,
        created_at TEXT NOT NULL
    );
    """)

    # EXPERIMENTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS experiments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        experiment_name TEXT NOT NULL,
        dataset_version TEXT NOT NULL,
        model_type TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)

    # METRICS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metrics (
        experiment_id INTEGER PRIMARY KEY,
        accuracy REAL,
        precision REAL,
        recall REAL,
        f1 REAL,
        roc_auc REAL,
        training_time REAL,
        FOREIGN KEY (experiment_id) REFERENCES experiments(id)
    );
    """)

    # MODELS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS models (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name TEXT NOT NULL,
        version TEXT NOT NULL,
        experiment_id INTEGER NOT NULL,
        stage TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (experiment_id) REFERENCES experiments(id)
    );
    """)

    conn.commit()
    conn.close()

    print("✅ Database initialized successfully.")

if __name__ == "__main__":
    init_db()
