from tracking.db import fetch_all

tables = fetch_all(
    "SELECT name FROM sqlite_master WHERE type='table';"
)

print(tables)
