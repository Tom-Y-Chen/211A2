import tkinter as tk
from tkinter import ttk

class DashboardFrame(ttk.Frame):
    def __init__(self, parent, controller): # controller 是 RoomieSplitApp 的实例
        super().__init__(parent)
        self.controller = controller

        # --- 仪表盘内容 ---
        # 标题
        title_label = ttk.Label(self, text="RoomieSplit Dashboard", font=('Arial', 16, 'bold'))
        title_label.pack(pady=(10, 20))

        # 描述
        desc_label = ttk.Label(self, text="Manage shared expenses with your roommates or track your personal budget.", wraplength=400)
        desc_label.pack(pady=(0, 20))

        # 操作按钮
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        # 这些按钮将用于导航到其他功能
        # 按钮的 command 将在后续步骤中连接到 controller 的方法
        ttk.Button(button_frame, text="Manage Roommates", command=self.on_manage_roommates_click).pack(pady=5)
        ttk.Button(button_frame, text="Add New Expense", command=self.on_add_expense_click).pack(pady=5)
        ttk.Button(button_frame, text="View Settlement Report", command=self.on_view_report_click).pack(pady=5)
        ttk.Button(button_frame, text="View Personal Budget", command=self.on_view_budget_click).pack(pady=5)

        # 概览信息区域 (可以后续添加)
        # overview_frame = ttk.LabelFrame(self, text="Overview")
        # overview_frame.pack(fill=tk.X, padx=20, pady=20)

    def on_manage_roommates_click(self):
        """处理“管理室友”按钮点击事件"""
        print("Manage Roommates button clicked") # 临时打印，后续替换为实际逻辑
        # 例如: self.controller.show_manage_roommates() # 需要在 controller 中实现此方法

    def on_add_expense_click(self):
        """处理“添加费用”按钮点击事件"""
        print("Add New Expense button clicked") # 临时打印，后续替换为实际逻辑
        # 例如: self.controller.show_expense_entry() # 需要在 controller 中实现此方法

    def on_view_report_click(self):
        """处理“查看结算报告”按钮点击事件"""
        print("View Settlement Report button clicked") # 临时打印，后续替换为实际逻辑
        # 例如: self.controller.show_report() # 需要在 controller 中实现此方法

    def on_view_budget_click(self):
        """处理“查看个人预算”按钮点击事件"""
        print("View Personal Budget button clicked") # 临时打印，后续替换为实际逻辑
        # 例如: self.controller.show_budget() # 需要在 controller 中实现此方法