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

def get_customer_devices(customer_id: str):

    query = f"""
    SELECT *
    FROM devices
    WHERE customer_id = '{customer_id}'
    """

    df = pd.read_sql(query, engine)

    return df.to_dict(orient="records")


def get_customer_upi_handles(customer_id: str):

    query = f"""
    SELECT *
    FROM upi_handles
    WHERE customer_id = '{customer_id}'
    """

    df = pd.read_sql(query, engine)

    return df.to_dict(orient="records")


def get_related_customers_by_ip(ip_address: str):

    query = f"""
    SELECT *
    FROM devices
    WHERE ip_address = '{ip_address}'
    """

    df = pd.read_sql(query, engine)

    return df.to_dict(orient="records")