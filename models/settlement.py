# models/settlement.py

class Settlement:
    """
    Represents a single settlement entry (who owes whom).
    This is the output model for the calculation logic.
    """
    def __init__(self, debtor_id: int, creditor_id: int, amount: float, debtor_name: str, creditor_name: str):
        """
        Initializes a Settlement object.

        Args:
            debtor_id (int): The ID of the roommate who owes money.
            creditor_id (int): The ID of the roommate who is owed money.
            amount (float): The amount of money owed.
            debtor_name (str): The name of the debtor (for display).
            creditor_name (str): The name of the creditor (for display).
        """
        self.debtor_id = debtor_id
        self.creditor_id = creditor_id
        self.amount = amount
        self.debtor_name = debtor_name
        self.creditor_name = creditor_name

    def to_dict(self) -> dict:
        """
        Converts the Settlement object to a dictionary.

        Returns:
            dict: A dictionary representation of the settlement.
                  e.g., {"debtor_id": 2, "creditor_id": 1, "amount": 20.17, "debtor_name": "Bob", "creditor_name": "Alice"}
        """
        return {
            "debtor_id": self.debtor_id,
            "creditor_id": self.creditor_id,
            "amount": self.amount,
            "debtor_name": self.debtor_name,
            "creditor_name": self.creditor_name
        }

    def __repr__(self):
        """
        Provides a string representation of the Settlement object for debugging.

        Returns:
            str: A string describing the Settlement object.
        """
        return f"Settlement(debtor='{self.debtor_name}' (ID {self.debtor_id}) owes creditor '{self.creditor_name}' (ID {self.creditor_id}) ${self.amount:.2f})"

# Optional: Define an aggregate settlement result model
class SettlementSummary:
    """
    Represents a summary of all settlements.
    """
    def __init__(self, settlements: list['Settlement']):
        """
        Initializes a SettlementSummary object.

        Args:
            settlements (list[Settlement]): A list of Settlement objects.
        """
        self.settlements = settlements

    def to_list_of_dicts(self) -> list[dict]:
        """
        Converts the summary to a list of settlement dictionaries.

        Returns:
            list[dict]: A list of dictionaries, each representing a settlement.
        """
        return [s.to_dict() for s in self.settlements]

    def __repr__(self):
        """
        Provides a string representation of the SettlementSummary object for debugging.

        Returns:
            str: A string describing the SettlementSummary object.
        """
        return f"SettlementSummary(total_settlements={len(self.settlements)})"