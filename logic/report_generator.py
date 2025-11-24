from models import Roommate, Expense, Settlement
from .calculator import calculate_settlements, calculate_personal_budget
from typing import List, Dict

def generate_settlement_report(expenses: List[Expense], roommates: List[Roommate]) -> List[Dict[str, any]]:
    """
    Generates a formatted settlement report.

    This function calculates settlements using the calculator and formats the results
    into a list of dictionaries suitable for display in the UI.

    Args:
        expenses (List[Expense]): A list of Expense objects.
        roommates (List[Roommate]): A list of Roommate objects.

    Returns:
        List[Dict[str, any]]: A list of dictionaries, each representing a settlement line.
                              e.g., [{"Person Owing": "Bob", "Owes To": "Alice", "Amount ($)": "$20.17"}, ...]
    """
    settlements = calculate_settlements(expenses, roommates)
    formatted_report = []
    for settlement in settlements:
        formatted_report.append({
            "Person Owing": settlement.debtor_name,
            "Owes To": settlement.creditor_name,
            "Amount ($)": f"${settlement.amount:.2f}"
        })
    return formatted_report

def generate_personal_budget_report(expenses: List[Expense], roommates: List[Roommate], user_id: int) -> List[Dict[str, any]]:
    """
    Generates a formatted personal budget report for a specific user.

    This function calculates the user's personal budget using the calculator and formats the results
    into a list of dictionaries suitable for display in the UI.

    Args:
        expenses (List[Expense]): A list of Expense objects.
        roommates (List[Roommate]): A list of Roommate objects.
        user_id (int): The ID of the user whose budget report is generated.

    Returns:
        List[Dict[str, any]]: A list of dictionaries, each representing a category and its total.
                              e.g., [{"Category": "Rent", "Total Amount ($)": "$1200.00"}, ...]
    """
    personal_budget_dict = calculate_personal_budget(expenses, roommates, user_id)
    formatted_report = []
    for category, total in personal_budget_dict.items():
        formatted_report.append({
            "Category": category,
            "Total Amount ($)": f"${total:.2f}"
        })
    # Sort by amount for easier reading (optional)
    formatted_report.sort(key=lambda x: x["Total Amount ($)"], reverse=True)
    return formatted_report

def generate_summary_report(expenses: List[Expense], roommates: List[Roommate]) -> Dict[str, any]:
    """
    Generates a summary report containing total expenses, contributions, and owed amounts.

    Args:
        expenses (List[Expense]): A list of Expense objects.
        roommates (List[Roommate]): A list of Roommate objects.

    Returns:
        Dict[str, any]: A dictionary containing summary statistics.
    """
    from .calculator import calculate_total_contributions, calculate_total_owed_per_person

    total_expenses = sum(exp.amount for exp in expenses)
    total_contributions = calculate_total_contributions(expenses, roommates)
    total_owed = calculate_total_owed_per_person(expenses, roommates)

    # Create a mapping from ID to Roommate object for names
    roommate_map = {rm.id: rm for rm in roommates}

    summary = {
        "total_household_expenses": f"${total_expenses:.2f}",
        "individual_contributions": {roommate_map[rm_id].name: f"${amount:.2f}" for rm_id, amount in total_contributions.items()},
        "individual_fair_shares": {roommate_map[rm_id].name: f"${amount:.2f}" for rm_id, amount in total_owed.items()},
    }
    return summary
