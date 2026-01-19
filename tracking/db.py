import sqlite3
from pathlib import Path

DB_PATH = Path("db") / "ml_platform.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def execute(query: str, params: tuple = ()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()


def fetch_one(query: str, params: tuple = ()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()
    return row


def fetch_all(query: str, params: tuple = ()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows
