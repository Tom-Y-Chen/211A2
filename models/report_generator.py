# models/report_generator.py
from models.calculator import (
    calculate_settlements, 
    calculate_personal_budget, 
    calculate_total_contributions, 
    calculate_total_owed_per_person
)
from typing import List, Dict, Any


def generate_settlement_report(expenses: List[tuple], roommates: List[tuple]) -> List[Dict[str, Any]]:
    """
    Generates a formatted settlement report showing who owes money to whom.
    
    This report displays the net financial settlements between roommates after
    accounting for all expenses and their fair shares. It provides a clear
    picture of the money transfers needed to balance everyone's accounts.
    
    Args:
        expenses (List[tuple]): List of expense tuples from database
                               (id, date, account, category, amount, note, payer_id)
        roommates (List[tuple]): List of roommate tuples from database
                                (id, name, email, join_date)
    
    Returns:
        List[Dict[str, Any]]: Formatted settlement report ready for UI display.
                             Each entry contains:
                             - "Person Owing": Name of the debtor
                             - "Owes To": Name of the creditor  
                             - "Amount ($)": Formatted amount owed
    """
    # Calculate raw settlements using the calculator
    settlements = calculate_settlements(expenses, roommates)
    formatted_report = []
    
    # Format each settlement for display
    for settlement in settlements:
        formatted_report.append({
            "Person Owing": settlement["debtor_name"],
            "Owes To": settlement["creditor_name"],
            "Amount ($)": f"${settlement['amount']:.2f}"  # Format as currency
        })
    
    return formatted_report


def generate_personal_budget_report(expenses: List[tuple], roommates: List[tuple], user_id: int) -> List[Dict[str, Any]]:
    """
    Generates a formatted personal budget report for a specific user.
    
    This report breaks down a user's spending by category, showing where
    their money is going. Useful for personal financial tracking and
    identifying spending patterns.
    
    Args:
        expenses (List[tuple]): List of expense tuples from database
        roommates (List[tuple]): List of roommate tuples from database
        user_id (int): The ID of the user whose budget report is generated
    
    Returns:
        List[Dict[str, Any]]: Formatted budget report sorted by amount (descending).
                             Each entry contains:
                             - "Category": Expense category name
                             - "Total Amount ($)": Formatted total spent in category
    """
    # Calculate raw budget data
    personal_budget_dict = calculate_personal_budget(expenses, roommates, user_id)
    formatted_report = []
    
    # Convert to formatted report entries
    for category, total in personal_budget_dict.items():
        formatted_report.append({
            "Category": category,
            "Total Amount ($)": f"${total:.2f}"  # Format as currency
        })
    
    # Sort by amount (highest to lowest) for better readability
    formatted_report.sort(
        key=lambda x: float(x["Total Amount ($)"].replace('$', '')), 
        reverse=True
    )
    
    return formatted_report


def generate_summary_report(expenses: List[tuple], roommates: List[tuple]) -> Dict[str, Any]:
    """
    Generates a comprehensive summary report of household finances.
    
    This report provides an overview of the financial situation including:
    - Total household expenses
    - Individual contributions (actual payments made)
    - Individual fair shares (theoretical amounts each should have paid)
    
    Useful for understanding the big picture and identifying financial patterns.
    
    Args:
        expenses (List[tuple]): List of expense tuples from database
        roommates (List[tuple]): List of roommate tuples from database
    
    Returns:
        Dict[str, Any]: Summary report containing:
                       - "total_household_expenses": Formatted total of all expenses
                       - "individual_contributions": Dict of names to formatted amounts paid
                       - "individual_fair_shares": Dict of names to formatted fair share amounts
    """
    # Calculate total household expenses
    total_expenses = sum(exp[4] for exp in expenses)  # amount at index 4
    
    # Calculate individual financial data
    total_contributions = calculate_total_contributions(expenses, roommates)
    total_owed = calculate_total_owed_per_person(expenses, roommates)

    # Create mapping from roommate ID to name for display
    roommate_map = {rm[0]: rm[1] for rm in roommates}  # rm[0] = id, rm[1] = name

    # Compile summary report
    summary = {
        "total_household_expenses": f"${total_expenses:.2f}",
        "individual_contributions": {
            roommate_map[rm_id]: f"${amount:.2f}" 
            for rm_id, amount in total_contributions.items()
        },
        "individual_fair_shares": {
            roommate_map[rm_id]: f"${amount:.2f}" 
            for rm_id, amount in total_owed.items()
        },
    }
    
    return summary
