"""
db_utils.py
Reusable database connection utility for the ApexPlanet Data Analytics Internship.

Usage:
    from db_utils import get_engine, run_query

    engine = get_engine()
    df = run_query(engine, "SELECT * FROM superstore LIMIT 10;")
"""

from sqlalchemy import create_engine
import pandas as pd


def get_engine(
    user: str = "root",
    password: str = "YOUR_MYSQL_PASSWORD",
    host: str = "localhost",
    port: int = 3306,
    database: str = "apexplanet_analytics",
):
    """
    Creates and returns a SQLAlchemy engine connected to the MySQL database.
    Update the default arguments below with your actual MySQL credentials,
    or pass them in directly when calling this function.
    """
    connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(connection_string)
    return engine


def run_query(engine, query: str) -> pd.DataFrame:
    """
    Runs a SQL query against the given engine and returns the result
    as a pandas DataFrame.
    """
    with engine.connect() as connection:
        df = pd.read_sql(query, connection)
    return df


if __name__ == "__main__":
    # Quick manual test when running this script directly
    engine = get_engine()
    result = run_query(engine, "SELECT COUNT(*) AS total_rows FROM superstore;")
    print(result)
