from models.database.db_connection import initialize_database
from models.database.expense_db import get_all_expenses
from models.database.roommate_db import add_roommate, assign_random_payer

# Initialize database tables if not already
initialize_database()

# Add sample roommates
sample_roommates = ["Alice", "Bob", "Charlie", "David"]
for name in sample_roommates:
    add_roommate(name)

# Assign random roommate to each expense
expenses = get_all_expenses()
expense_ids = [e[0] for e in expenses]  # extract expense IDs
assign_random_payer(expense_ids)

print(f"Added {len(sample_roommates)} roommates and assigned them to {len(expense_ids)} expenses.")