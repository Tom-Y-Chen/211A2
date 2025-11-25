# validators.py

import re
from datetime import datetime

# =========================
# Expense validators
# =========================

def validate_date(date_str):
    """
    Validate date string (expects 'YYYY-MM-DD').
    Returns True if valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_amount(amount):
    """
    Validate that amount is a number and non-negative.
    """
    try:
        amt = float(amount)
        return amt >= 0
    except (ValueError, TypeError):
        return False

def validate_category(category, allowed_categories=None):
    """
    Validate category is non-empty and optionally in allowed list.
    """
    if not category or not isinstance(category, str):
        return False
    if allowed_categories:
        return category in allowed_categories
    return True

def validate_note(note):
    """
    Optional field: make sure it's a string (can be empty).
    """
    return isinstance(note, str)

def validate_account(account):
    """
    Optional field: make sure it's a string (can be empty).
    """
    return isinstance(account, str)


# =========================
# Roommate validators
# =========================

def validate_name(name):
    """
    Validate roommate name is non-empty string.
    """
    return isinstance(name, str) and len(name.strip()) > 0

def validate_email(email):
    """
    Validate email using a simple regex.
    """
    if not email or not isinstance(email, str):
        return False
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

# =========================
# Generic helper
# =========================

def validate_expense_record(date, account, category, note, amount, allowed_categories=None):
    """
    Validate an entire expense record. Returns True if all valid.
    """
    return (validate_date(date) and
            validate_account(account) and
            validate_category(category, allowed_categories) and
            validate_note(note) and
            validate_amount(amount))
