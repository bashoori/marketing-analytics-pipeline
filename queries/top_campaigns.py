import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

def top_campaigns(limit: int = 5):
    load_dotenv()

    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME")

    conn_str = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(conn_str)

    query = f"""
        SELECT campaign_name, COUNT(*) AS clicks, SUM(total_revenue) AS revenue
        FROM user_campaign_summary
        GROUP BY campaign_name
        ORDER BY revenue DESC
        LIMIT {limit}
    """
    df = pd.read_sql(query, con=engine)
    return df

if __name__ == "__main__":
    df = top_campaigns()
    print(df)
