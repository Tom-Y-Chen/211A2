import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.validators import (
    validate_date, validate_amount, validate_category, validate_note,
    validate_account, validate_name, validate_email, validate_expense_record
)

cases = [
    ("validate_date", "2024-01-02", validate_date, True),
    ("validate_date_bad", "2024-13-02", validate_date, False),
    ("validate_amount_int", 100, validate_amount, True),
    ("validate_amount_neg", -5, validate_amount, False),
    ("validate_amount_str", "12.34", validate_amount, True),
    ("validate_amount_badstr", "abc", validate_amount, False),
    ("validate_category_ok", "Groceries", lambda v: validate_category(v, ["Groceries","Rent"]), True),
    ("validate_category_bad", "Other", lambda v: validate_category(v, ["Groceries","Rent"]), False),
    ("validate_note_ok", "some note", validate_note, True),
    ("validate_note_not_str", None, validate_note, False),
    ("validate_account_ok", "Cash", validate_account, True),
    ("validate_name_ok", "Alice", validate_name, True),
    ("validate_name_empty", "  ", validate_name, False),
    ("validate_email_ok", "a@b.com", validate_email, True),
    ("validate_email_bad", "not-an-email", validate_email, False),
]

print('Running validator quick checks')
failed = []
for name, value, fn, expected in cases:
    try:
        result = fn(value)
    except Exception as e:
        result = f"EXCEPTION: {e}"
    ok = (result == expected)
    print(f"{name}: input={value!r:15} -> {result!r:10} expected={expected} {'OK' if ok else 'FAIL'}")
    if not ok:
        failed.append((name, value, result, expected))

# Full record check
record_ok = validate_expense_record("2024-01-01", "Cash", "Groceries", "note", "12.5", ["Groceries","Rent"]) 
record_bad = validate_expense_record("bad-date", "Cash", "Groceries", "note", "12.5", ["Groceries","Rent"]) 
print('\nvalidate_expense_record good ->', record_ok)
print('validate_expense_record bad (date) ->', record_bad)

if failed:
    print('\nSome validator checks failed:')
    for f in failed:
        print(f)
    raise SystemExit(2)
else:
    print('\nAll validation quick-checks passed')
