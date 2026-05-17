import importlib
import sqlite3
import sys


def test_init_db_migrates_older_items_table(tmp_path, monkeypatch):
    database = tmp_path / "old.db"
    connection = sqlite3.connect(database)
    connection.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)
    connection.execute("""
    CREATE TABLE sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_token TEXT NOT NULL UNIQUE,
        user_id INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    connection.execute("""
    CREATE TABLE items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    connection.commit()
    connection.close()

    monkeypatch.setenv("DATABASE_NAME", str(database))
    sys.modules.pop("db", None)

    db = importlib.import_module("db")
    db.init_db()

    connection = sqlite3.connect(database)
    columns = {
        row[1]: row[2]
        for row in connection.execute("PRAGMA table_info(items)").fetchall()
    }
    connection.close()

    assert columns["name"] == "TEXT"
    assert columns["completed"] == "INTEGER"
