import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def load_to_postgres(df: pd.DataFrame, table_name: str = "user_campaign_summary"):
    """
    Loads a DataFrame into a PostgreSQL table.

    Parameters:
        df (pd.DataFrame): The transformed data to load
        table_name (str): The name of the target table in PostgreSQL

    Returns:
        None
    """
    try:
        # Load environment variables from .env
        load_dotenv()

        # Get database credentials
        db_user = os.getenv("DB_USER")
        db_pass = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME")

        # Build PostgreSQL connection string
        conn_str = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        engine = create_engine(conn_str)

        # Optional: create the table if it doesn't exist (replace schema manually if needed)
        with engine.begin() as conn:
            conn.execute(text(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    user_id INTEGER,
                    campaign_name TEXT,
                    source TEXT,
                    clicked_at TIMESTAMP,
                    total_playtime FLOAT,
                    total_revenue FLOAT
                )
            """))

        # Load DataFrame to table (replace if exists)
        df.to_sql(name=table_name, con=engine, if_exists="replace", index=False)
        print(f"✅ Loaded {len(df)} records into PostgreSQL table: {table_name}")

    except Exception as e:
        print(f"❌ Failed to load data to PostgreSQL: {e}")