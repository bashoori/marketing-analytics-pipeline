import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load database credentials
load_dotenv()
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME")

# Connect to PostgreSQL
conn_str = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
engine = create_engine(conn_str)

# Load data
@st.cache_data
def load_data():
    query = "SELECT * FROM user_campaign_summary"
    df = pd.read_sql(query, engine)
    return df

df = load_data()

# UI: Title and filters
st.title("📊 Marketing Campaign Dashboard")
st.markdown("Visualize performance of campaigns and revenue sources.")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
campaigns = st.sidebar.multiselect("Campaign", df["campaign_name"].unique(), default=df["campaign_name"].unique())
sources = st.sidebar.multiselect("Source", df["source"].unique(), default=df["source"].unique())

# Filters
campaigns = st.multiselect("Filter by Campaign", df["campaign_name"].unique(), default=df["campaign_name"].unique())
sources = st.multiselect("Filter by Source", df["source"].unique(), default=df["source"].unique())

filtered_df = df[df["campaign_name"].isin(campaigns) & df["source"].isin(sources)]

# Metrics
col1, col2 = st.columns(2)
col1.metric("Total Revenue", f"${filtered_df['total_revenue'].sum():,.2f}")
col2.metric("Total Playtime (min)", f"{filtered_df['total_playtime'].sum():,.0f}")

# Show table
st.subheader("🔎 Filtered Data")
st.dataframe(filtered_df)

# Chart
st.subheader("📈 Revenue by Campaign")
chart_data = filtered_df.groupby("campaign_name")["total_revenue"].sum().sort_values(ascending=False)
st.bar_chart(chart_data)