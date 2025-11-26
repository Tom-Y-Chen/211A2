# views/report_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.database.expense_db import get_all_expenses
from models.database.roomate_db import get_all_roommates
from models.report_generator import (
    generate_settlement_report,
    generate_personal_budget_report,
    generate_summary_report
)


class ReportFrame(ttk.Frame):
    """
    Report Generation Frame for financial analysis and reporting.

    This frame provides access to various financial reports including:
    - Settlement reports (who owes whom)
    - Summary reports (overall financial overview)
    - Personal budget reports (individual spending by category)
    """

    def __init__(self, parent, controller):
        """
        Initialize the Report Frame.

        Args:
            parent: The parent widget
            controller: The main application controller
        """
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface for report generation.

        Creates:
        - Report type selection buttons
        - Personal budget report controls with roommate selection
        - Results display area for generated reports
        """
        # --- Main Container ---
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Report Selection Section ---
        report_frame = ttk.LabelFrame(main_frame, text="Generate Reports", padding=10)
        report_frame.pack(fill=tk.X, padx=5, pady=5)

        # Configure grid for even button distribution
        report_frame.grid_columnconfigure(0, weight=1)
        report_frame.grid_columnconfigure(1, weight=1)
        report_frame.grid_columnconfigure(2, weight=1)

        # Settlement Report Button - Shows who owes money to whom
        ttk.Button(
            report_frame,
            text="Settlement Report",
            command=self.generate_settlement_report
        ).grid(row=0, column=0, padx=5, pady=2, sticky="ew")

        # Summary Report Button - Shows overall financial overview
        ttk.Button(
            report_frame,
            text="Summary Report",
            command=self.generate_summary_report
        ).grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        # --- Personal Budget Report Section ---
        ttk.Label(
            report_frame,
            text="Personal Budget for:"
        ).grid(row=0, column=2, sticky=tk.W, padx=(20, 5), pady=2)

        # Roommate selection for personal budget reports
        self.roommate_combo = ttk.Combobox(report_frame, state="readonly", width=15)
        self.roommate_combo.grid(row=0, column=3, padx=5, pady=2, sticky="ew")

        # Generate personal budget report button
        ttk.Button(
            report_frame,
            text="Generate",
            command=self.generate_personal_report
        ).grid(row=0, column=4, padx=5, pady=2)

        # Configure the column for the combo box to expand
        report_frame.grid_columnconfigure(3, weight=1)

        # --- Report Results Display Area ---
        self.results_frame = ttk.LabelFrame(main_frame, text="Report Results", padding=10)
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Load available roommates for personal budget reports
        self.refresh_roommates()

    def refresh_roommates(self):
        """
        Refresh the list of roommates for the personal budget report dropdown.

        Loads all roommates from the database and populates the selection
        combo box. Sets the first roommate as the default selection.
        """
        try:
            roommates = get_all_roommates()
            # Assuming get_all_roommates returns [(id, name, email, join_date), ...]
            # Extract names for the combobox
            roommate_names = [rm[1] for rm in roommates]  # rm[1] = name
            self.roommate_combo['values'] = roommate_names

            # Set default selection if roommates exist
            if roommate_names:
                self.roommate_combo.set(roommate_names[0])

        except Exception as e:
            print(f"Error loading roommates for report: {e}") # Log the error
            messagebox.showerror("Error", f"Failed to load roommates: {e}")

    def generate_settlement_report(self):
        """
        Generate and display the settlement report.

        Shows financial settlements between roommates - who owes money to whom
        based on expense history and fair share calculations.
        """
        try:
            expenses = get_all_expenses()
            roommates = get_all_roommates()
            report_data = generate_settlement_report(expenses, roommates)
            self.display_report("Settlement Report", report_data)

        except Exception as e:
            print(f"Error generating settlement report: {e}") # Log the error
            messagebox.showerror("Error", f"Failed to generate settlement report: {e}")

    def generate_summary_report(self):
        """
        Generate and display the summary report.

        Provides an overview of household finances including:
        - Total household expenses
        - Individual contributions (actual payments)
        - Individual fair shares (theoretical amounts owed)
        """
        try:
            expenses = get_all_expenses()
            roommates = get_all_roommates()
            report_data = generate_summary_report(expenses, roommates)
            self.display_summary_report(report_data)

        except Exception as e:
            print(f"Error generating summary report: {e}") # Log the error
            messagebox.showerror("Error", f"Failed to generate summary report: {e}")

    def generate_personal_report(self):
        """
        Generate and display a personal budget report for the selected roommate.

        Shows spending breakdown by category for an individual roommate,
        helping them understand their personal spending patterns.
        """
        try:
            selected_name = self.roommate_combo.get()
            if not selected_name:
                messagebox.showwarning("Selection Error", "Please select a roommate.")
                return

            expenses = get_all_expenses()
            roommates = get_all_roommates()

            # Find roommate ID from selected name
            roommate_id = None
            for rm in roommates:
                if rm[1] == selected_name:  # rm[1] = name
                    roommate_id = rm[0]     # rm[0] = id
                    break

            if roommate_id is None:
                messagebox.showerror("Error", "Selected roommate not found.")
                return

            # Generate and display personal budget report
            report_data = generate_personal_budget_report(expenses, roommates, roommate_id)
            self.display_report(f"Personal Budget - {selected_name}", report_data)

        except Exception as e:
            print(f"Error generating personal report: {e}") # Log the error
            messagebox.showerror("Error", f"Failed to generate personal report: {e}")

    def display_report(self, title, data):
        """
        Display tabular report data in a treeview widget.

        Args:
            title (str): The report title to display
            data (list): List of dictionaries containing report data
        """
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Display report title
        ttk.Label(
            self.results_frame,
            text=title,
            font=('Arial', 12, 'bold')
        ).pack(pady=5)

        # Handle empty data case
        if not data:
            ttk.Label(self.results_frame, text="No data available").pack(pady=10)
            return

        # Create treeview for tabular data display
        if data:
            columns = list(data[0].keys())
        else:
            columns = [] # Handle empty data case gracefully

        tree = ttk.Treeview(self.results_frame, columns=columns, show='headings', height=10)

        # Configure column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150) # Adjust width as needed

        # Populate with data
        for row in data:
            tree.insert('', tk.END, values=list(row.values()))

        # Add scrollbar for large datasets
        scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def display_summary_report(self, summary_data):
        """
        Display summary report data in a formatted label-based layout.

        Summary reports use a different display format than tabular reports
        to better present overview information.

        Args:
            summary_data (dict): Dictionary containing summary report information
        """
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Display report title
        ttk.Label(
            self.results_frame,
            text="Summary Report",
            font=('Arial', 12, 'bold')
        ).pack(pady=5)

        # Create content frame for formatted display
        content_frame = ttk.Frame(self.results_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Total Household Expenses
        ttk.Label(
            content_frame,
            text=f"Total Household Expenses: {summary_data.get('total_household_expenses', 'N/A')}",
            font=('Arial', 10, 'bold')
        ).pack(anchor=tk.W, pady=2)

        # Individual Contributions Section
        ttk.Label(
            content_frame,
            text="Individual Contributions:",
            font=('Arial', 10, 'bold')
        ).pack(anchor=tk.W, pady=(10, 5))

        for name, amount in summary_data.get('individual_contributions', {}).items():
            ttk.Label(content_frame, text=f"  {name}: {amount}").pack(anchor=tk.W)

        # Individual Fair Shares Section
        ttk.Label(
            content_frame,
            text="Individual Fair Shares:",
            font=('Arial', 10, 'bold')
        ).pack(anchor=tk.W, pady=(10, 5))

        for name, amount in summary_data.get('individual_fair_shares', {}).items():
            ttk.Label(content_frame, text=f"  {name}: {amount}").pack(anchor=tk.W)

    def on_show(self):
        """
        Refresh data when this frame is displayed.

        Called by the navigation system when switching to the reports frame.
        Ensures roommate list is current for personal budget reports.
        """
        self.refresh_roommates()