import tkinter as tk
from tkinter import ttk


class NavigationFrame(ttk.Frame):
    """
    Top navigation bar providing access to all major application features.
    
    This frame contains navigation buttons that allow users to switch between
    different sections of the RoomieSplit application. It provides consistent
    navigation across all main application screens.
    """
    
    def __init__(self, parent, controller):
        """
        Initialize the Navigation Frame.
        
        Args:
            parent: The parent widget (typically a container frame)
            controller: The main application controller (RoomieSplitApp instance)
                       used to call navigation methods
        """
        super().__init__(parent, relief="raised", borderwidth=1)
        self.controller = controller
        
        self.setup_navigation()

    def setup_navigation(self):
        """
        Set up the navigation buttons for all major application sections.
        
        Creates buttons for:
        - Dashboard (home screen)
        - Roommate management
        - Expense entry
        - Reports and analytics
        """
        # Dashboard Button - Returns to main home screen
        ttk.Button(
            self, 
            text="Dashboard", 
            command=self.controller.show_dashboard
        ).pack(side=tk.LEFT, padx=2, pady=2)

        # Roommate Management Button - Access roommate CRUD operations
        ttk.Button(
            self, 
            text="Manage Roommates", 
            command=self.controller.show_manage_roommates
        ).pack(side=tk.LEFT, padx=2, pady=2)

        # Expense Entry Button - Navigate to expense creation and management
        ttk.Button(
            self, 
            text="Add Expense", 
            command=self.controller.show_add_expense
        ).pack(side=tk.LEFT, padx=2, pady=2)

        # Reports Button - Access settlement and budget reports
        ttk.Button(
            self, 
            text="Reports", 
            command=self.controller.show_report
        ).pack(side=tk.LEFT, padx=2, pady=2)

        # Optional: Uncomment to add a "Back to Dashboard" button on the right side
        # ttk.Button(
        #     self, 
        #     text="Go to Dashboard", 
        #     command=self.controller.show_dashboard
        # ).pack(side=tk.RIGHT, padx=2, pady=2)

    def on_show(self):
        """
        Called when the frame containing this navigation bar is displayed.
        
        This method can be used to update navigation state, highlight active
        sections, or perform other navigation-related updates when needed.
        
        Currently, the navigation bar doesn't require updates when shown,
        but this method provides a hook for future enhancements.
        """
        # Navigation bar is static and doesn't require updates when shown
        # This method can be extended to:
        # - Highlight the currently active section
        # - Update navigation state based on application context
        # - Refresh navigation elements if needed
        pass