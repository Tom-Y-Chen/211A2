from models.database.db_connection import get_connection
import random

# -----------------------------
# Roommate CRUD
# -----------------------------

def add_roommate(name, email=""):
    """Insert a new roommate"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO roommates (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()

def get_all_roommates():
    """Retrieve all roommates"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM roommates")
    results = cur.fetchall()
    conn.close()
    return results

def assign_random_payer(expense_ids):
    """Assign a random roommate to each expense"""
    roommates = get_all_roommates()
    if not roommates:
        raise ValueError("No roommates in database to assign.")
    
    conn = get_connection()
    cur = conn.cursor()
    for eid in expense_ids:
        roommate_id = random.choice(roommates)[0]  # get the id of a random roommate
        cur.execute("UPDATE expenses SET payer_id = ? WHERE id = ?", (roommate_id, eid))
    conn.commit()
    conn.close()
