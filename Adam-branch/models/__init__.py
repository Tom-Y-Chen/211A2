# import pandas as pd
# # from database.db_connection import create_tables, add_expense
# from models.database.db_connection import initialize_database, get_connection


# def load_dataset(path="data/sample.csv"):
#     """Load CSV and insert into database."""
#     df = pd.read_csv(path)

#     # Standardize column names from the Kaggle dataset
#     df = df.rename(columns={
#         "INR": "Amount",
#         "amount": "Amount",
#         "Category": "Category",
#         "category": "Category",
#         "Account": "Account",
#         "Note": "Note",
#         "Date": "Date"
#     })

#     for _, row in df.iterrows():
#         add_expense(
#             date=str(row["Date"]),
#             account=str(row.get("Account", "")),
#             category=str(row.get("Category", "")),
#             note=str(row.get("Note", "")),
#             amount=float(row["Amount"])
#         )

# if __name__ == "__main__":
#     create_tables()
#     load_dataset()
#     print("Database initialized and dataset loaded.")
