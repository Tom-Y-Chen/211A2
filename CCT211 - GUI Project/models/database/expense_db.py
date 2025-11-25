# models/database/expense_db.py
from models.database.db_connection import get_connection

# -----------------------------
# Expense CRUD Operations
# -----------------------------

def add_expense(date: str, account: str, category: str, amount: float, 
                note: str = "", payer_id: int = None) -> int:
    """
    Creates a new expense record in the database and returns the generated expense ID.
    
    This function handles the core expense creation and is typically followed by
    adding participants via add_expense_participants().
    
    Args:
        date (str): The date of the expense in 'YYYY-MM-DD' format
        account (str): The account or payment method used
        category (str): Expense category (e.g., 'Groceries', 'Rent', 'Utilities')
        amount (float): The expense amount
        note (str, optional): Additional notes about the expense. Defaults to empty string.
        payer_id (int, optional): ID of the roommate who paid. Defaults to None.
    
    Returns:
        int: The auto-generated ID of the newly created expense record
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Insert expense record
    cur.execute("""
        INSERT INTO expenses (date, account, category, amount, note, payer_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, account, category, amount, note, payer_id))
    
    # Get the auto-generated ID of the new expense
    expense_id = cur.lastrowid
    
    conn.commit()
    conn.close()
    return expense_id


def get_all_expenses() -> list:
    """
    Retrieves all expense records from the database, ordered by most recent first.
    
    Returns:
        list: List of expense tuples ordered by date descending.
              Each tuple: (id, date, account, category, amount, note, payer_id)
    """
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


def get_expense_by_id(expense_id: int) -> tuple:
    """
    Retrieves a single expense record by its ID.
    
    Args:
        expense_id (int): The ID of the expense to retrieve
    
    Returns:
        tuple: Expense record as a tuple, or None if not found
    """
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


def get_expense_by_category(category: str) -> list:
    """
    Retrieves all expenses in a specific category.
    
    Useful for generating category-based reports or filtering expenses.
    
    Args:
        category (str): The category to filter by (e.g., 'Groceries', 'Entertainment')
    
    Returns:
        list: List of expense tuples matching the specified category
    """
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


def get_expenses_by_roommate(roommate_id: int) -> list:
    """
    Retrieves all expenses paid by a specific roommate.
    
    Useful for generating personal expense reports or calculating individual contributions.
    
    Args:
        roommate_id (int): The ID of the roommate whose expenses to retrieve
    
    Returns:
        list: List of expense tuples paid by the specified roommate
    """
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


def update_expense(expense_id: int, date: str = None, account: str = None, 
                   category: str = None, amount: float = None, note: str = None, 
                   payer_id: int = None):
    """
    Updates an existing expense record with only the provided fields.
    
    This function uses dynamic field building to only update the fields that
    are provided (not None), making it flexible for partial updates.
    
    Args:
        expense_id (int): The ID of the expense to update
        date (str, optional): New date in 'YYYY-MM-DD' format
        account (str, optional): New account/payment method
        category (str, optional): New expense category
        amount (float, optional): New expense amount
        note (str, optional): New notes
        payer_id (int, optional): New payer roommate ID
    """
    conn = get_connection()
    cur = conn.cursor()

    # Build dynamic update query based on provided parameters
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

    # Exit early if no fields to update
    if not fields:
        conn.close()
        return

    # Build and execute the dynamic SQL query
    sql = f"UPDATE expenses SET {', '.join(fields)} WHERE id = ?"
    values.append(expense_id)

    cur.execute(sql, tuple(values))
    conn.commit()
    conn.close()


def delete_expense(expense_id: int) -> bool:
    """
    Deletes an expense record from the database.
    
    Due to foreign key constraints with CASCADE delete, this will also
    automatically remove all associated participant records from the
    expense_participants table.
    
    Args:
        expense_id (int): The ID of the expense to delete
    
    Returns:
        bool: True if the expense was successfully deleted, False otherwise
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Verify the expense exists before attempting deletion
    cur.execute("SELECT id FROM expenses WHERE id = ?", (expense_id,))
    exists = cur.fetchone()
    
    # Execute the deletion
    cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    rows_deleted = cur.rowcount
    
    conn.commit()
    conn.close()
    
    # Return success status
    return rows_deleted > 0


# -----------------------------
# Expense Participant Operations
# -----------------------------

def add_expense_participants(expense_id: int, participant_ids: list):
    """
    Adds multiple roommates as participants to an expense.
    
    This creates the many-to-many relationship between expenses and roommates.
    Uses INSERT OR IGNORE to handle cases where participant might already exist.
    
    Args:
        expense_id (int): The ID of the expense
        participant_ids (list): List of roommate IDs to add as participants
    """
    conn = get_connection()
    cur = conn.cursor()
    
    for participant_id in participant_ids:
        cur.execute("""
            INSERT OR IGNORE INTO expense_participants (expense_id, roommate_id)
            VALUES (?, ?)
        """, (expense_id, participant_id))
    
    conn.commit()
    conn.close()


def get_expense_participants(expense_id: int) -> list:
    """
    Retrieves all roommates who participated in a specific expense.
    
    Args:
        expense_id (int): The ID of the expense
    
    Returns:
        list: List of tuples containing participant information.
              Each tuple: (roommate_id, roommate_name)
    """
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT r.id, r.name 
        FROM expense_participants ep
        JOIN roommates r ON ep.roommate_id = r.id
        WHERE ep.expense_id = ?
    """, (expense_id,))
    
    participants = cur.fetchall()
    conn.close()
    return participants


def update_expense_participants(expense_id: int, participant_ids: list):
    """
    Completely replaces the participant list for an expense.
    
    This operation first removes all existing participants and then adds
    the new list. Useful for when you need to completely change who
    participated in an expense.
    
    Args:
        expense_id (int): The ID of the expense to update
        participant_ids (list): New list of roommate IDs to set as participants
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Remove all existing participants for this expense
    cur.execute("DELETE FROM expense_participants WHERE expense_id = ?", (expense_id,))
    
    # Add the new participants
    for participant_id in participant_ids:
        cur.execute("""
            INSERT INTO expense_participants (expense_id, roommate_id)
            VALUES (?, ?)
        """, (expense_id, participant_id))
    
    conn.commit()
    conn.close()