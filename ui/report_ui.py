import tkinter as tk
from tkinter import ttk, messagebox
# 假设您已经创建了 logic.calculator
# from logic.calculator import calculate_settlements

class ReportFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # self.db = controller.db # 假设 controller 有数据库实例

        # --- 布局容器 ---
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- 报告类型选择 ---
        type_frame = ttk.Frame(main_frame)
        type_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        type_frame.grid_columnconfigure(0, weight=1) # 让空白列填充空间

        ttk.Label(type_frame, text="Report Type:").grid(row=0, column=1, sticky='w', padx=(0, 10))
        self.report_type_var = tk.StringVar(value="Settlement")
        ttk.Radiobutton(type_frame, text="Settlement Summary", variable=self.report_type_var, value="Settlement").grid(row=0, column=2, sticky='w', padx=(0, 10))
        ttk.Radiobutton(type_frame, text="Personal Budget (Individual)", variable=self.report_type_var, value="Personal").grid(row=0, column=3, sticky='w', padx=(0, 10))
        ttk.Button(type_frame, text="Generate Report", command=self.generate_report).grid(row=0, column=4, sticky='e', padx=(0, 0))

        # --- 结算报告区域 ---
        self.settlement_frame = ttk.LabelFrame(main_frame, text="Settlement Report", padding=10)
        # self.settlement_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5) # 移除 pack，改用 grid

        settlement_columns = ('Person Owing', 'Owes To', 'Amount ($)')
        self.settlement_tree = ttk.Treeview(self.settlement_frame, columns=settlement_columns, show='headings', height=10)
        for col in settlement_columns:
            self.settlement_tree.heading(col, text=col)
            self.settlement_tree.column(col, width=150, anchor=tk.CENTER)

        scrollbar_settlement = ttk.Scrollbar(self.settlement_frame, orient=tk.VERTICAL, command=self.settlement_tree.yview)
        self.settlement_tree.configure(yscroll=scrollbar_settlement.set)

        self.settlement_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_settlement.pack(side=tk.RIGHT, fill=tk.Y)

        # --- 个人预算报告区域 ---
        self.personal_frame = ttk.LabelFrame(main_frame, text="Personal Budget Report", padding=10)
        # self.personal_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5) # 移除 pack，改用 grid

        # 个人预算树视图
        personal_columns = ('Category', 'Total Amount ($)')
        self.personal_tree = ttk.Treeview(self.personal_frame, columns=personal_columns, show='headings', height=10)
        for col in personal_columns:
            self.personal_tree.heading(col, text=col)
            self.personal_tree.column(col, width=150, anchor=tk.CENTER)

        scrollbar_personal = ttk.Scrollbar(self.personal_frame, orient=tk.VERTICAL, command=self.personal_tree.yview)
        self.personal_tree.configure(yscroll=scrollbar_personal.set)

        self.personal_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_personal.pack(side=tk.RIGHT, fill=tk.Y)

        # 配置 main_frame 的网格权重，让下方框架填充剩余空间
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # 初始显示结算报告区域
        self.settlement_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        self.personal_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5) # 与结算区域放在同一位置
        self.personal_frame.grid_remove() # 初始隐藏个人预算区域

        # 刷新数据
        self.generate_report() # 初始加载结算报告

    def generate_report(self):
        report_type = self.report_type_var.get()

        if report_type == "Settlement":
            self.settlement_tree.delete(*self.settlement_tree.get_children())
            self.personal_frame.grid_remove() # 隐藏个人预算区域
            self.settlement_frame.grid() # 显示结算区域 (如果之前被隐藏)

            # --- 后端集成点 ---
            # try:
            #     settlements = calculate_settlements(self.db) # 调用后端计算逻辑
            #     for settlement in settlements:
            #         self.settlement_tree.insert('', tk.END, values=(settlement['debtor'], settlement['creditor'], f"${settlement['amount']:.2f}"))
            # except Exception as e:
            #     messagebox.showerror("Calculation Error", f"Failed to calculate settlements: {str(e)}")

            # --- 模拟后端逻辑 ---
            print("Generating Settlement Report...")
            mock_settlements = [
                ("Bob Smith", "Alice Johnson", 20.17),
                ("Charlie Brown", "Alice Johnson", 15.00),
            ]
            for item in mock_settlements:
                self.settlement_tree.insert('', tk.END, values=(item[0], item[1], f"${item[2]:.2f}"))

        elif report_type == "Personal":
            self.personal_tree.delete(*self.personal_tree.get_children())
            self.settlement_frame.grid_remove() # 隐藏结算区域
            self.personal_frame.grid() # 显示个人预算区域 (如果之前被隐藏)

            # --- 后端集成点 ---
            # try:
            #     personal_budget = calculate_personal_budget(self.db) # 调用后端计算逻辑
            #     for category, total in personal_budget.items():
            #         self.personal_tree.insert('', tk.END, values=(category, f"${total:.2f}"))
            # except Exception as e:
            #     messagebox.showerror("Calculation Error", f"Failed to calculate personal budget: {str(e)}")

            # --- 模拟后端逻辑 ---
            print("Generating Personal Budget Report...")
            mock_personal_budget = {
                "Rent": 1200.00,
                "Utilities": 150.00,
                "Groceries": 300.50,
                "Dining Out": 200.00,
                "Entertainment": 100.00,
                "Other": 50.75,
            }
            for category, total in mock_personal_budget.items():
                self.personal_tree.insert('', tk.END, values=(category, f"${total:.2f}"))

    def on_show(self):
        """当此界面被显示时调用，用于刷新数据"""
        self.generate_report()
