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
        super().__init__(parent, relief="groove", borderwidth=1) # Changed to 'groove' for a more defined look with 'clam' theme
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
        # Configure the frame's internal grid to distribute buttons evenly
        # There are 4 buttons, so we configure 4 columns with equal weight
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

        # Dashboard Button - Returns to main home screen
        dashboard_btn = ttk.Button(
            self,
            text="Dashboard",
            command=self.controller.show_dashboard
        )
        dashboard_btn.grid(row=0, column=0, padx=2, pady=2, sticky="ew")

        # Roommate Management Button - Access roommate CRUD operations
        roommate_btn = ttk.Button(
            self,
            text="Manage Roommates",
            command=self.controller.show_manage_roommates
        )
        roommate_btn.grid(row=0, column=1, padx=2, pady=2, sticky="ew")

        # Expense Entry Button - Navigate to expense creation and management
        expense_btn = ttk.Button(
            self,
            text="Add Expense",
            command=self.controller.show_add_expense
        )
        expense_btn.grid(row=0, column=2, padx=2, pady=2, sticky="ew")

        # Reports Button - Access settlement and budget reports
        reports_btn = ttk.Button(
            self,
            text="Reports",
            command=self.controller.show_report
        )
        reports_btn.grid(row=0, column=3, padx=2, pady=2, sticky="ew")

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
