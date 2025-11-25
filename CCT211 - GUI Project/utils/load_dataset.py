# utils/load_dataset.py
import pandas as pd
import os
from models.database.db_connection import get_connection  # Add this import

def load_dataset(path="assets/data/dataset.csv"):
    """Load CSV and insert into expenses table"""
    # Get the absolute path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, path)
    
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Dataset file not found at {full_path}")

    df = pd.read_csv(full_path)
    print(f"Loaded dataset with {len(df)} rows from {full_path}")

    # Standardize column names
    df = df.rename(columns={
        "INR": "amount",
        "Amount": "amount", 
        "Category": "category",
        "Account": "account",
        "Note": "note",
        "Date": "date"
    })

    conn = get_connection()  # This should work now
    cur = conn.cursor()

    inserted_count = 0
    for _, row in df.iterrows():
        try:
            cur.execute("""
                INSERT INTO expenses (date, account, category, amount, note)
                VALUES (?, ?, ?, ?, ?)
            """, (
                str(row.get("date", "")),
                str(row.get("account", "")),
                str(row.get("category", "")),
                float(row["amount"]),
                str(row.get("note", ""))
            ))
            inserted_count += 1
        except Exception as e:
            print(f"Error inserting row {_}: {e}")

    conn.commit()
    conn.close()
    print(f"Successfully inserted {inserted_count} expenses into database")

if __name__ == "__main__":
    from models.database.db_connection import initialize_database
    initialize_database()
    load_dataset("assets/data/dataset.csv")
    print("Database initialized and dataset loaded.")


# import pandas as pd
# import os
# from models.database.db_connection import get_connection, initialize_database

# def load_dataset(path="assets/data/data.csv"):
#     """Load CSV and insert into expenses table"""
#     # df = pd.read_csv(path)

#     # Get the absolute path
#     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     full_path = os.path.join(base_dir, path)
    
#     if not os.path.exists(full_path):
#         raise FileNotFoundError(f"Dataset file not found at {full_path}")

#     df = pd.read_csv(full_path)
#     print(f"Loaded dataset with {len(df)} rows from {full_path}")

#     # Standardize column names
#     df = df.rename(columns={
#         "INR": "Amount",
#         "amount": "Amount",
#         "Category": "Category",
#         "category": "Category",
#         "Account": "Account",
#         "Note": "Note",
#         "Date": "Date"
#     })

#     conn = get_connection()
#     cur = conn.cursor()

#     for _, row in df.iterrows():
#         try:
#             cur.execute("""
#                 INSERT INTO expenses (date, account, category, amount, note)
#                 VALUES (?, ?, ?, ?, ?)
#             """, (
#                 str(row.get("date", "")),
#                 str(row.get("account", "")),
#                 str(row.get("category", "")),
#                 float(row["amount"]),
#                 str(row.get("note", ""))
#             ))
#             inserted_count += 1
#         except Exception as e:
#             print(f"Error inserting row {_}: {e}")

#     conn.commit()
#     conn.close()
#     print(f"Successfully inserted {inserted_count} expenses into database")


# if __name__ == "__main__":
#     from models.database.db_connection import initialize_database
#     initialize_database()
#     load_dataset("assets/data/dataset.csv")
#     print("Database initialized and dataset loaded.")


"""
References

Dataset
https://www.kaggle.com/datasets/ramyapintchy/personal-finance-data
"""