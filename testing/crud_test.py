"""Quick CRUD tests for roommates and expenses.

Run with the project's venv: `.venv/bin/python3 testing/crud_test.py`
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.database.db_connection import DB_PATH, initialize_database
from models.database.roomate_db import (
    add_roommate, get_all_roommates, get_roommate_by_id,
    update_roommate, delete_roommate, assign_random_payer, assign_random_participants
)
from models.database.expense_db import (
    add_expense, get_all_expenses, get_expense_by_id,
    update_expense, delete_expense, add_expense_participants,
    get_expense_participants, update_expense_participants
)


def fail(msg):
    print("[FAIL]", msg)
    raise SystemExit(2)


def ok(msg):
    print("[OK]", msg)


def run():
    # Reset DB file
    if DB_PATH.exists():
        DB_PATH.unlink()
        print("Removed existing DB to start fresh")

    # Initialize schema
    initialize_database()
    print("Initialized DB schema")

    # ROOMMATES CRUD
    add_roommate("CRUD Tester", "crud@test.local", "2025-01-01")
    rms = get_all_roommates()
    if not rms:
        fail("No roommates after add_roommate")
    ok(f"Roommates count after add: {len(rms)}")

    rm = next((r for r in rms if r[1] == "CRUD Tester"), None)
    if not rm:
        fail("Could not find newly added roommate")
    rid = rm[0]
    ok(f"Found roommate id={rid}")

    # Update roommate
    update_roommate(rid, name="CRUD Tester Updated")
    updated = get_roommate_by_id(rid)
    if updated[1] != "CRUD Tester Updated":
        fail("Roommate update did not persist")
    ok("Roommate update persisted")

    # EXPENSES CRUD
    eid = add_expense("2025-02-01", "Card", "Test", 12.34, "note", payer_id=None)
    if not isinstance(eid, int):
        fail("add_expense did not return an int id")
    ok(f"Created expense id={eid}")

    all_exp = get_all_expenses()
    if not any(e[0] == eid for e in all_exp):
        fail("Inserted expense not found in get_all_expenses")
    ok("Expense present in DB")

    exp = get_expense_by_id(eid)
    if exp is None:
        fail("get_expense_by_id returned None")
    ok(f"get_expense_by_id returned: {exp}")

    # Update expense
    update_expense(eid, amount=99.99, note="updated")
    exp2 = get_expense_by_id(eid)
    if abs(exp2[4] - 99.99) > 1e-6 or exp2[5] != "updated":
        fail("Expense update failed")
    ok("Expense update persisted")

    # Participants
    add_expense_participants(eid, [rid])
    parts = get_expense_participants(eid)
    if not any(p[0] == rid for p in parts):
        fail("Participant add failed")
    ok("Participant added")

    update_expense_participants(eid, [])
    parts2 = get_expense_participants(eid)
    if parts2:
        fail("Participant update (clear) failed")
    ok("Participant cleared")

    # Assign payer and participants helpers
    # create more roommates and expenses to test bulk assign helpers
    add_roommate("Bulk1")
    add_roommate("Bulk2")
    # create another expense
    eid2 = add_expense("2025-02-02", "Cash", "Test", 5.0, "n")
    all_ids = [e[0] for e in get_all_expenses()]
    assign_random_payer(all_ids)
    assign_random_participants(all_ids)
    ok("assign_random_payer and assign_random_participants ran without error")

    # Delete expense
    if not delete_expense(eid):
        fail("delete_expense reported failure")
    if get_expense_by_id(eid) is not None:
        fail("Expense still present after delete")
    ok("Expense deleted successfully")

    # Delete roommate
    delete_roommate = globals().get('delete_roommate')
    # delete_roommate exists in roommate_db; import directly to be safe
    from models.database.roomate_db import delete_roommate as _del_rm
    _del_rm(rid)
    if get_roommate_by_id(rid) is not None:
        fail("Roommate still present after delete")
    ok("Roommate deleted successfully")

    print("\nAll CRUD checks passed")


if __name__ == '__main__':
    run()
