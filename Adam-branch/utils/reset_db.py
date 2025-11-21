# models/database/expense_db.py

import sqlite3
import pandas as pd

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.database.db_connection import get_connection, initialize_database


DB_FILE = "roomiesplit.db"  # replace with your actual DB filename if different

def reset_expenses_from_csv(csv_path="assets/data/dataset.csv"):
    """
    Clears the expenses table and reloads data from the CSV file.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Optional: drop table and recreate
    cursor.execute("DROP TABLE IF EXISTS expenses;")
    conn.commit()

    # Re-initialize DB (will recreate tables)
    initialize_database(path=csv_path)

    conn.close()
    print(f"Expenses table reset and reloaded from {csv_path}")
