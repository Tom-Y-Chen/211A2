import tkinter as tk
from tkinter import ttk

class NavigationFrame(ttk.Frame):
    def __init__(self, parent, controller):
        """
        顶部导航栏，包含所有主要功能的按钮。
        :param parent: 父容器
        :param controller: RoomieSplitApp 实例，用于调用显示不同界面的方法
        """
        super().__init__(parent, relief="raised", borderwidth=1)
        self.controller = controller

        # 添加导航按钮
        ttk.Button(self, text="Dashboard", command=controller.show_dashboard).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(self, text="Manage Roommates", command=controller.show_manage_roommates).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(self, text="Add Expense", command=controller.show_add_expense).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(self, text="Reports", command=controller.show_report).pack(side=tk.LEFT, padx=2, pady=2)

        # 可选：添加一个“返回”按钮到主仪表盘
        # ttk.Button(self, text="Go to Dashboard", command=controller.show_dashboard).pack(side=tk.RIGHT, padx=2, pady=2)

    def on_show(self):
        """当导航栏所在的界面被显示时，可以进行一些更新操作（如果需要）"""
        # 当前导航栏本身不需要更新，但可以在此处添加逻辑
        pass