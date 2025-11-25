import sqlite3
from pathlib import Path

DB_PATH = Path("assets/data/roomiesplit.db")

def get_connection():
    """
    Returns a SQLite connection with foreign keys enabled.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")  # Enforce FK constraints
    return conn

def initialize_database():
    """Create tables if they do not exist."""
    conn = get_connection()
    cur = conn.cursor()

    # Enable WAL mode (optional but improves read/write performance)
    cur.execute("PRAGMA journal_mode=WAL;")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS roommates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            account TEXT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            note TEXT,
            payer_id INTEGER,
            FOREIGN KEY (payer_id) REFERENCES roommates(id) ON DELETE SET NULL
        );
    """)

    conn.commit()
    conn.close()
