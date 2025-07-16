import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import plotly.express as px

# Load environment variables
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
    return pd.read_sql(query, engine)

df = load_data()

# Title
st.title("📊 Marketing Campaign Dashboard")
st.markdown("Visualize performance of campaigns and revenue sources.")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
campaigns = st.sidebar.multiselect("Campaign", df["campaign_name"].unique(), default=df["campaign_name"].unique())
sources = st.sidebar.multiselect("Source", df["source"].unique(), default=df["source"].unique())

# Apply filters
filtered_df = df[df["campaign_name"].isin(campaigns) & df["source"].isin(sources)]

# Metrics
col1, col2 = st.columns(2)
col1.metric("💰 Total Revenue", f"${filtered_df['total_revenue'].sum():,.2f}")
col2.metric("⏱️ Total Playtime (min)", f"{filtered_df['total_playtime'].sum():,.0f}")

# Data Table
st.subheader("📄 Filtered Data")
st.dataframe(filtered_df)

# Chart
st.subheader("📈 Revenue by Campaign")
chart_data = filtered_df.groupby("campaign_name")["total_revenue"].sum().sort_values(ascending=False)
st.bar_chart(chart_data)



# 📊 Pie Chart
st.subheader("🥧 Revenue Share by Source")
pie_data = filtered_df.groupby("source")["total_revenue"].sum().reset_index()
fig = px.pie(pie_data, values="total_revenue", names="source", title="Revenue Distribution by Source")
st.plotly_chart(fig)


# 👥 نمودار دایره‌ای تعداد کاربران به تفکیک Source
st.subheader("👥 User Distribution by Source")
user_pie_data = filtered_df.groupby("source")["user_id"].nunique().reset_index()
fig2 = px.pie(user_pie_data, values="user_id", names="source", title="User Count by Source")
st.plotly_chart(fig2)