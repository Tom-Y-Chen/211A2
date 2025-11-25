"""
main.py
Entry point for the RoomieSplit application.
Initializes the database, controllers, and launches the Tkinter UI.
"""

import tkinter as tk

from controllers.app_controller import AppController
from models.database.db_connection import initialize_database


def main():
    """
    Application startup sequence:
    - Initialize the SQLite database & tables
    - Create the Tkinter root window
    - Create the master AppController
    - Start the main Tk loop
    """

    # 1. Initialize database (creates tables if not exist)
    initialize_database()

    # 2. Start Tkinter root window
    root = tk.Tk()
    root.title("RoomieSplit — Shared Expense Manager")
    root.geometry("900x600")

    # 3. Create the master controller (which loads the first view)
    app = AppController(root)
    app.launch_dashboard()  # or app.show_login() if you add login later

    # 4. Tkinter loop
    root.mainloop()


if __name__ == "__main__":
    main()
