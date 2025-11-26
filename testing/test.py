import sys
import tkinter as tk
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.load_dataset import load_dataset
from models.database.db_connection import initialize_database, DB_PATH
from models.database.roomate_db import add_roommate, get_all_roommates, assign_random_payer, assign_random_participants
from models.database.expense_db import get_all_expenses
from main import RoomieSplitApp

def test_database_creation():
    """Test database creation from CSV and display app contents"""
    
    csv_path = Path(__file__).parent.parent / "assets" / "data" / "dataset.csv"
    
    print(f"Reading from: {csv_path}")
    print(f"Creating database at: {DB_PATH}")
    
    # Remove existing database if it exists
    if DB_PATH.exists():
        DB_PATH.unlink()
        print("✓ Removed existing database")
    
    # Ensure directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Initialize database schema
    initialize_database()
    print("✓ Database schema initialized")
    
    # Load dataset from CSV (using the project's CSV loader which uses pandas)
    try:
        load_dataset("assets/data/dataset.csv")
        print("✓ Dataset loaded from CSV")
    except Exception as e:
        print(f"✗ Error loading dataset: {e}")
        print("Install pandas in this environment: `pip install pandas`")
        return
    
    # Add sample roommates
    sample_roommates = [
        ("Alice Johnson", "alice@example.com", "2023-09-01"),
        ("Bob Smith", "bob@example.com", "2023-09-15"), 
        ("Charlie Brown", "charlie@example.com", "2023-10-01"),
        ("David Wilson", "david@example.com", "2023-10-15")
    ]
    for name, email, join_date in sample_roommates:
        add_roommate(name, email, join_date)
    print(f"✓ Added {len(sample_roommates)} sample roommates")
    
    # Assign random payers and participants
    expenses = get_all_expenses()
    if expenses:
        expense_ids = [e[0] for e in expenses]
        assign_random_payer(expense_ids)
        assign_random_participants(expense_ids)
        print(f"✓ Assigned payers and participants to {len(expense_ids)} expenses")
    
    print("\n--- Starting RoomieSplit Application ---\n")
    
    # Start the Tkinter app like main.py does
    root = tk.Tk()
    app = RoomieSplitApp(root)
    root.mainloop()

if __name__ == "__main__":
    test_database_creation()