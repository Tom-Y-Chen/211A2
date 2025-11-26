# models/database/db_connection.py
import sqlite3
from pathlib import Path

# Database file path configuration
DB_PATH = Path("assets/data/roomiesplit.db")


def get_connection() -> sqlite3.Connection:
    """
    Establishes and returns a SQLite database connection with foreign key constraints enabled.
    
    Foreign key constraints ensure referential integrity between related tables
    (e.g., expenses.payer_id must reference a valid roommates.id).
    
    Returns:
        sqlite3.Connection: A SQLite database connection with foreign keys enabled
    """
    conn = sqlite3.connect(DB_PATH)
    # Enable foreign key constraints to maintain data integrity
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def initialize_database():
    """
    Initializes the database by creating all required tables if they don't exist.
    
    This function sets up the complete database schema including:
    - Roommates table for storing roommate information
    - Expenses table for tracking individual expenses
    - Expense participants table for many-to-many relationship between expenses and roommates
    
    The schema includes proper foreign key constraints and indexing for data integrity
    and performance.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Enable Write-Ahead Logging for better concurrent read/write performance
    # WAL allows reads to occur while writes are in progress
    cur.execute("PRAGMA journal_mode=WAL;")

    # Create roommates table - stores basic roommate information
    cur.execute("""
        CREATE TABLE IF NOT EXISTS roommates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            join_date TEXT
        );
    """)

    # Create expenses table - tracks individual expense records
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            account TEXT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            note TEXT,
            payer_id INTEGER,
            -- Foreign key to roommates table with SET NULL on delete
            -- This preserves expense records even if the payer is deleted
            FOREIGN KEY (payer_id) REFERENCES roommates(id) ON DELETE SET NULL
        );
    """)

    # Create expense_participants table - many-to-many relationship table
    # Tracks which roommates participated in which expenses
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expense_participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_id INTEGER NOT NULL,
            roommate_id INTEGER NOT NULL,
            -- CASCADE delete: if expense is deleted, remove all its participant records
            FOREIGN KEY (expense_id) REFERENCES expenses(id) ON DELETE CASCADE,
            -- Standard foreign key: participant must be a valid roommate
            FOREIGN KEY (roommate_id) REFERENCES roommates(id),
            -- Ensure unique combinations to prevent duplicate participant entries
            UNIQUE(expense_id, roommate_id)
        );
    """)

    # Commit changes and close connection
    conn.commit()
    conn.close()