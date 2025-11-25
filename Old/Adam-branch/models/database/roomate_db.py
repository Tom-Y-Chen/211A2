# models/database/roommate_db.py
from models.database.db_connection import get_connection
import random

# -----------------------------
# Roommate CRUD
# -----------------------------

def add_roommate(name, email=""):
    """Insert a new roommate"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO roommates (name, email) VALUES (?, ?)",
        (name, email)
    )
    conn.commit()
    conn.close()


def get_all_roommates():
    """Retrieve all roommates"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM roommates")
    results = cur.fetchall()
    conn.close()
    return results


def get_roommate_by_id(roommate_id):
    """Retrieve one roommate by ID"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, email FROM roommates WHERE id = ?",
        (roommate_id,)
    )
    result = cur.fetchone()
    conn.close()
    return result


def update_roommate(roommate_id, name=None, email=None):
    """Update a roommate's information"""
    conn = get_connection()
    cur = conn.cursor()

    fields = []
    values = []

    if name is not None:
        fields.append("name = ?")
        values.append(name)

    if email is not None:
        fields.append("email = ?")
        values.append(email)

    if not fields:
        conn.close()
        return  # nothing to update

    sql = f"UPDATE roommates SET {', '.join(fields)} WHERE id = ?"
    values.append(roommate_id)

    cur.execute(sql, tuple(values))
    conn.commit()
    conn.close()


def delete_roommate(roommate_id):
    """Delete a roommate by ID"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM roommates WHERE id = ?", (roommate_id,))
    conn.commit()
    conn.close()


# -----------------------------
# Assign random payer
# -----------------------------

def assign_random_payer(expense_ids):
    """Assign a random roommate to each expense (payer_id)"""
    roommates = get_all_roommates()
    if not roommates:
        raise ValueError("No roommates in database to assign.")

    conn = get_connection()
    cur = conn.cursor()

    for expense_id in expense_ids:
        random_roommate_id = random.choice(roommates)[0]
        cur.execute(
            "UPDATE expenses SET payer_id = ? WHERE id = ?",
            (random_roommate_id, expense_id)
        )

    conn.commit()
    conn.close()
