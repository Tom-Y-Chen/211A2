# 211A2


RoomieSplit/
├── main.py                  # 应用入口
├── database/
│   ├── __init__.py
│   ├── db_connection.py     # 数据库连接
│   ├── roommate_db.py       # 室友数据操作
│   └── expense_db.py        # 费用数据操作
├── models/
│   ├── __init__.py
│   ├── roommate.py          # 室友模型
│   ├── expense.py           # 费用模型
│   └── settlement.py        # 结算模型
├── logic/
│   ├── __init__.py
│   ├── calculator.py        # 费用计算核心逻辑
│   └── report_generator.py  # 报告生成逻辑
├── ui/
│   ├── __init__.py
│   ├── dashboard.py         # 主仪表盘
│   ├── roommate_ui.py       # 室友管理界面
│   ├── expense_ui.py        # 费用录入界面
│   └── report_ui.py         # 报告查看界面
├── utils/
│   ├── __init__.py
│   ├── validators.py        # 输入验证
│   └── helpers.py           # 通用工具函数
├── assets/                  # 界面资源（图标、样式等）
└── tests/                   # 测试文件



Datasets links:

https://www.kaggle.com/datasets/ramyapintchy/personal-finance-data
https://www.kaggle.com/datasets/sanjay3454chauhan/personal-expense-data
https://www.kaggle.com/datasets/tharunprabu/my-expenses-data
