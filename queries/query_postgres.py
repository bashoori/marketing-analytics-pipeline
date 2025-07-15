import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def query_postgres(table_name: str = "user_campaign_summary", limit: int = 10):
    """
    Connects to PostgreSQL and queries data from the specified table.

    Parameters:
        table_name (str): Name of the table to query.
        limit (int): Number of rows to fetch.

    Returns:
        pd.DataFrame: Query result as a DataFrame.
    """
    try:
        # Load DB credentials from .env
        load_dotenv()

        db_user = os.getenv("DB_USER")
        db_pass = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME")

        # Create SQLAlchemy engine
        conn_str = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        engine = create_engine(conn_str)

        # Define query
        query = text(f"SELECT * FROM {table_name} LIMIT :limit")
        with engine.connect() as conn:
            result = pd.read_sql(query, conn, params={"limit": limit})

        print(f"✅ Retrieved {len(result)} records from table: {table_name}")
        return result

    except Exception as e:
        print(f"❌ Failed to query PostgreSQL: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    df = query_postgres(limit=10)
    print(df)