import tkinter as tk
from tkinter import ttk


class DashboardFrame(ttk.Frame):
    """
    Main dashboard frame that serves as the home screen for the RoomieSplit application.
    
    Provides navigation to all major features of the application and serves as the
    central hub for users to access different functionality areas.
    """
    
    def __init__(self, parent, controller):
        """
        Initialize the DashboardFrame.
        
        Args:
            parent: The parent widget (typically the main container)
            controller: The main application controller (RoomieSplitApp instance)
        """
        super().__init__(parent)
        self.controller = controller
        
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface for the dashboard.
        
        Creates the main dashboard layout including:
        - Application title and description
        - Navigation buttons to access different features
        """
        # --- Dashboard Header Section ---
        title_label = ttk.Label(
            self, 
            text="RoomieSplit Dashboard", 
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=(10, 20))

        # Application description
        desc_label = ttk.Label(
            self, 
            text="Manage shared expenses with your roommates or track your personal budget.", 
            wraplength=400
        )
        desc_label.pack(pady=(0, 20))

        # --- Navigation Buttons Section ---
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        # Roommate Management Button
        ttk.Button(
            button_frame, 
            text="Manage Roommates", 
            command=self.controller.show_manage_roommates
        ).pack(pady=5)

        # Expense Entry Button
        ttk.Button(
            button_frame, 
            text="Add New Expense", 
            command=self.controller.show_add_expense
        ).pack(pady=5)

        # Reports Button
        ttk.Button(
            button_frame, 
            text="View Settlement Report", 
            command=self.controller.show_report
        ).pack(pady=5)

        # Note: Personal budget reports are now accessible through the ReportFrame
        # via radio button selection, not as a separate dashboard button.

    def on_manage_roommates_click(self):
        """
        Handle 'Manage Roommates' button click event.
        
        Note: This method is kept for backward compatibility but is no longer
        used directly. Navigation is now handled through the controller methods.
        """
        print("Manage Roommates button clicked")
        # Legacy method - navigation now handled by controller.show_manage_roommates()

    def on_add_expense_click(self):
        """
        Handle 'Add New Expense' button click event.
        
        Note: This method is kept for backward compatibility but is no longer
        used directly. Navigation is now handled through the controller methods.
        """
        print("Add New Expense button clicked")
        # Legacy method - navigation now handled by controller.show_add_expense()

    def on_view_report_click(self):
        """
        Handle 'View Settlement Report' button click event.
        
        Note: This method is kept for backward compatibility but is no longer
        used directly. Navigation is now handled through the controller methods.
        """
        print("View Settlement Report button clicked")
        # Legacy method - navigation now handled by controller.show_report()
