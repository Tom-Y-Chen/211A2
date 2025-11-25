# models/database/roommate_db.py
from models.database.db_connection import get_connection
import random

# -----------------------------
# Roommate CRUD Operations
# -----------------------------

def add_roommate(name: str, email: str = "", join_date: str = None) -> None:
    """
    Creates a new roommate record in the database.
    
    Args:
        name (str): Full name of the roommate (required)
        email (str, optional): Email address of the roommate. Defaults to empty string.
        join_date (str, optional): Join date in 'YYYY-MM-DD' format. Defaults to None.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute(
        "INSERT INTO roommates (name, email, join_date) VALUES (?, ?, ?)",
        (name, email, join_date)
    )
    
    conn.commit()
    conn.close()


def get_all_roommates() -> list:
    """
    Retrieves all roommate records from the database.
    
    Returns:
        list: List of roommate tuples ordered by ID.
              Each tuple: (id, name, email, join_date)
    """
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id, name, email, join_date FROM roommates")
    results = cur.fetchall()
    
    conn.close()
    return results


def get_roommate_by_id(roommate_id: int) -> tuple:
    """
    Retrieves a single roommate record by ID.
    
    Args:
        roommate_id (int): The ID of the roommate to retrieve
    
    Returns:
        tuple: Roommate record as (id, name, email), or None if not found
    """
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute(
        "SELECT id, name, email FROM roommates WHERE id = ?",
        (roommate_id,)
    )
    
    result = cur.fetchone()
    conn.close()
    return result


def update_roommate(roommate_id: int, name: str = None, email: str = None, 
                    join_date: str = None) -> None:
    """
    Updates a roommate's information with only the provided fields.
    
    This function uses dynamic field building to only update fields that are
    provided (not None), making it flexible for partial updates.
    
    Args:
        roommate_id (int): The ID of the roommate to update
        name (str, optional): New full name for the roommate
        email (str, optional): New email address
        join_date (str, optional): New join date in 'YYYY-MM-DD' format
    """
    conn = get_connection()
    cur = conn.cursor()

    # Build dynamic update query based on provided parameters
    fields = []
    values = []

    if name is not None:
        fields.append("name = ?")
        values.append(name)

    if email is not None:
        fields.append("email = ?")
        values.append(email)

    if join_date is not None:
        fields.append("join_date = ?")
        values.append(join_date)

    # Exit early if no fields to update
    if not fields:
        conn.close()
        return

    # Build and execute the dynamic SQL query
    sql = f"UPDATE roommates SET {', '.join(fields)} WHERE id = ?"
    values.append(roommate_id)

    cur.execute(sql, tuple(values))
    conn.commit()
    conn.close()


def delete_roommate(roommate_id: int) -> None:
    """
    Deletes a roommate record from the database.
    
    Important: This operation may fail due to foreign key constraints if the
    roommate is referenced in expenses (as payer or participant). Consider
    handling this constraint in the UI layer with appropriate user feedback.
    
    Args:
        roommate_id (int): The ID of the roommate to delete
    """
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM roommates WHERE id = ?", (roommate_id,))
    
    conn.commit()
    conn.close()


# -----------------------------
# Random Assignment Operations
# -----------------------------

def assign_random_payer(expense_ids: list) -> None:
    """
    Assigns a random roommate as the payer for each specified expense.
    
    This is typically used during database initialization to assign payers
    to imported expenses that don't have payer information.
    
    Args:
        expense_ids (list): List of expense IDs to assign random payers to
    
    Raises:
        ValueError: If there are no roommates in the database to assign
    """
    roommates = get_all_roommates()
    if not roommates:
        raise ValueError("No roommates in database to assign.")

    conn = get_connection()
    cur = conn.cursor()

    for expense_id in expense_ids:
        # Select a random roommate ID from all available roommates
        random_roommate_id = random.choice(roommates)[0]
        
        cur.execute(
            "UPDATE expenses SET payer_id = ? WHERE id = ?",
            (random_roommate_id, expense_id)
        )

    conn.commit()
    conn.close()


def assign_random_participants(expense_ids: list) -> None:
    """
    Assigns random participants to each expense, ensuring the payer is always included.
    
    This function creates realistic expense participation scenarios by:
    1. Always including the expense payer as a participant
    2. Randomly selecting 0 to (total_roommates - 1) additional participants
    3. Ensuring no duplicate participants
    
    Args:
        expense_ids (list): List of expense IDs to assign random participants to
    
    Raises:
        ValueError: If there are no roommates in the database to assign
    """
    roommates = get_all_roommates()
    if not roommates:
        raise ValueError("No roommates in database to assign.")
    
    conn = get_connection()
    cur = conn.cursor()

    for expense_id in expense_ids:
        # Get the current payer for this expense
        cur.execute("SELECT payer_id FROM expenses WHERE id = ?", (expense_id,))
        result = cur.fetchone()
        payer_id = result[0] if result else None
        
        # Skip expenses without a payer assigned
        if not payer_id:
            continue
            
        # Determine how many total participants (1 to all roommates)
        num_participants = random.randint(1, len(roommates))
        
        # Start participant list with the payer (always included)
        participant_ids = [payer_id]
        
        # Add additional random participants if needed
        other_roommates = [rm for rm in roommates if rm[0] != payer_id]
        if other_roommates and num_participants > 1:
            # Calculate how many additional participants to add
            additional_count = min(num_participants - 1, len(other_roommates))
            additional_participants = random.sample(other_roommates, additional_count)
            participant_ids.extend([rm[0] for rm in additional_participants])
        
        # Clear existing participants and add the new random set
        cur.execute("DELETE FROM expense_participants WHERE expense_id = ?", (expense_id,))
        
        for participant_id in participant_ids:
            cur.execute(
                "INSERT OR IGNORE INTO expense_participants (expense_id, roommate_id) VALUES (?, ?)",
                (expense_id, participant_id)
            )

    conn.commit()
    conn.close()
    print(f"Assigned random participants to {len(expense_ids)} expenses (payers always included)")
