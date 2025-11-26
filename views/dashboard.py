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
        # Configure the main frame's padding
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Welcome Message Section ---
        welcome_frame = ttk.Frame(self)
        welcome_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 0))

        title_label = ttk.Label(
            welcome_frame,
            text="Welcome to RoomieSplit!",
            font=('Arial', 20, 'bold') # Larger, bolder title
        )
        title_label.pack(pady=(0, 5))

        subtitle_label = ttk.Label(
            welcome_frame,
            text="Your shared living costs, simplified.",
            font=('Arial', 12, 'italic'), # Subtle subtitle
            foreground='gray60' # Lighter color
        )
        subtitle_label.pack(pady=(0, 10))

        # --- Description Section ---
        desc_frame = ttk.Frame(self)
        desc_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        desc_label = ttk.Label(
            desc_frame,
            text="Track shared expenses, manage budgets, and settle up easily with your roommates.",
            font=('Arial', 11),
            wraplength=500, # Wrap text within a specific width
            justify='center' # Center-align the text
        )
        desc_label.pack(expand=True) # Allow label to expand within its frame

        # --- Navigation Buttons Section ---
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)

        # Define button styles (these can be configured in main.py or here if needed)
        # For ttkbootstrap themes, these styles are often handled by the theme itself.
        # Using standard ttk styles here for compatibility.

        # Roommate Management Button
        ttk.Button(
            button_frame,
            text="Manage Roommates",
            command=self.controller.show_manage_roommates,
            style='Accent.TButton'  # Use accent style if available (e.g., from ttkbootstrap theme)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Expense Entry Button
        ttk.Button(
            button_frame,
            text="Add New Expense",
            command=self.controller.show_add_expense,
            style='Accent.TButton' # Use accent style if available
        ).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Reports Button
        ttk.Button(
            button_frame,
            text="View Reports",
            command=self.controller.show_report,
            style='Accent.TButton' # Use accent style if available
        ).grid(row=0, column=2, padx=5, pady=5, sticky="ew")

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
