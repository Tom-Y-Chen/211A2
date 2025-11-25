import pandas as pd
from models.database.db_connection import get_connection, initialize_database

def load_dataset(path="data/data.csv"):
    """Load CSV and insert into expenses table"""
    df = pd.read_csv(path)

    # Standardize column names
    df = df.rename(columns={
        "INR": "Amount",
        "amount": "Amount",
        "Category": "Category",
        "category": "Category",
        "Account": "Account",
        "Note": "Note",
        "Date": "Date"
    })

    conn = get_connection()
    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO expenses (date, account, category, amount, note)
            VALUES (?, ?, ?, ?, ?)
        """, (
            str(row["Date"]),
            str(row.get("Account", "")),
            str(row.get("Category", "")),
            float(row["Amount"]),
            str(row.get("Note", ""))
        ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    load_dataset("assets/data/datset.csv")
    print("Database initialized and dataset loaded.")


"""
References

Dataset
https://www.kaggle.com/datasets/ramyapintchy/personal-finance-data
"""
