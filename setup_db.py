import pandas as pd
from sqlalchemy import create_engine

# Create SQLite database
engine = create_engine("sqlite:///fraud.db")

# CSV files to load
files = [
    "customers",
    "devices",
    "transactions",
    "upi_handles",
    "merchants"
]

# Load each CSV into SQLite
for file in files:
    df = pd.read_csv(f"data/{file}.csv")
    df.to_sql(file, engine, if_exists="replace", index=False)
    print(f"Loaded {file}.csv")

print("\nDatabase setup complete.")