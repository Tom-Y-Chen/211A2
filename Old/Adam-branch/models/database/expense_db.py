# models/database/expense_db.py
from models.database.db_connection import get_connection
import pandas as pd
import os

# -----------------------------
# Expense CRUD Operations
# -----------------------------

def add_expense(date, account, category, amount, note="", payer_id=None):
    """Insert a new expense record into the database"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO expenses (date, account, category, amount, note, payer_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, account, category, amount, note, payer_id))
    conn.commit()
    conn.close()


def get_all_expenses():
    """Retrieve all expenses ordered by newest first"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, date, account, category, amount, note, payer_id
        FROM expenses
        ORDER BY date DESC
    """)
    data = cur.fetchall()
    conn.close()
    return data


def get_expense_by_id(expense_id):
    """Retrieve a single expense"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, date, account, category, amount, note, payer_id
        FROM expenses
        WHERE id = ?
    """, (expense_id,))
    result = cur.fetchone()
    conn.close()
    return result


def get_expense_by_category(category):
    """Retrieve expenses by category"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, date, account, category, amount, note, payer_id
        FROM expenses
        WHERE category = ?
    """, (category,))
    results = cur.fetchall()
    conn.close()
    return results


def get_expenses_by_roommate(roommate_id):
    """Retrieve expenses assigned to a specific roommate"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, date, account, category, amount, note, payer_id
        FROM expenses
        WHERE payer_id = ?
    """, (roommate_id,))
    results = cur.fetchall()
    conn.close()
    return results


def update_expense(expense_id, date=None, account=None, category=None,
                   amount=None, note=None, payer_id=None):
    """Update an existing expense record with only provided fields"""
    conn = get_connection()
    cur = conn.cursor()

    fields = []
    values = []

    if date is not None:
        fields.append("date = ?")
        values.append(date)
    if account is not None:
        fields.append("account = ?")
        values.append(account)
    if category is not None:
        fields.append("category = ?")
        values.append(category)
    if amount is not None:
        fields.append("amount = ?")
        values.append(amount)
    if note is not None:
        fields.append("note = ?")
        values.append(note)
    if payer_id is not None:
        fields.append("payer_id = ?")
        values.append(payer_id)

    # Nothing to update
    if not fields:
        conn.close()
        return

    sql = f"UPDATE expenses SET {', '.join(fields)} WHERE id = ?"
    values.append(expense_id)

    cur.execute(sql, tuple(values))
    conn.commit()
    conn.close()


def delete_expense(expense_id):
    """Delete an expense"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()


# -----------------------------
# CSV Loader
# -----------------------------

def load_dataset(path="assets/data/dataset.csv"):
    """Load dataset CSV into the database"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset file not found at {path}")

    df = pd.read_csv(path).fillna("")

    # Normalize column names
    df = df.rename(columns={
        "INR": "Amount",
        "amount": "Amount",
        "Category": "Category",
        "category": "Category",
        "Account": "Account",
        "Note": "Note",
        "Date": "Date"
    })

    for _, row in df.iterrows():
        add_expense(
            date=str(row["Date"]),
            account=str(row.get("Account", "")),
            category=str(row.get("Category", "")),
            amount=float(row["Amount"]) if row["Amount"] != "" else 0.0,
            note=str(row.get("Note", "")),
            payer_id=None
        )

    print(f"Loaded {len(df)} expenses.")
