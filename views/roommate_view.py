# views/roomate_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class RoommateManagerFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.roommate_controller = None
        self.id_mapping = {}
        self.setup_ui()
        self.refresh_list()

    def setup_ui(self):
        """Setup the user interface with sorting functionality"""
        # Main layout container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add roommate section
        add_frame = ttk.LabelFrame(main_frame, text="Add New Roommate", padding=10)
        add_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(add_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.name_entry = ttk.Entry(add_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=(0, 10), pady=2)

        ttk.Label(add_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.email_entry = ttk.Entry(add_frame, width=20)
        self.email_entry.grid(row=1, column=1, padx=(0, 10), pady=2)

        ttk.Label(add_frame, text="Join Date (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.date_entry = ttk.Entry(add_frame, width=15)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.date_entry.grid(row=2, column=1, padx=(0, 10), pady=2)

        self.add_button = ttk.Button(add_frame, text="Add Roommate", command=self.add_roommate)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Search/filter section
        filter_frame = ttk.Frame(main_frame)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        search_entry.bind('<KeyRelease>', self.filter_roommates)
        
        ttk.Button(filter_frame, text="Clear Filter", command=self.clear_filter).pack(side=tk.LEFT)

        # Roommate list section
        list_frame = ttk.LabelFrame(main_frame, text="Roommate List", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Treeview for displaying roommates with sorting
        columns = ('ID', 'Name', 'Email', 'Join Date')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        
        # Configure column headings with sorting
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
        
        # Set column widths
        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('Name', width=150, anchor=tk.W)
        self.tree.column('Email', width=200, anchor=tk.W)
        self.tree.column('Join Date', width=100, anchor=tk.CENTER)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Button frame
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))

        self.edit_button = ttk.Button(button_frame, text="Edit Selected", command=self.edit_roommate)
        self.edit_button.pack(side=tk.LEFT, padx=(0, 5))
        self.delete_button = ttk.Button(button_frame, text="Delete Selected", command=self.delete_roommate)
        self.delete_button.pack(side=tk.LEFT)

        # Initialize sorting state
        self.sort_direction = {}  # Track sort direction for each column
        for col in columns:
            self.sort_direction[col] = False  # False = ascending, True = descending

    def refresh_list(self):
        """Refresh the roommate list from database with sorting support"""
        if not self.roommate_controller:
            return

        # Clear existing items
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Get roommates from controller
        success, result = self.roommate_controller.get_all_roommates()
                
        if success:
            # Store the raw data for sorting and filtering
            self.roommates_data = []
            self.id_mapping = {}  # Recreate the mapping
            
            display_number = 1
            
            for roommate in result:
                actual_id, name, email, join_date = roommate
                # Store both display values and raw values for sorting
                display_values = (display_number, name, email, join_date)
                raw_values = (actual_id, name, email, join_date, display_number)
                
                self.tree.insert('', tk.END, values=display_values)
                self.roommates_data.append((display_values, raw_values))
                self.id_mapping[display_number] = actual_id  # Store the mapping
                
                display_number += 1
            
            self.tree.update_idletasks()
        else:
            messagebox.showerror("Database Error", result)

    def sort_treeview(self, column):
        """Sort treeview by column when heading is clicked"""
        if not hasattr(self, 'roommates_data') or not self.roommates_data:
            return
        
        # Get column index
        columns = ('ID', 'Name', 'Email', 'Join Date')
        col_index = columns.index(column)
        
        # Toggle sort direction
        self.sort_direction[column] = not self.sort_direction[column]
        reverse = self.sort_direction[column]
        
        # Define sorting keys for different column types
        def get_sort_key(item):
            display_values, raw_values = item
            
            if column == 'ID':
                return raw_values[4]  # Use display number for consistent ordering
            elif column == 'Name':
                return raw_values[1].lower()  # Case-insensitive name
            elif column == 'Email':
                return raw_values[2].lower()  # Case-insensitive email
            elif column == 'Join Date':
                return raw_values[3]  # Date string (YYYY-MM-DD format sorts correctly)
            else:
                return display_values[col_index]
        
        # Sort the data
        sorted_data = sorted(self.roommates_data, key=get_sort_key, reverse=reverse)
        
        # Clear and repopulate treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        for display_values, _ in sorted_data:
            self.tree.insert('', tk.END, values=display_values)
        
        # Update column heading to show sort direction
        direction_symbol = " ↓" if reverse else " ↑"
        for col in columns:
            current_text = col
            if col == column:
                current_text += direction_symbol
            self.tree.heading(col, text=current_text)

    def filter_roommates(self, event=None):
        """Filter roommates based on search text"""
        search_text = self.search_var.get().lower()
        
        if not hasattr(self, 'roommates_data') or not self.roommates_data:
            return
        
        # Clear treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Filter and display matching roommates
        for display_values, raw_values in self.roommates_data:
            # Check if search text matches any column
            matches = any(search_text in str(value).lower() for value in display_values)
            if matches or not search_text:
                self.tree.insert('', tk.END, values=display_values)

    def clear_filter(self):
        """Clear search filter and refresh the list"""
        self.search_var.set("")
        self.refresh_list()

    def set_controller(self, roommate_controller):
        """Set the roommate controller instance"""
        self.roommate_controller = roommate_controller
        self.refresh_list()  # Refresh immediately when controller is set

    def add_roommate(self):
        """Handle add roommate button click"""
        if not self.roommate_controller:
            messagebox.showerror("Error", "Controller not initialized")
            return

        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        join_date = self.date_entry.get().strip()

        # Validate inputs
        if not name:
            messagebox.showerror("Input Error", "Name is required.")
            return

        if not self.roommate_controller.validate_email(email):
            messagebox.showerror("Input Error", "Please enter a valid email address.")
            return
        
        try:
            datetime.strptime(join_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Input Error", "Join date format should be YYYY-MM-DD.")
            return

        # Call controller to add roommate
        success, message = self.roommate_controller.add_roommate(name, email, join_date)
        
        if success:
            self.refresh_list()
            self.clear_add_form()
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def create_edit_dialog(self, roommate_id, current_name, current_email, current_join_date):
        """Create a dialog for editing roommate information"""
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Roommate")
        edit_window.geometry("350x200")
        edit_window.transient(self)
        edit_window.grab_set()
        
        ttk.Label(edit_window, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(edit_window, width=20)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        name_entry.insert(0, current_name)
        
        ttk.Label(edit_window, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        email_entry = ttk.Entry(edit_window, width=20)
        email_entry.grid(row=1, column=1, padx=5, pady=5)
        email_entry.insert(0, current_email)
        
        # Join date field
        ttk.Label(edit_window, text="Join Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        date_entry = ttk.Entry(edit_window, width=15)
        date_entry.grid(row=2, column=1, padx=5, pady=5)
        date_entry.insert(0, current_join_date)
        
        def save_changes():
            new_name = name_entry.get().strip()
            new_email = email_entry.get().strip()
            new_join_date = date_entry.get().strip()
            
            if not new_name:
                messagebox.showerror("Input Error", "Name is required.")
                return

            if not self.roommate_controller.validate_email(new_email):
                messagebox.showerror("Input Error", "Please enter a valid email address.")
                return
            
            # Validate date format
            try:
                datetime.strptime(new_join_date, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Input Error", "Join date format should be YYYY-MM-DD.")
                return
            
            # Call controller to update roommate with join date
            success, message = self.roommate_controller.update_roommate(
                roommate_id, new_name, new_email, new_join_date
            )
            
            if success:
                messagebox.showinfo("Success", message)
                edit_window.destroy()
                self.refresh_list()
            else:
                messagebox.showerror("Error", message)
        
        ttk.Button(edit_window, text="Save", command=save_changes).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(edit_window, text="Cancel", command=edit_window.destroy).grid(row=4, column=0, columnspan=2)

    def delete_roommate(self):
        """Handle delete roommate button click"""
        if not self.roommate_controller:
            messagebox.showerror("Error", "Controller not initialized")
            return

        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Selection Error", "Please select at least one roommate to delete.")
            return

        # Get roommate names and actual IDs for confirmation message
        roommate_names = []
        roommate_ids = []
        
        for item in selected_items:
            item_values = self.tree.item(item)['values']
            display_number = item_values[0]
            
            if not hasattr(self, 'id_mapping') or display_number not in self.id_mapping:
                messagebox.showerror("Error", f"Could not find database ID for display number {display_number}. Please refresh the list.")
                return
                
            actual_id = self.id_mapping[display_number]
            roommate_name = item_values[1]
            roommate_names.append(roommate_name)
            roommate_ids.append(actual_id)

        # Create confirmation message
        if len(roommate_names) == 1:
            confirm_msg = f"Are you sure you want to delete '{roommate_names[0]}'?\n\nNote: This will fail if the roommate has expenses associated with them."
        else:
            confirm_msg = f"Are you sure you want to delete {len(roommate_names)} roommates?\n\nNote: This will fail for any roommate who has expenses associated with them.\n\n" + "\n".join([f"• {name}" for name in roommate_names])

        confirm = messagebox.askyesno("Confirm Delete", confirm_msg)

        if confirm:
            success_count = 0
            error_messages = []
            
            for roommate_id, roommate_name in zip(roommate_ids, roommate_names):
                try:
                    # Call controller to delete roommate
                    success, message = self.roommate_controller.delete_roommate(roommate_id)
                    
                    if success:
                        success_count += 1
                    else:
                        error_messages.append(f"Failed to delete '{roommate_name}': {message}")
                except Exception as e:
                    if "foreign key constraint" in str(e).lower():
                        error_messages.append(f"Cannot delete '{roommate_name}': This roommate has expenses associated with them. Please reassign or delete their expenses first.")
                    else:
                        error_messages.append(f"Failed to delete '{roommate_name}': {str(e)}")

            # Show results
            if success_count == len(roommate_ids):
                if len(roommate_ids) == 1:
                    messagebox.showinfo("Success", f"Roommate '{roommate_names[0]}' deleted successfully.")
                else:
                    messagebox.showinfo("Success", f"All {success_count} roommates deleted successfully.")
            elif success_count > 0:
                partial_message = f"Deleted {success_count} of {len(roommate_ids)} roommates."
                if error_messages:
                    partial_message += "\n\nErrors:\n" + "\n".join(error_messages)
                messagebox.showwarning("Partial Success", partial_message)
            else:
                error_message = "Failed to delete all roommates:\n" + "\n".join(error_messages)
                messagebox.showerror("Error", error_message)
            
            self.refresh_list()

    def clear_add_form(self):
        """Clear the add roommate form and reset to default values"""
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))  # Reset to today

    def edit_roommate(self):
        """Handle edit roommate button click"""
        if not self.roommate_controller:
            messagebox.showerror("Error", "Controller not initialized")
            return

        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a roommate to edit.")
            return

        item_values = self.tree.item(selected_item)['values']
        roommate_id = item_values[0]
        current_name = item_values[1]
        current_email = item_values[2]
        current_join_date = item_values[3]
        
        # Create edit dialog
        self.create_edit_dialog(roommate_id, current_name, current_email, current_join_date)

    def on_show(self):
        """Called when this interface is shown, used to refresh data"""
        self.refresh_list()
        self.clear_add_form()
