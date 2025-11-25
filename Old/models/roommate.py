# models/roommate.py

class Roommate:
    """
    Represents a roommate in the system.
    This model defines the structure for roommate data used by other modules.
    """
    def __init__(self, id: int, name: str, email: str = "", join_date: str = ""):
        """
        Initializes a Roommate object.

        Args:
            id (int): Unique identifier for the roommate. Can be None if not yet saved to DB.
            name (str): The roommate's name (required).
            email (str, optional): The roommate's email address. Defaults to "".
            join_date (str, optional): The date the roommate joined. Defaults to "".
        """
        self.id = id
        self.name = name
        self.email = email
        self.join_date = join_date

    def to_dict(self) -> dict:
        """
        Converts the Roommate object to a dictionary.

        Returns:
            dict: A dictionary representation of the roommate's data.
                  e.g., {"id": 1, "name": "Alice", "email": "alice@example.com", "join_date": "2023-09-01"}
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "join_date": self.join_date
        }

    def __repr__(self):
        """
        Provides a string representation of the Roommate object for debugging.

        Returns:
            str: A string describing the Roommate object.
        """
        return f"Roommate(id={self.id}, name='{self.name}', email='{self.email}', join_date='{self.join_date}')"

