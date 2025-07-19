import os
import pandas as pd
import psycopg2  # ✅ You need this import
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def load_to_postgres(df: pd.DataFrame, table_name: str = "user_campaign_summary"):
    """
    Loads a DataFrame into a PostgreSQL table.
    """
    try:
        load_dotenv()

        # ✅ Get credentials from .env (or hardcode temporarily)
        db_user = os.getenv("MARKETING_DB_USER", "user")
        db_pass = os.getenv("MARKETING_DB_PASSWORD", "pass")
        db_host = os.getenv("MARKETING_DB_HOST", "pgdb")  # Important fix!
        db_port = os.getenv("MARKETING_DB_PORT", "5432")
        db_name = os.getenv("MARKETING_DB_NAME", "marketingdb")

        # ✅ SQLAlchemy connection string
        conn_str = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        engine = create_engine(conn_str)

        # ✅ Create table if not exists
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

        # ✅ Load DataFrame to PostgreSQL
        df.to_sql(name=table_name, con=engine, if_exists="replace", index=False)
        print(f"✅ Loaded {len(df)} records into PostgreSQL table: {table_name}")

    except Exception as e:
        print(f"❌ Failed to load data to PostgreSQL: {e}")