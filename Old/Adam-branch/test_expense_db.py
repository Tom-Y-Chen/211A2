# tests/test_expense_crud.py

from models.database.expense_db import add_expense, get_all_expenses, update_expense, delete_expense

def test_expense_crud():
    print("Initial expenses in DB:")
    expenses = get_all_expenses()
    print(expenses[:5])  # print first 5 for brevity

    # ----------------------
    # 1. Test creation
    # ----------------------
    print("\nAdding a new expense...")
    add_expense(
        date="2025-11-21",
        account="Cash",
        category="Food & Drink",
        note="Lunch",
        amount=15.50
    )

    expenses = get_all_expenses()
    print("After addition:")
    print(expenses[-5:])  # last 5 records

    # ----------------------
    # 2. Test update
    # ----------------------
    last_expense_id = expenses[-1][0]  # assuming first field is ID
    print(f"\nUpdating expense ID {last_expense_id}...")
    update_expense(
        expense_id=last_expense_id,
        date="2025-11-21",
        account="Card",
        category="Food & Drink",
        note="Lunch with coffee",
        amount=17.00
    )

    updated_expense = [e for e in get_all_expenses() if e[0] == last_expense_id][0]
    print("After update:")
    print(updated_expense)

    # ----------------------
    # 3. Test deletion
    # ----------------------
    print(f"\nDeleting expense ID {last_expense_id}...")
    delete_expense(last_expense_id)

    expenses = get_all_expenses()
    print("After deletion (last 5 records):")
    print(expenses[-5:])

if __name__ == "__main__":
    test_expense_crud()
