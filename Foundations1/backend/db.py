import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()
DATABASE = os.environ.get("DATABASE_NAME")

if not DATABASE:
    raise RuntimeError("DATABASE_NAME environment variable must be set")

def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

def column_exists(connection, table_name, column_name):
    columns = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    return any(column["name"] == column_name for column in columns)

def migrate_items_table(connection):
    if not column_exists(connection, "items", "name"):
        connection.execute(
            "ALTER TABLE items ADD COLUMN name TEXT NOT NULL DEFAULT ''"
        )

    if not column_exists(connection, "items", "completed"):
        connection.execute(
            "ALTER TABLE items ADD COLUMN completed INTEGER NOT NULL DEFAULT 0"
        )

def init_db():
    connection = get_connection()

    connection.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)

    connection.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_token TEXT NOT NULL UNIQUE,
        user_id INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    connection.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        completed INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    migrate_items_table(connection)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    init_db()
