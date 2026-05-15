import os
import sqlite3
from dotenv import load_dotenv

DATABASE = os.environ.get("DATABASE_NAME")

if not DATABASE:
    raise RuntimeError("DATABASE_NAME environment variable must be set")

def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

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

    connection.commit()
    connection.close()

if __name__ == "__main__":
    init_db()