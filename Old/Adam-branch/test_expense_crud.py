from models.database.db_connection import initialize_database, get_connection

initialize_database()
conn = get_connection()
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cur.fetchall())  # should show your tables
conn.close()


# from models.database.db_connection import initialize_database, get_connection
# from models.database.roommate_db import RoommateDB
# from models.database.expense_db import ExpenseDB

# def test_database():
#     # Initialize tables
#     initialize_database()

#     roommates = RoommateDB()
#     expenses = ExpenseDB()

#     print("\n--- Creating roommates ---")
#     roommates.add("Alice", "alice@example.com")
#     roommates.add("Bob", "bob@example.com")

#     print("All roommates:", roommates.get_all())

#     print("\n--- Adding expenses ---")
#     expenses.add(date="2025-01-01", amount=50.0, category="Groceries", payer_id=1, note="Fruit")
#     expenses.add(date="2025-01-02", amount=30.0, category="Utilities", payer_id=2, note="Water bill")

#     print("All expenses:", expenses.get_all())

# if __name__ == "__main__":
#     test_database()
