import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class ExpenseEntryFrame(ttk.Frame):
    """
    Expense Entry Frame for adding and managing expense records.

    This frame provides:
    - Form for entering new expenses with validation
    - Interactive expense history list with sorting and filtering
    - Multi-select participant functionality
    - Bulk expense deletion capabilities
    """

    def __init__(self, parent, controller):
        """
        Initialize the Expense Entry Frame.

        Args:
            parent: The parent widget
            controller: The main application controller
        """
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
        self.refresh_roommates_list()
        self.refresh_history_list()

    def setup_ui(self):
        """
        Set up the complete user interface for expense management.

        Creates:
        - Expense entry form with validation
        - Search and filter functionality
        - Sortable expense history table
        - Action buttons for expense management
        """
        # --- Main Container ---
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Expense Entry Form Section ---
        input_frame = ttk.LabelFrame(main_frame, text="Enter Expense Details", padding=10)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        # Configure grid weights for input frame to align elements nicely
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)

        # Amount Field
        ttk.Label(input_frame, text="Amount ($):").grid(row=0, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.amount_entry = ttk.Entry(input_frame, width=15)
        self.amount_entry.grid(row=0, column=1, padx=(0, 10), pady=2, sticky=tk.EW)

        # Date Field (defaults to today)
        ttk.Label(input_frame, text="Date:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5), pady=2)
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.date_entry.grid(row=0, column=3, padx=(0, 10), pady=2, sticky=tk.EW)

        # Category Selection
        ttk.Label(input_frame, text="Category:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.category_combo = ttk.Combobox(
            input_frame,
            values=["Rent", "Utilities", "Groceries", "Dining Out", "Entertainment", "Other"],
            state="readonly",
            width=13
        )
        self.category_combo.set("Other")
        self.category_combo.grid(row=1, column=1, padx=(0, 10), pady=2, sticky=tk.EW)

        # Payer Selection (populated from database)
        ttk.Label(input_frame, text="Paid By:").grid(row=1, column=2, sticky=tk.W, padx=(0, 5), pady=2)
        self.payer_combo = ttk.Combobox(input_frame, values=[], state="readonly", width=15)
        self.payer_combo.grid(row=1, column=3, padx=(0, 10), pady=2, sticky=tk.EW)

        # Multi-select Participants
        ttk.Label(input_frame, text="Participants:").grid(row=2, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.participant_vars = {}  # Stores checkbox variables for participant selection
        self.participant_frame = ttk.Frame(input_frame)
        self.participant_frame.grid(row=2, column=1, columnspan=3, sticky=tk.W, padx=(0, 10), pady=2)

        # Add Expense Button
        self.add_button = ttk.Button(main_frame, text="Add Expense", command=self.add_expense)
        self.add_button.pack(pady=10)

        # --- Search and Filter Section ---
        filter_frame = ttk.Frame(main_frame)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(filter_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        search_entry.bind('<KeyRelease>', self.filter_expenses)

        ttk.Button(filter_frame, text="Clear Filter", command=self.clear_filter).pack(side=tk.LEFT)

        # --- Expense History Section ---
        history_frame = ttk.LabelFrame(main_frame, text="Expense History", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Configure sortable treeview columns
        columns = ('ID', 'Amount', 'Date', 'Category', 'Paid By', 'Participants')
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=8)

        # Make column headings clickable for sorting
        for col in columns:
            self.history_tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            # Set default column width (can be adjusted)
            self.history_tree.column(col, width=100, anchor=tk.W)

        # Scrollbar for expense history
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscroll=scrollbar.set)

        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Action Buttons for Expense Management
        button_frame = ttk.Frame(history_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))

        self.edit_button = ttk.Button(button_frame, text="Edit Selected", command=self.edit_expense)
        self.edit_button.pack(side=tk.LEFT, padx=(0, 5))
        self.delete_button = ttk.Button(button_frame, text="Delete Selected", command=self.delete_expense)
        self.delete_button.pack(side=tk.LEFT)

        # Initialize sorting state for all columns
        self.sort_direction = {}
        for col in columns:
            self.sort_direction[col] = False  # False = ascending, True = descending

    def refresh_history_list(self):
        """
        Refresh the expense history list from the database.

        Loads all expenses, formats them for display, and stores raw data
        for sorting and filtering operations.
        """
        # Clear existing items from treeview
        for i in self.history_tree.get_children():
            self.history_tree.delete(i)

        try:
            from models.database.expense_db import get_all_expenses, get_expense_participants
            from models.database.roomate_db import get_roommate_by_id, get_all_roommates

            # Load expenses and roommate data
            expenses = get_all_expenses()
            all_roommates = get_all_roommates()
            total_roommates = len(all_roommates)

            # Store raw data for sorting and filtering
            self.expenses_data = []

            # Process each expense for display
            for exp in expenses:
                expense_id = exp[0]
                date = exp[1]
                category = exp[3]
                amount = exp[4]
                payer_id = exp[6]

                # Get payer name for display
                payer_name = "Unknown"
                if payer_id:
                    roommate = get_roommate_by_id(payer_id)
                    if roommate:
                        payer_name = roommate[1]

                # Get participant information
                participants_data = get_expense_participants(expense_id)
                if participants_data:
                    participant_names = [p[1] for p in participants_data]

                    # Show "All" if all roommates are participants
                    if len(participants_data) == total_roommates:
                        participants_str = "All"
                    else:
                        participants_str = ", ".join(participant_names)
                else:
                    participants_str = "None"

                # Format amount for display
                formatted_amount = f"${amount:.2f}"

                # Store both display and raw values for sorting
                display_values = (expense_id, formatted_amount, date, category, payer_name, participants_str)
                raw_values = (expense_id, amount, date, category, payer_name, participants_str, expense_id)

                self.history_tree.insert('', tk.END, values=display_values)
                self.expenses_data.append((display_values, raw_values))

        except Exception as e:
            print(f"Error loading expenses: {e}")
            messagebox.showerror("Database Error", f"Failed to load expense history: {str(e)}")

    def sort_treeview(self, column):
        """
        Sort the expense history by the specified column.

        Args:
            column (str): The column name to sort by
        """
        if not hasattr(self, 'expenses_data') or not self.expenses_data:
            return

        # Get column index and toggle sort direction
        columns = ('ID', 'Amount', 'Date', 'Category', 'Paid By', 'Participants')
        col_index = columns.index(column)
        self.sort_direction[column] = not self.sort_direction[column]
        reverse = self.sort_direction[column]

        def get_sort_key(item):
            """Define sorting keys for different column types."""
            display_values, raw_values = item

            if column == 'ID':
                return raw_values[0]  # Use raw ID
            elif column == 'Amount':
                return raw_values[1]  # Use raw amount (float)
            elif column == 'Date':
                return raw_values[2]  # Use date string
            elif column == 'Category':
                return raw_values[3].lower()  # Case-insensitive
            elif column == 'Paid By':
                return raw_values[4].lower()  # Case-insensitive
            elif column == 'Participants':
                return raw_values[5].lower()  # Case-insensitive
            else:
                return display_values[col_index]

        # Sort data and refresh display
        sorted_data = sorted(self.expenses_data, key=get_sort_key, reverse=reverse)

        for i in self.history_tree.get_children():
            self.history_tree.delete(i)

        for display_values, _ in sorted_data:
            self.history_tree.insert('', tk.END, values=display_values)

        # Update column headings to show sort direction
        direction_symbol = " ↓" if reverse else " ↑"
        for col in columns:
            current_text = col
            if col == column:
                current_text += direction_symbol
            self.history_tree.heading(col, text=current_text)

    def filter_expenses(self, event=None):
        """
        Filter expenses based on search text.

        Args:
            event: Key release event (unused)
        """
        search_text = self.search_var.get().lower()

        if not hasattr(self, 'expenses_data') or not self.expenses_data:
            return

        # Clear and repopulate with filtered results
        for i in self.history_tree.get_children():
            self.history_tree.delete(i)

        for display_values, raw_values in self.expenses_data:
            # Check if search text matches any column
            matches = any(search_text in str(value).lower() for value in display_values)
            if matches or not search_text:
                self.history_tree.insert('', tk.END, values=display_values)

    def clear_filter(self):
        """Clear the search filter and refresh the expense list."""
        self.search_var.set("")
        self.refresh_history_list()

    def refresh_roommates_list(self):
        """
        Refresh the roommate list from the database.

        Updates the payer dropdown and participant checkboxes with current
        roommate data.
        """
        try:
            from models.database.roomate_db import get_all_roommates

            # Load current roommates from database
            self.roommates_list = []
            roommates_data = get_all_roommates()

            # Process roommate data
            for rm in roommates_data:
                self.roommates_list.append({"id": rm[0], "name": rm[1]})

            # Update payer dropdown
            payer_names = [rm['name'] for rm in self.roommates_list]
            self.payer_combo['values'] = payer_names
            if payer_names:
                self.payer_combo.set(payer_names[0])

            # Recreate participant checkboxes
            for widget in self.participant_frame.winfo_children():
                widget.destroy()

            self.participant_vars = {}
            for rm in self.roommates_list:
                var = tk.BooleanVar()
                chk = ttk.Checkbutton(self.participant_frame, text=rm['name'], variable=var)
                chk.pack(side=tk.LEFT, padx=5)
                self.participant_vars[rm['id']] = var

            # Default to selecting all participants
            for var in self.participant_vars.values():
                var.set(True)

        except Exception as e:
            print(f"Error loading roommates: {e}")
            messagebox.showerror("Database Error", f"Failed to load roommates: {str(e)}")

    def add_expense(self):
        """
        Add a new expense to the database with validation.

        Validates all input fields, creates the expense record, and adds
        participant associations.
        """
        # Get form data
        amount_str = self.amount_entry.get().strip()
        date_str = self.date_entry.get().strip()
        category = self.category_combo.get()
        payer_name = self.payer_combo.get()

        # Validate amount
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid positive amount.")
            return

        # Validate at least one participant selected
        selected_participant_ids = [rm_id for rm_id, var in self.participant_vars.items() if var.get()]
        if not selected_participant_ids:
            messagebox.showerror("Input Error", "At least one participant must be selected.")
            return

        # Validate date format
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Input Error", "Date format should be YYYY-MM-DD.")
            return

        # Find payer ID and validate
        payer_id = None
        for rm in self.roommates_list:
            if rm['name'] == payer_name:
                payer_id = rm['id']
                break

        if payer_id is None:
            messagebox.showerror("Input Error", "Selected payer is not in the roommate list.")
            return

        # Ensure payer is included in participants
        if payer_id not in selected_participant_ids:
            messagebox.showerror("Input Error", "The payer must be included in the participants.")
            return

        try:
            from models.database.expense_db import add_expense, add_expense_participants

            # Create expense record
            expense_id = add_expense(
                date=date_str,
                account="",
                category=category,
                amount=amount,
                note="",
                payer_id=payer_id
            )

            # Add participant associations
            add_expense_participants(expense_id, selected_participant_ids)

            # Refresh UI and reset form
            self.refresh_history_list()
            self.clear_form()
            messagebox.showinfo("Success", "Expense added successfully.")

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to add expense: {str(e)}")

    def edit_expense(self):
        """
        Placeholder for expense editing functionality.

        Note: This feature is not yet implemented.
        """
        selected_item = self.history_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an expense to edit.")
            return
        messagebox.showinfo("Info", "Edit functionality for expense would be implemented here.")

    def delete_expense(self):
        """
        Delete selected expenses from the database.

        Supports multiple expense selection and provides confirmation
        before deletion.
        """
        selected_items = self.history_tree.selection()
        if not selected_items:
            messagebox.showwarning("Selection Error", "Please select at least one expense to delete.")
            return

        # Collect expense details for confirmation
        expense_details = []
        expense_ids = []

        for item in selected_items:
            item_values = self.history_tree.item(item)['values']
            expense_id = item_values[0]
            amount = item_values[1]
            date = item_values[2]
            category = item_values[3]
            expense_details.append(f"ID {expense_id}: {amount} on {date} ({category})")
            expense_ids.append(expense_id)

        # Create confirmation message
        if len(expense_details) == 1:
            confirm_msg = f"Are you sure you want to delete this expense?\n{expense_details[0]}"
        else:
            confirm_msg = f"Are you sure you want to delete {len(expense_details)} expenses?\n" + "\n".join([f"• {detail}" for detail in expense_details])

        confirm = messagebox.askyesno("Confirm Delete", confirm_msg)

        if confirm:
            success_count = 0
            error_messages = []

            # Delete each selected expense
            for expense_id in expense_ids:
                try:
                    from models.database.expense_db import delete_expense
                    success = delete_expense(expense_id)

                    if success:
                        success_count += 1
                    else:
                        error_messages.append(f"Failed to delete expense ID {expense_id}")

                except Exception as e:
                    error_messages.append(f"Error deleting expense ID {expense_id}: {str(e)}")

            # Show operation results
            if success_count == len(expense_ids):
                if len(expense_ids) == 1:
                    messagebox.showinfo("Success", f"Expense deleted successfully.")
                else:
                    messagebox.showinfo("Success", f"All {success_count} expenses deleted successfully.")
            elif success_count > 0:
                partial_message = f"Deleted {success_count} of {len(expense_ids)} expenses."
                if error_messages:
                    partial_message += "\n\nErrors:\n" + "\n".join(error_messages)
                messagebox.showwarning("Partial Success", partial_message)
            else:
                error_message = "Failed to delete all expenses:\n" + "\n".join(error_messages)
                messagebox.showerror("Error", error_message)

            self.refresh_history_list()

    def clear_form(self):
        """Reset the expense entry form to default values."""
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.category_combo.set("Other")
        if self.payer_combo['values']:
            self.payer_combo.set(self.payer_combo['values'][0])
        for var in self.participant_vars.values():
            var.set(True)  # Default to selecting all participants

    def on_show(self):
        """
        Refresh data when this frame is displayed.

        Called by the navigation system when switching to this frame.
        """
        self.refresh_roommates_list()
        self.refresh_history_list()
        self.clear_form()
