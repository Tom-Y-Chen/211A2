import tkinter as tk
from tkinter import ttk
from ui.dashboard import DashboardFrame # Import dashboard interface
# Additional interfaces can be imported later, for example:
# from ui.expense_ui import ExpenseEntryFrame
# from ui.report_ui import ReportFrame

class RoomieSplitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RoomieSplit - Expense Tracker")
        self.root.geometry("800x600") # Set initial window size
        self.root.minsize(600, 400) # Set minimum window size

        # --- Style configuration ---
        self.style = ttk.Style()
        # For example, set default fonts
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TEntry', font=('Arial', 10))
        self.style.configure('TCombobox', font=('Arial', 10))
        # More style configuration can be added

        # --- Main container ---
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Initialize and display main dashboard ---
        self.current_frame = None
        self.show_dashboard()

    def show_dashboard(self):
        """Display the main dashboard interface"""
        self._hide_current_frame()
        self.current_frame = DashboardFrame(self.main_container, self) # Pass self (RoomieSplitApp instance) to DashboardFrame
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def _hide_current_frame(self):
        """Hide the currently displayed frame"""
        if self.current_frame:
            self.current_frame.pack_forget()

    # Additional methods like show_expense_entry and show_report can be added
    # for switching to other views

if __name__ == "__main__":
    root = tk.Tk()
    app = RoomieSplitApp(root)
    root.mainloop()