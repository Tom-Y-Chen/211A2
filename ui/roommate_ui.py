import tkinter as tk
from tkinter import ttk, messagebox
# 假设您已经创建了 models.roommate 和 utils.validators
# from models.roommate import Roommate
# from utils.validators import validate_email # 示例验证器

class RoommateManagerFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # self.db = controller.db # 假设 controller 有数据库实例

        # --- 布局容器 ---
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- 添加室友区域 ---
        add_frame = ttk.LabelFrame(main_frame, text="Add New Roommate", padding=10)
        add_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(add_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.name_entry = ttk.Entry(add_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=(0, 10), pady=2)

        ttk.Label(add_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.email_entry = ttk.Entry(add_frame, width=20)
        self.email_entry.grid(row=1, column=1, padx=(0, 10), pady=2)

        # ttk.Label(add_frame, text="Join Date:").grid(row=2, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        # self.date_entry = DateEntry(add_frame, width=12, background='darkblue', foreground='white', borderwidth=2) # 需要ttkbootstrap或类似库
        # self.date_entry.grid(row=2, column=1, padx=(0, 10), pady=2)
        # 或者使用简单的Entry
        ttk.Label(add_frame, text="Join Date (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.date_entry = ttk.Entry(add_frame, width=15)
        self.date_entry.grid(row=2, column=1, padx=(0, 10), pady=2)

        self.add_button = ttk.Button(add_frame, text="Add Roommate", command=self.add_roommate)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=5)

        # --- 室友列表区域 ---
        list_frame = ttk.LabelFrame(main_frame, text="Roommate List", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Treeview for displaying roommates
        columns = ('ID', 'Name', 'Email', 'Join Date')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Join Date', text='Join Date')

        # 设置列宽
        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('Name', width=150, anchor=tk.W)
        self.tree.column('Email', width=200, anchor=tk.W)
        self.tree.column('Join Date', width=100, anchor=tk.CENTER)

        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 按钮框架
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))

        self.edit_button = ttk.Button(button_frame, text="Edit Selected", command=self.edit_roommate)
        self.edit_button.pack(side=tk.LEFT, padx=(0, 5))
        self.delete_button = ttk.Button(button_frame, text="Delete Selected", command=self.delete_roommate)
        self.delete_button.pack(side=tk.LEFT)

        # 加载初始数据
        self.refresh_list()

    def add_roommate(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        join_date = self.date_entry.get().strip()

        if not name or not email:
            messagebox.showerror("Input Error", "Name and Email are required fields.")
            return

        # --- 后端集成点 ---
        # try:
        #     # 验证邮箱 (如果使用utils.validators)
        #     # if not validate_email(email):
        #     #     raise ValueError("Invalid email format")
        #
        #     new_roommate = Roommate(name=name, email=email, join_date=join_date)
        #     self.db.add_roommate(new_roommate)
        #     self.refresh_list()
        #     self.clear_add_form()
        #     messagebox.showinfo("Success", f"Roommate '{name}' added successfully.")
        # except ValueError as e:
        #     messagebox.showerror("Validation Error", str(e))
        # except Exception as e:
        #     messagebox.showerror("Database Error", f"Failed to add roommate: {str(e)}")

        # --- 模拟后端逻辑 ---
        print(f"Attempting to add roommate: Name='{name}', Email='{email}', Join Date='{join_date}'")
        # 在实际实现中，这里会调用数据库方法
        # self.db.add_roommate(name, email, join_date)
        self.refresh_list() # 模拟添加后刷新列表
        self.clear_add_form()
        messagebox.showinfo("Success", f"Roommate '{name}' added successfully.")

    def edit_roommate(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a roommate to edit.")
            return

        item_id = self.tree.item(selected_item)['values'][0] # 假设ID是第一列
        # --- 后端集成点 ---
        # messagebox.showinfo("Edit", f"Editing roommate with ID: {item_id}")
        # 在实际实现中，这里会打开一个编辑窗口或修改当前窗口
        messagebox.showinfo("Info", f"Edit functionality for roommate ID {item_id} would be implemented here.")

    def delete_roommate(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a roommate to delete.")
            return

        item_values = self.tree.item(selected_item)['values']
        roommate_name = item_values[1] # 假设Name是第二列
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{roommate_name}'?")

        if confirm:
            # --- 后端集成点 ---
            # try:
            #     roommate_id = item_values[0]
            #     self.db.delete_roommate(roommate_id)
            #     self.refresh_list()
            #     messagebox.showinfo("Success", f"Roommate '{roommate_name}' deleted.")
            # except Exception as e:
            #     messagebox.showerror("Database Error", f"Failed to delete roommate: {str(e)}")

            # --- 模拟后端逻辑 ---
            print(f"Attempting to delete roommate: ID={item_values[0]}, Name='{roommate_name}'")
            self.refresh_list() # 模拟删除后刷新列表
            messagebox.showinfo("Success", f"Roommate '{roommate_name}' deleted.")

    def refresh_list(self):
        # --- 后端集成点 ---
        # Clear existing items
        for i in self.tree.get_children():
            self.tree.delete(i)

        # --- 模拟后端逻辑 ---
        # 这里应该是从数据库获取数据
        mock_data = [
            (1, "Alice Johnson", "alice@example.com", "2023-09-01"),
            (2, "Bob Smith", "bob@example.com", "2023-09-15"),
            (3, "Charlie Brown", "charlie@example.com", "2023-10-01"),
        ]
        for row in mock_data:
            self.tree.insert('', tk.END, values=row)

        # --- 实际后端集成示例 ---
        # try:
        #     roommates = self.db.get_all_roommates()
        #     for rm in roommates:
        #         self.tree.insert('', tk.END, values=(rm.id, rm.name, rm.email, rm.join_date))
        # except Exception as e:
        #     messagebox.showerror("Database Error", f"Failed to load roommates: {str(e)}")

    def clear_add_form(self):
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        # self.date_entry.set_date(datetime.date.today()) # 如果使用DateEntry

    def on_show(self):
        """当此界面被显示时调用，用于刷新数据"""
        self.refresh_list()
        self.clear_add_form()