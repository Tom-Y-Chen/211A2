import tkinter as tk
from tkinter import ttk
from views.dashboard import DashboardFrame
from views.roommate_view import RoommateManagerFrame
from views.expense_view import ExpenseEntryFrame
from views.report_view import ReportFrame
from views.navigation import NavigationFrame

# Import the controller
from controllers.roommate_controller import RoommateController

class RoomieSplitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RoomieSplit - Expense Tracker")
        self.root.geometry("800x600")
        self.root.minsize(1000, 400)

        # --- Create controllers ---
        self.roommate_controller = RoommateController()
        
        # --- Initialize database and sample data ---
        self.initialize_app_data()

        # --- Style Configuration ---
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TEntry', font=('Arial', 10))
        self.style.configure('TCombobox', font=('Arial', 10))

        # --- Main Container ---
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Initialize and display main dashboard ---
        self.frames = {}
        self.current_frame = None
        self._create_frames()
        self.show_frame("Dashboard")

    def initialize_app_data(self):
        """
        Initialize database and load sample data including:
        - Roommates table with sample roommates
        - Expenses table with dataset
        - Random assignment of payers and participants to expenses
        """
        try:
            from models.database.db_connection import initialize_database
            from models.database.roomate_db import get_all_roommates, add_roommate, assign_random_payer, assign_random_participants
            from models.database.expense_db import get_all_expenses
            
            # Initialize database tables
            initialize_database()
            
            # Check if we need to add sample roommates
            roommates = get_all_roommates()
            if not roommates:
                # Add sample roommates with full information
                sample_roommates = [
                    ("Alice Johnson", "alice@example.com", "2023-09-01"),
                    ("Bob Smith", "bob@example.com", "2023-09-15"), 
                    ("Charlie Brown", "charlie@example.com", "2023-10-01"),
                    ("David Wilson", "david@example.com", "2023-10-15")
                ]
                for name, email, join_date in sample_roommates:
                    add_roommate(name, email, join_date)
                print(f"Added {len(sample_roommates)} sample roommates")
            else:
                print(f"Database already has {len(roommates)} roommates")
            
            # Load expenses dataset if not already loaded
            expenses = get_all_expenses()
            if not expenses:  # Only load if no expenses exist
                try:
                    from utils.load_dataset import load_dataset
                    load_dataset("assets/data/dataset.csv")
                    print("Expense dataset loaded successfully")
                    
                    # Verify expenses were loaded
                    expenses = get_all_expenses()
                    
                except FileNotFoundError:
                    print("Warning: Expense dataset file not found")
                except Exception as e:
                    print(f"Warning: Could not load expense dataset: {e}")
            else:
                print(f"Database already has {len(expenses)} expenses")
            
            # Process expenses: assign random payers and participants
            expenses = get_all_expenses()
            if expenses:
                # Assign random payers to expenses without payers
                expenses_without_payers = [e for e in expenses if e[6] is None]  # payer_id at index 6
                if expenses_without_payers:
                    expense_ids = [e[0] for e in expenses_without_payers]
                    assign_random_payer(expense_ids)
                    print(f"Assigned random payers to {len(expense_ids)} expenses")
                else:
                    print("All expenses already have payers assigned")
                
                # Assign random participants to all expenses
                all_expense_ids = [e[0] for e in expenses]
                assign_random_participants(all_expense_ids)
                print(f"Assigned random participants to {len(all_expense_ids)} expenses")
                    
            else:
                print("No expenses to assign roommates to")
                
        except Exception as e:
            print("Error during initialization:", str(e))

    def _create_frames(self):
        """Create all application frames and set up navigation structure"""
        # Frame configuration dictionary
        FRAME_CONFIG = {
            # Dashboard doesn't need navigation bar
            "Dashboard": DashboardFrame,
            # Other frames need navigation bar
            "RoommateManager": RoommateManagerFrame,
            "ExpenseEntry": ExpenseEntryFrame,
            "Report": ReportFrame,
        }

        for name, frame_class in FRAME_CONFIG.items():
            if name == "Dashboard":
                # Dashboard uses simple frame without navigation
                frame = frame_class(self.main_container, self)
                self.frames[name] = frame
            else:
                # Other frames use container with navigation bar
                container_frame = ttk.Frame(self.main_container)
                
                # Add navigation bar
                nav_frame = NavigationFrame(container_frame, self)
                nav_frame.pack(side=tk.TOP, fill=tk.X)

                # Add content frame
                content_frame = frame_class(container_frame, self)
                content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(5, 0))

                # Set controller for roommate manager
                if name == "RoommateManager":
                    content_frame.set_controller(self.roommate_controller)

                self.frames[name] = container_frame

            # Add all frames to grid but initially hide them
            self.frames[name].grid(row=0, column=0, sticky="nsew")
            self.frames[name].grid_remove()  # Initially hidden

        # Configure main container grid weights
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

    def show_frame(self, name):
        """Show the specified frame and hide the current one"""        
        # Handle current frame cleanup
        if self.current_frame:
            # Call on_show() on the content frame, not the container
            if name != "Dashboard":
                # For frames with navigation, get the content frame (second child)
                if hasattr(self.current_frame, 'winfo_children') and len(self.current_frame.winfo_children()) > 1:
                    content_frame = self.current_frame.winfo_children()[1]
                    if hasattr(content_frame, 'on_show'):
                        content_frame.on_show()
            else:
                # For Dashboard, call directly
                if hasattr(self.current_frame, 'on_show'):
                    self.current_frame.on_show()
                    
            self.current_frame.grid_remove()
        
        # Show new frame
        self.current_frame = self.frames[name]
        self.current_frame.grid()

        # Call on_show() for the new frame as well
        if name != "Dashboard":
            # For frames with navigation, get the content frame (second child)
            if hasattr(self.current_frame, 'winfo_children') and len(self.current_frame.winfo_children()) > 1:
                content_frame = self.current_frame.winfo_children()[1]
                if hasattr(content_frame, 'on_show'):
                    content_frame.on_show()
        else:
            # For Dashboard, call directly
            if hasattr(self.current_frame, 'on_show'):
                self.current_frame.on_show()

    # --- Navigation methods for navigation bar and dashboard ---
    def show_dashboard(self):
        """Show the dashboard frame"""
        self.show_frame("Dashboard")

    def show_manage_roommates(self):
        """Show the roommate management frame"""
        self.show_frame("RoommateManager")

    def show_add_expense(self):
        """Show the expense entry frame"""
        self.show_frame("ExpenseEntry")

    def show_report(self):
        """Show the report frame"""
        self.show_frame("Report")

if __name__ == "__main__":
    # Create and run the application
    root = tk.Tk()
    app = RoomieSplitApp(root)
    root.mainloop()
