from sqlalchemy import create_engine
import pandas as pd

# Connect to SQLite DB
engine = create_engine("sqlite:///fraud.db")


def get_customer_transactions(customer_id: str):

    query = f"""
    SELECT *
    FROM transactions
    WHERE customer_id = '{customer_id}'
    """

    df = pd.read_sql(query, engine)

    return df.to_dict(orient="records")