from models.database.db_connection import get_connection

# -----------------------------
# Expense CRUD Operations
# -----------------------------

def add_expense(date, account, category, amount, note=""):
    """Insert a new expense record into the database"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO expenses (date, account, category, amount, note)
        VALUES (?, ?, ?, ?, ?)
    """, (date, account, category, amount, note))
    conn.commit()
    conn.close()


def get_all_expenses():
    """Retrieve all expense records"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses")
    results = cur.fetchall()
    conn.close()
    return results


def get_expense_by_category(category):
    """Retrieve expenses filtered by category"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses WHERE category = ?", (category,))
    results = cur.fetchall()
    conn.close()
    return results


def update_expense(expense_id, date=None, account=None, category=None, amount=None, note=None):
    """Update an existing expense record"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Build dynamic update query
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
    
    values.append(expense_id)
    sql = f"UPDATE expenses SET {', '.join(fields)} WHERE id = ?"
    cur.execute(sql, tuple(values))
    conn.commit()
    conn.close()


def delete_expense(expense_id):
    """Delete an expense record"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()


# -----------------------------
# Load dataset CSV into database
# -----------------------------
import pandas as pd
import os

def load_dataset(path="assets/data/dataset.csv"):
    """Load CSV and insert all expenses into the database"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset file not found at {path}")

    df = pd.read_csv(path)

    # Standardize column names for our DB
    df = df.rename(columns={
        "INR": "Amount",
        "amount": "Amount",
        "Category": "Category",
        "category": "Category",
        "Account": "Account",
        "Note": "Note",
        "Date": "Date"
    })

    # Fill NaN with empty strings
    df = df.fillna("")

    for _, row in df.iterrows():
        add_expense(
            date=str(row["Date"]),
            account=str(row.get("Account", "")),
            category=str(row.get("Category", "")),
            amount=float(row["Amount"]) if row["Amount"] != "" else 0.0,
            note=str(row.get("Note", ""))
        )

    print(f"{len(df)} records loaded from {path}")
