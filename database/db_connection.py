# models/database/db_connection.py
import sqlite3
from pathlib import Path

DB_PATH = Path("assets/data/roomiesplit.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_database():
    """Create tables if they do not exist"""
    conn = get_connection()
    cur = conn.cursor()

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
            FOREIGN KEY (payer_id) REFERENCES roommates(id)
        );
    """)

    conn.commit()
    conn.close()
