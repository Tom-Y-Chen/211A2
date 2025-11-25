# controllers/roommate_controller.py
from models.database.roomate_db import (
    add_roommate, 
    get_all_roommates, 
    get_roommate_by_id, 
    update_roommate, 
    delete_roommate
)


class RoommateController:
    """
    Controller class for managing roommate-related business logic and operations.
    
    This class serves as the intermediary between the UI layer and the database layer,
    handling validation, error handling, and business rules for roommate operations.
    """
    
    def __init__(self):
        """Initialize the RoommateController."""
        pass

    def add_roommate(self, name: str, email: str = "", join_date: str = None) -> tuple:
        """
        Adds a new roommate to the database with validation.
        
        Performs input validation and sets default values before delegating
        to the database layer. Automatically sets join_date to today if not provided.
        
        Args:
            name (str): Full name of the new roommate
            email (str, optional): Email address. Defaults to empty string.
            join_date (str, optional): Join date in 'YYYY-MM-DD' format. Defaults to None.
        
        Returns:
            tuple: (success: bool, message: str)
                   - If successful: (True, success_message)
                   - If failed: (False, error_message)
        """
        try:
            # Validate required name field
            if not name or not name.strip():
                return False, "Name is required."
            
            # Set default join_date to today if not provided
            if not join_date:
                from datetime import datetime
                join_date = datetime.today().strftime('%Y-%m-%d')
            
            # Delegate to database layer
            add_roommate(name.strip(), email.strip(), join_date)
            return True, f"Roommate '{name}' added successfully."
            
        except Exception as e:
            return False, f"Failed to add roommate: {str(e)}"

    def get_all_roommates(self) -> tuple:
        """
        Retrieves all roommates from the database.
        
        Returns:
            tuple: (success: bool, result: list/str)
                   - If successful: (True, list_of_roommates)
                   - If failed: (False, error_message)
        """
        try:
            roommates = get_all_roommates()
            return True, roommates
        except Exception as e:
            return False, f"Failed to load roommates: {str(e)}"

    def get_roommate(self, roommate_id: int) -> tuple:
        """
        Retrieves a specific roommate by their ID.
        
        Args:
            roommate_id (int): The ID of the roommate to retrieve
        
        Returns:
            tuple: (success: bool, result: tuple/str)
                   - If successful: (True, roommate_data)
                   - If failed: (False, error_message)
        """
        try:
            roommate = get_roommate_by_id(roommate_id)
            if roommate:
                return True, roommate
            else:
                return False, f"Roommate with ID {roommate_id} not found."
        except Exception as e:
            return False, f"Failed to get roommate: {str(e)}"

    def update_roommate(self, roommate_id: int, name: str = None, email: str = None, 
                       join_date: str = None) -> tuple:
        """
        Updates roommate information with validation.
        
        Performs input validation before delegating to the database layer.
        Only updates fields that are provided (not None).
        
        Args:
            roommate_id (int): The ID of the roommate to update
            name (str, optional): New full name. Defaults to None.
            email (str, optional): New email address. Defaults to None.
            join_date (str, optional): New join date in 'YYYY-MM-DD' format. Defaults to None.
        
        Returns:
            tuple: (success: bool, message: str)
                   - If successful: (True, success_message)
                   - If failed: (False, error_message)
        """
        try:
            # Validate name if provided
            if name is not None and not name.strip():
                return False, "Name cannot be empty."
            
            # Validate date format if provided
            if join_date is not None:
                from datetime import datetime
                try:
                    datetime.strptime(join_date, '%Y-%m-%d')
                except ValueError:
                    return False, "Join date format should be YYYY-MM-DD."
            
            # Delegate to database layer
            update_roommate(roommate_id, name, email, join_date)
            return True, f"Roommate updated successfully."
            
        except Exception as e:
            return False, f"Failed to update roommate: {str(e)}"

    def delete_roommate(self, roommate_id: int) -> tuple:
        """
        Deletes a roommate from the database.
        
        Note: This operation may fail due to foreign key constraints if the
        roommate is referenced in existing expenses. The UI layer should
        handle this gracefully.
        
        Args:
            roommate_id (int): The ID of the roommate to delete
        
        Returns:
            tuple: (success: bool, message: str)
                   - If successful: (True, success_message)
                   - If failed: (False, error_message)
        """
        try:
            delete_roommate(roommate_id)
            return True, "Roommate deleted successfully."
        except Exception as e:
            return False, f"Failed to delete roommate: {str(e)}"

    def validate_email(self, email: str) -> bool:
        """
        Performs basic email format validation.
        
        This is a simple validation that checks for the presence of '@' and '.'.
        For production use, consider using a more robust email validation library.
        
        Args:
            email (str): The email address to validate
        
        Returns:
            bool: True if email is valid or empty, False if invalid format
        """
        # Empty email is allowed based on database schema
        if not email:
            return True
        
        # Basic format check - contains '@' and '.'
        if '@' in email and '.' in email:
            return True
            
        return False
