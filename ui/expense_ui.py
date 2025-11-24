import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
# 假设您已经创建了 models.expense 和 utils.validators
# from models.expense import Expense
# from utils.validators import validate_amount # 示例验证器

class ExpenseEntryFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # self.db = controller.db # 假设 controller 有数据库实例
        # self.roommates_list = controller.get_roommates_list() # 获取室友列表用于下拉框

        # --- 布局容器 ---
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- 输入区域 ---
        input_frame = ttk.LabelFrame(main_frame, text="Enter Expense Details", padding=10)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        # 金额
        ttk.Label(input_frame, text="Amount ($):").grid(row=0, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.amount_entry = ttk.Entry(input_frame, width=15)
        self.amount_entry.grid(row=0, column=1, padx=(0, 10), pady=2)

        # 日期
        ttk.Label(input_frame, text="Date:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5), pady=2)
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d')) # 默认为今天
        self.date_entry.grid(row=0, column=3, padx=(0, 10), pady=2)

        # 类别
        ttk.Label(input_frame, text="Category:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.category_combo = ttk.Combobox(input_frame, values=["Rent", "Utilities", "Groceries", "Dining Out", "Entertainment", "Other"], state="readonly", width=13)
        self.category_combo.set("Other") # 默认值
        self.category_combo.grid(row=1, column=1, padx=(0, 10), pady=2)

        # 支付者
        ttk.Label(input_frame, text="Paid By:").grid(row=1, column=2, sticky=tk.W, padx=(0, 5), pady=2)
        self.payer_combo = ttk.Combobox(input_frame, values=[], state="readonly", width=15) # 值将在加载时填充
        self.payer_combo.grid(row=1, column=3, padx=(0, 10), pady=2)

        # 参与者 (多选)
        ttk.Label(input_frame, text="Participants:").grid(row=2, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.participant_vars = {} # 用于存储复选框变量
        self.participant_frame = ttk.Frame(input_frame)
        self.participant_frame.grid(row=2, column=1, columnspan=3, sticky=tk.W, padx=(0, 10), pady=2)

        # 添加费用按钮
        self.add_button = ttk.Button(main_frame, text="Add Expense", command=self.add_expense)
        self.add_button.pack(pady=10)

        # --- 费用历史列表区域 ---
        history_frame = ttk.LabelFrame(main_frame, text="Expense History", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = ('ID', 'Amount', 'Date', 'Category', 'Paid By', 'Participants')
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=8)
        for col in columns:
            self.history_tree.heading(col, text=col)
            # 设置列宽 (可以根据需要调整)
            self.history_tree.column(col, width=100, anchor=tk.W)

        # 滚动条
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscroll=scrollbar.set)

        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 按钮框架
        button_frame = ttk.Frame(history_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))

        self.edit_button = ttk.Button(button_frame, text="Edit Selected", command=self.edit_expense)
        self.edit_button.pack(side=tk.LEFT, padx=(0, 5))
        self.delete_button = ttk.Button(button_frame, text="Delete Selected", command=self.delete_expense)
        self.delete_button.pack(side=tk.LEFT)

        # 加载初始数据和室友列表
        self.refresh_roommates_list()
        self.refresh_history_list()

    def refresh_roommates_list(self):
        # --- 后端集成点 ---
        # 这里应该从数据库获取室友列表
        # self.roommates_list = self.db.get_all_roommates()

        # --- 模拟后端逻辑 ---
        self.roommates_list = [
            {"id": 1, "name": "Alice Johnson"},
            {"id": 2, "name": "Bob Smith"},
            {"id": 3, "name": "Charlie Brown"},
        ]

        # 更新支付者下拉框
        payer_names = [rm['name'] for rm in self.roommates_list]
        self.payer_combo['values'] = payer_names
        if payer_names:
            self.payer_combo.set(payer_names[0]) # 默认选择第一个

        # 重新创建参与者复选框
        for widget in self.participant_frame.winfo_children():
            widget.destroy()

        self.participant_vars = {}
        for rm in self.roommates_list:
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(self.participant_frame, text=rm['name'], variable=var)
            chk.pack(side=tk.LEFT, padx=5)
            self.participant_vars[rm['id']] = var
        # 默认全选
        for var in self.participant_vars.values():
             var.set(True)


    def add_expense(self):
        amount_str = self.amount_entry.get().strip()
        date_str = self.date_entry.get().strip()
        category = self.category_combo.get()
        payer_name = self.payer_combo.get()

        # --- 后端集成点 ---
        # 验证金额
        # try:
        #     amount = float(amount_str)
        #     if amount <= 0:
        #         raise ValueError("Amount must be positive")
        # except ValueError:
        #     messagebox.showerror("Input Error", "Please enter a valid positive amount.")
        #     return

        # 获取参与者ID列表
        selected_participant_ids = [rm_id for rm_id, var in self.participant_vars.items() if var.get()]
        if not selected_participant_ids:
            messagebox.showerror("Input Error", "At least one participant must be selected.")
            return

        # 验证日期格式
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Input Error", "Date format should be YYYY-MM-DD.")
            return

        # 验证支付者是否在参与者中
        payer_id = None
        for rm in self.roommates_list:
            if rm['name'] == payer_name:
                payer_id = rm['id']
                break

        if payer_id is None:
            messagebox.showerror("Input Error", "Selected payer is not in the roommate list.")
            return

        if payer_id not in selected_participant_ids:
             messagebox.showerror("Input Error", "The payer must be included in the participants.")
             return


        # --- 模拟后端逻辑 ---
        print(f"Attempting to add expense: Amount={amount_str}, Date={date_str}, Category={category}, Paid By={payer_name}, Participants IDs={selected_participant_ids}")
        # 在实际实现中，这里会调用数据库方法
        # new_expense = Expense(amount=amount, date=date_str, category=category, payer_id=payer_id, participants=selected_participant_ids)
        # self.db.add_expense(new_expense)
        self.refresh_history_list() # 模拟添加后刷新列表
        self.clear_form()
        messagebox.showinfo("Success", "Expense added successfully.")

    def edit_expense(self):
        selected_item = self.history_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an expense to edit.")
            return
        messagebox.showinfo("Info", "Edit functionality for expense would be implemented here.")

    def delete_expense(self):
        selected_item = self.history_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an expense to delete.")
            return
        item_values = self.history_tree.item(selected_item)['values']
        expense_id = item_values[0]
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete expense ID {expense_id}?")
        if confirm:
            # --- 后端集成点 ---
            # try:
            #     self.db.delete_expense(expense_id)
            #     self.refresh_history_list()
            #     messagebox.showinfo("Success", f"Expense ID {expense_id} deleted.")
            # except Exception as e:
            #     messagebox.showerror("Database Error", f"Failed to delete expense: {str(e)}")

            # --- 模拟后端逻辑 ---
            print(f"Attempting to delete expense ID: {expense_id}")
            self.refresh_history_list() # 模拟删除后刷新列表
            messagebox.showinfo("Success", f"Expense ID {expense_id} deleted.")

    def refresh_history_list(self):
        # Clear existing items
        for i in self.history_tree.get_children():
            self.history_tree.delete(i)

        # --- 模拟后端逻辑 ---
        # 这里应该是从数据库获取费用历史
        mock_data = [
            (1, "$120.50", "2023-10-15", "Groceries", "Alice Johnson", "Alice, Bob, Charlie"),
            (2, "$80.00", "2023-10-18", "Dining Out", "Bob Smith", "Bob, Charlie"),
            (3, "$50.00", "2023-10-20", "Entertainment", "Charlie Brown", "Alice, Charlie"),
        ]
        for row in mock_data:
            self.history_tree.insert('', tk.END, values=row)

        # --- 实际后端集成示例 ---
        # try:
        #     expenses = self.db.get_all_expenses_with_details() # 这个方法需要返回包含室友名字的费用列表
        #     for exp in expenses:
        #         # 假设 exp 是一个包含所有信息的对象或字典
        #         self.history_tree.insert('', tk.END, values=(exp.id, f"${exp.amount:.2f}", exp.date, exp.category, exp.payer_name, exp.participant_names_str))
        # except Exception as e:
        #     messagebox.showerror("Database Error", f"Failed to load expense history: {str(e)}")

    def clear_form(self):
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.category_combo.set("Other")
        if self.payer_combo['values']:
            self.payer_combo.set(self.payer_combo['values'][0])
        for var in self.participant_vars.values():
            var.set(True) # 默认全选

    def on_show(self):
        """当此界面被显示时调用，用于刷新数据"""
        self.refresh_roommates_list()
        self.refresh_history_list()
        self.clear_form()