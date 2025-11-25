import tkinter as tk
from tkinter import ttk
from ui.dashboard import DashboardFrame
from ui.roommate_ui import RoommateManagerFrame
from ui.expense_ui import ExpenseEntryFrame
from ui.report_ui import ReportFrame
from ui.navigation import NavigationFrame # 导入导航栏

class RoomieSplitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RoomieSplit - Expense Tracker")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        # --- 样式设置 ---
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TEntry', font=('Arial', 10))
        self.style.configure('TCombobox', font=('Arial', 10))

        # --- 主容器 ---
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- 初始化并显示主仪表盘 ---
        self.frames = {}
        self.current_frame = None
        self._create_frames()
        self.show_frame("Dashboard")

    def _create_frames(self):
        """创建所有界面实例"""
        F = {
            # Dashboard 不需要导航栏
            "Dashboard": DashboardFrame,
            # 其他界面需要导航栏
            "RoommateManager": RoommateManagerFrame,
            "ExpenseEntry": ExpenseEntryFrame,
            "Report": ReportFrame,
        }

        for name, frame_class in F.items():
            if name == "Dashboard":
                # Dashboard 使用原始框架
                frame = frame_class(self.main_container, self)
                self.frames[name] = frame
            else:
                # 其他界面使用包含导航栏的容器
                container_frame = ttk.Frame(self.main_container)
                nav_frame = NavigationFrame(container_frame, self)
                nav_frame.pack(side=tk.TOP, fill=tk.X)

                content_frame = frame_class(container_frame, self)
                content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(5, 0))

                self.frames[name] = container_frame

            # 将所有框架添加到网格，但初始隐藏
            self.frames[name].grid(row=0, column=0, sticky="nsew")
            self.frames[name].grid_remove() # 初始隐藏

        # 配置主容器网格权重
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

    def show_frame(self, name):
        """显示指定的界面"""
        if self.current_frame:
            if hasattr(self.current_frame, 'on_show'):
                 self.current_frame.on_show()
            self.current_frame.grid_remove()
        self.current_frame = self.frames[name]
        self.current_frame.grid()

    # --- 为导航栏和仪表盘提供导航方法 ---
    def show_dashboard(self):
        self.show_frame("Dashboard")

    def show_manage_roommates(self):
        self.show_frame("RoommateManager")

    def show_add_expense(self):
        self.show_frame("ExpenseEntry")

    def show_report(self):
        self.show_frame("Report")

if __name__ == "__main__":
    root = tk.Tk()
    app = RoomieSplitApp(root)
    root.mainloop()