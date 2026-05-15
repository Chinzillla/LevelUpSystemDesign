import sqlite3
import os
from pathlib import Path

DATABASE = Path(os.environ.get("DATABASE", Path(__file__).with_name("app.db")))


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()

    connection.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        message TEXT NOT NULL
    )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    init_db()