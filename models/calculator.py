# models/calculator.py

def calculate_settlements(expenses: list[tuple], roommates: list[tuple]) -> list[dict]:
    """
    Calculates financial settlements between roommates based on expense data.
    
    This function determines how much each roommate owes or is owed by others
    based on the expenses they've paid and participated in. It uses a simplified
    algorithm that assumes all roommates participate in every expense.
    
    Args:
        expenses (list[tuple]): List of expense tuples from database 
                                (id, date, account, category, amount, note, payer_id)
        roommates (list[tuple]): List of roommate tuples from database 
                                 (id, name, email, join_date)
    
    Returns:
        list[Dict]: List of settlement dictionaries representing who owes whom.
                   Each dict contains: debtor_id, creditor_id, amount, debtor_name, creditor_name
    """
    # Handle empty data cases
    if not expenses or not roommates:
        return []

    # Create mapping from roommate ID to name for easy lookup
    roommate_map = {rm[0]: rm[1] for rm in roommates}  # rm[0] = id, rm[1] = name

    # Initialize balances: {roommate_id: net_balance}
    # Positive balance = person is owed money (paid more than they owe)
    # Negative balance = person owes money (paid less than they owe)
    balances = {rm[0]: 0.0 for rm in roommates}

    # Process each expense to calculate net balances
    for exp in expenses:
        # Extract expense data from tuple
        # Tuple structure: (id, date, account, category, amount, note, payer_id)
        payer_id = exp[6]  # payer_id is at index 6
        amount = exp[4]    # amount is at index 4
        
        participant_ids = [rm[0] for rm in roommates]

        # Skip expenses with no participants (shouldn't happen with validation)
        if not participant_ids:
            continue

        # Calculate equal share per participant
        share_per_person = amount / len(participant_ids)

        # Update balances:
        # Payer's balance increases (they paid the full amount)
        balances[payer_id] += amount
        
        # Each participant's balance decreases (they owe their share)
        for participant_id in participant_ids:
            balances[participant_id] -= share_per_person

    # Separate creditors (positive balance) and debtors (negative balance)
    creditors = {rm_id: bal for rm_id, bal in balances.items() if bal > 0}
    debtors = {rm_id: abs(bal) for rm_id, bal in balances.items() if bal < 0}

    # Generate settlements using a greedy algorithm:
    # Repeatedly settle the largest creditor with the largest debtor
    settlements = []
    while creditors and debtors:
        # Find the largest creditor and largest debtor
        creditor_id, creditor_balance = next(iter(sorted(creditors.items(), 
                                                       key=lambda item: item[1], 
                                                       reverse=True)))
        debtor_id, debtor_balance = next(iter(sorted(debtors.items(), 
                                                   key=lambda item: item[1], 
                                                   reverse=True)))

        # Settle the smaller of the two amounts
        amount_to_settle = min(creditor_balance, debtor_balance)

        # Create settlement record
        settlement = {
            "debtor_id": debtor_id,
            "creditor_id": creditor_id,
            "amount": round(amount_to_settle, 2),
            "debtor_name": roommate_map[debtor_id],
            "creditor_name": roommate_map[creditor_id]
        }
        settlements.append(settlement)

        # Update balances after settlement
        creditors[creditor_id] -= amount_to_settle
        debtors[debtor_id] -= amount_to_settle

        # Remove fully settled balances (using epsilon for floating point precision)
        if creditors[creditor_id] < 0.01:
            del creditors[creditor_id]
        if debtors[debtor_id] < 0.01:
            del debtors[debtor_id]

    return settlements


def calculate_personal_budget(expenses: list[tuple], roommates: list[tuple], user_id: int) -> dict[str, float]:
    """
    Calculates personal budget summary for a specific user by category.
    
    Aggregates all expenses paid by the specified user and groups them by category
    to show spending patterns.
    
    Args:
        expenses (list[tuple]): List of expense tuples from database
        roommates (list[tuple]): List of roommate tuples (unused in this function)
        user_id (int): The ID of the user whose budget is being calculated
    
    Returns:
        dict[str, float]: Dictionary mapping category names to total amounts spent
                         by the user in that category
    """
    personal_budget = {}

    for exp in expenses:
        # Tuple structure: (id, date, account, category, amount, note, payer_id)
        if exp[6] == user_id:  # Check if this expense was paid by our user
            category = exp[3]  # category at index 3
            amount = exp[4]    # amount at index 4
            
            # Accumulate amount for this category
            personal_budget[category] = personal_budget.get(category, 0.0) + amount

    # Round all amounts to 2 decimal places for currency display
    for category in personal_budget:
        personal_budget[category] = round(personal_budget[category], 2)

    return personal_budget


def calculate_total_contributions(expenses: list[tuple], roommates: list[tuple]) -> dict[int, float]:
    """
    Calculates the total amount paid by each roommate across all expenses.
    
    This shows how much each person has actually spent, regardless of who should
    have paid for what.
    
    Args:
        expenses (list[tuple]): List of expense tuples from database
        roommates (list[tuple]): List of roommate tuples from database
    
    Returns:
        dict[int, float]: Dictionary mapping roommate IDs to their total contributions
    """
    # Initialize contributions to zero for all roommates
    contributions = {rm[0]: 0.0 for rm in roommates}
    
    # Sum up all expenses paid by each roommate
    for exp in expenses:
        payer_id = exp[6]  # payer_id at index 6
        amount = exp[4]    # amount at index 4
        contributions[payer_id] += amount

    # Round all amounts for clean display
    for rm_id in contributions:
        contributions[rm_id] = round(contributions[rm_id], 2)

    return contributions


def calculate_total_owed_per_person(expenses: list[tuple], roommates: list[tuple]) -> dict[int, float]:
    """
    Calculates the fair share amount each roommate should have paid.
    
    This represents the ideal distribution of expenses if everything was split
    equally among all participants for each expense.
    
    Args:
        expenses (list[tuple]): List of expense tuples from database
        roommates (list[tuple]): List of roommate tuples from database
    
    Returns:
        dict[int, float]: Dictionary mapping roommate IDs to their total fair share amount
    """
    # Initialize owed amounts to zero for all roommates
    total_owed = {rm[0]: 0.0 for rm in roommates}

    # Calculate each person's share of each expense
    for exp in expenses:
        participant_ids = [rm[0] for rm in roommates]
        amount = exp[4]  # amount at index 4
        
        # Calculate equal share for each participant
        share_per_person = amount / len(participant_ids)
        
        # Add this expense's share to each participant's total
        for participant_id in participant_ids:
            total_owed[participant_id] += share_per_person

    # Round all amounts for clean display
    for rm_id in total_owed:
        total_owed[rm_id] = round(total_owed[rm_id], 2)

    return total_owed
