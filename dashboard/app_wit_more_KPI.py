import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# ───── Load environment and DB connection ─────
load_dotenv()
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME")
conn_str = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
engine = create_engine(conn_str)

@st.cache_data
def load_data():
    query = "SELECT * FROM user_campaign_summary"
    return pd.read_sql(query, engine)

df = load_data()

# ───── Sidebar Filters ─────
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/e1/EA_Sports_monogram_logo.svg", width=100)
st.sidebar.header("📂 Filters")
selected_campaigns = st.sidebar.multiselect("📢 Campaign", df["campaign_name"].unique(), default=df["campaign_name"].unique())
selected_sources = st.sidebar.multiselect("🌐 Source", df["source"].unique(), default=df["source"].unique())

filtered_df = df[df["campaign_name"].isin(selected_campaigns) & df["source"].isin(selected_sources)]

# ───── KPI Metrics Row ─────
st.title("🎯 Marketing Analytics Dashboard")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("💰 Total Revenue", f"${filtered_df['total_revenue'].sum():,.2f}")
kpi2.metric("⏱ Total Playtime", f"{filtered_df['total_playtime'].sum():,.0f} min")
kpi3.metric("👥 Unique Users", filtered_df['user_id'].nunique())
kpi4.metric("🎯 Campaigns Used", filtered_df['campaign_name'].nunique())

kpi_row1, kpi_row2 = st.columns(2)

with kpi_row1:
    st.subheader("📥 Total Accounts Receivable")
    st.bar_chart(pd.DataFrame({"Receivable": [6621280]}))

with kpi_row2:
    st.subheader("📤 Total Accounts Payable")
    st.bar_chart(pd.DataFrame({"Payable": [1630270]}))

kpi_row3, kpi_row4 = st.columns(2)

with kpi_row3:
    st.subheader("📈 Equity Ratio")
    st.progress(0.75)  # 75.38%

with kpi_row4:
    st.subheader("🏦 Debt Equity Ratio")
    st.progress(0.11)  # 1.10%

# ───── Charts Section ─────
chart1, chart2 = st.columns(2)

with chart1:
    st.subheader("💵 Revenue by Campaign")
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    rev_by_campaign = filtered_df.groupby("campaign_name")["total_revenue"].sum().sort_values()
    ax1.barh(rev_by_campaign.index, rev_by_campaign.values, color="#3399FF")
    ax1.set_xlabel("Revenue")
    ax1.set_ylabel("Campaign")
    st.pyplot(fig1)

with chart2:
    st.subheader("🧩 Users by Source")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    source_counts = filtered_df['source'].value_counts()
    ax2.pie(source_counts.values, labels=source_counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Set3.colors)
    ax2.axis('equal')
    st.pyplot(fig2)

st.subheader("📈 Playtime Trend by Source")
fig3, ax3 = plt.subplots(figsize=(10, 4))
trend = filtered_df.groupby(['source'])['total_playtime'].sum().sort_values(ascending=False)
ax3.bar(trend.index, trend.values, color="#66CC99")
ax3.set_ylabel("Total Playtime (min)")
st.pyplot(fig3)


