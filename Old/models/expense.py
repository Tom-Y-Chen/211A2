# models/expense.py

class Expense:
    """
    Represents an expense in the system.
    This model defines the structure for expense data used by other modules.
    """
    def __init__(self, id: int, amount: float, date: str, category: str, payer_id: int, participants: list[int]):
        """
        Initializes an Expense object.

        Args:
            id (int): Unique identifier for the expense. Can be None if not yet saved to DB.
            amount (float): The total amount of the expense (required, positive).
            date (str): The date the expense was incurred (required, format YYYY-MM-DD).
            category (str): The category of the expense (e.g., Rent, Groceries) (required).
            payer_id (int): The ID of the roommate who paid (required, references Roommate.id).
            participants (list[int]): A list of roommate IDs who participated in the expense (required, non-empty).
        """
        self.id = id
        self.amount = amount
        self.date = date
        self.category = category
        self.payer_id = payer_id
        self.participants = participants # List of integers representing roommate IDs

    def to_dict(self) -> dict:
        """
        Converts the Expense object to a dictionary.

        Returns:
            dict: A dictionary representation of the expense's data.
                  e.g., {"id": 1, "amount": 120.5, "date": "2023-10-15", "category": "Groceries", "payer_id": 1, "participants": [1, 2, 3]}
        """
        return {
            "id": self.id,
            "amount": self.amount,
            "date": self.date,
            "category": self.category,
            "payer_id": self.payer_id,
            "participants": self.participants # List of IDs
        }

    def __repr__(self):
        """
        Provides a string representation of the Expense object for debugging.

        Returns:
            str: A string describing the Expense object.
        """
        return f"Expense(id={self.id}, amount={self.amount}, date='{self.date}', category='{self.category}', payer_id={self.payer_id}, participants={self.participants})"
