from models import Roommate, Expense, Settlement
from typing import List, Dict, Tuple

def calculate_settlements(expenses: List[Expense], roommates: List[Roommate]) -> List[Settlement]:
    """
    Calculates settlements based on expenses and roommates.

    This function determines how much each roommate owes or is owed by others
    based on the expenses they've paid and participated in.

    Args:
        expenses (List[Expense]): A list of Expense objects.
        roommates (List[Roommate]): A list of Roommate objects.

    Returns:
        List[Settlement]: A list of Settlement objects representing who owes whom.
                         e.g., [{"debtor": "Bob", "creditor": "Alice", "amount": 20.17}, ...]
    """
    if not expenses or not roommates:
        return []

    # Create a mapping from ID to Roommate object for quick lookup
    roommate_map = {rm.id: rm for rm in roommates}

    # Initialize balances: {roommate_id: net_balance}
    # Positive balance means the person is owed money (paid more than they owe)
    # Negative balance means the person owes money (paid less than they owe)
    balances = {rm.id: 0.0 for rm in roommates}

    # Process each expense
    for exp in expenses:
        payer_id = exp.payer_id
        amount = exp.amount
        participant_ids = exp.participants

        if not participant_ids:
            # Should ideally be prevented by validation, but handle gracefully
            continue

        # Calculate the share per participant
        share_per_person = amount / len(participant_ids)

        # The payer's balance increases by the total amount they paid
        balances[payer_id] += amount

        # Each participant's balance decreases by their share
        for pid in participant_ids:
            balances[pid] -= share_per_person

    # Identify creditors (positive balance) and debtors (negative balance)
    creditors = {rm_id: bal for rm_id, bal in balances.items() if bal > 0}
    debtors = {rm_id: abs(bal) for rm_id, bal in balances.items() if bal < 0}

    # Generate settlements using a simple algorithm:
    # Repeatedly find the largest creditor and the largest debtor,
    # and settle the smaller of the two amounts.
    settlements = []
    while creditors and debtors:
        # Get the first item from the sorted dictionaries (largest creditor/debtor)
        # Note: This is a simplification; a more robust approach might sort repeatedly.
        # However, this simple approach works correctly for generating settlements.
        creditor_id, creditor_balance = next(iter(sorted(creditors.items(), key=lambda item: item[1], reverse=True)))
        debtor_id, debtor_balance = next(iter(sorted(debtors.items(), key=lambda item: item[1], reverse=True)))

        # The amount to settle is the smaller of the creditor's claim and the debtor's debt
        amount_to_settle = min(creditor_balance, debtor_balance)

        # Create a settlement record
        creditor_name = roommate_map[creditor_id].name
        debtor_name = roommate_map[debtor_id].name
        settlement = Settlement(
            debtor_id=debtor_id,
            creditor_id=creditor_id,
            amount=round(amount_to_settle, 2), # Round to 2 decimal places for currency
            debtor_name=debtor_name,
            creditor_name=creditor_name
        )
        settlements.append(settlement)

        # Update the balances after this settlement
        creditors[creditor_id] -= amount_to_settle
        debtors[debtor_id] -= amount_to_settle

        # Remove the creditor or debtor from the list if their balance is settled
        if creditors[creditor_id] < 0.01: # Use a small epsilon to handle floating point inaccuracies
            del creditors[creditor_id]
        if debtors[debtor_id] < 0.01:
            del debtors[debtor_id]

    return settlements

def calculate_personal_budget(expenses: List[Expense], roommates: List[Roommate], user_id: int) -> Dict[str, float]:
    """
    Calculates personal budget summary for a specific user.

    This function aggregates the expenses incurred by a specific user,
    grouped by category.

    Args:
        expenses (List[Expense]): A list of Expense objects.
        roommates (List[Roommate]): A list of Roommate objects (for name lookup if needed, though not used here).
        user_id (int): The ID of the user whose budget is calculated.

    Returns:
        Dict[str, float]: A dictionary summarizing expenses by category for the user.
                          e.g., {"Rent": 1200.00, "Groceries": 300.50, ...}
    """
    personal_budget = {}

    for exp in expenses:
        # Only consider expenses where the user was the payer
        if exp.payer_id == user_id:
            category = exp.category
            amount = exp.amount
            personal_budget[category] = personal_budget.get(category, 0.0) + amount

    # Round the final amounts for currency display
    for category in personal_budget:
        personal_budget[category] = round(personal_budget[category], 2)

    return personal_budget

def calculate_total_contributions(expenses: List[Expense], roommates: List[Roommate]) -> Dict[int, float]:
    """
    Calculates the total amount paid by each roommate.

    Args:
        expenses (List[Expense]): A list of Expense objects.
        roommates (List[Roommate]): A list of Roommate objects.

    Returns:
        Dict[int, float]: A dictionary mapping roommate ID to their total contributions.
    """
    contributions = {rm.id: 0.0 for rm in roommates}
    for exp in expenses:
        contributions[exp.payer_id] += exp.amount

    # Round the final amounts
    for rm_id in contributions:
        contributions[rm_id] = round(contributions[rm_id], 2)

    return contributions

def calculate_total_owed_per_person(expenses: List[Expense], roommates: List[Roommate]) -> Dict[int, float]:
    """
    Calculates the total amount each roommate should have paid (their fair share).

    Args:
        expenses (List[Expense]): A list of Expense objects.
        roommates (List[Roommate]): A list of Roommate objects.

    Returns:
        Dict[int, float]: A dictionary mapping roommate ID to their total owed amount.
    """
    total_owed = {rm.id: 0.0 for rm in roommates}

    for exp in expenses:
        share_per_person = exp.amount / len(exp.participants)
        for pid in exp.participants:
            total_owed[pid] += share_per_person

    # Round the final amounts
    for rm_id in total_owed:
        total_owed[rm_id] = round(total_owed[rm_id], 2)

    return total_owed