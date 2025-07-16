import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# ───── Streamlit Page Setup ─────
st.set_page_config(page_title="EA Marketing Dashboard", layout="wide")
plt.rcParams.update({
    'font.size': 7,
    'axes.titlesize': 7,
    'axes.labelsize': 7,
    'xtick.labelsize': 6,
    'ytick.labelsize': 6,
    'legend.fontsize': 6
})

# ───── Load environment and DB connection ─────
load_dotenv()
conn_str = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(conn_str)

@st.cache_data
def load_data():
    return pd.read_sql("SELECT * FROM user_campaign_summary", engine)

df = load_data()
st.write("🧾 Columns in the data:", df.columns.tolist())  # 👈 This will print column names

# 🔁 Rename clicked_at to event_date before any filtering
df.rename(columns={"clicked_at": "event_date"}, inplace=True)

# Sidebar filters
st.sidebar.image("https://raw.githubusercontent.com/bashoori/repo/master/profile/ba.png", width=500)
st.sidebar.header("📂 Filters")
campaigns = st.sidebar.multiselect("📢 Campaign", df["campaign_name"].unique(), default=df["campaign_name"].unique())
sources = st.sidebar.multiselect("🌐 Source", df["source"].unique(), default=df["source"].unique())
filtered_df = df[df["campaign_name"].isin(campaigns) & df["source"].isin(sources)]

# Now this will work correctly:
filtered_df["event_date"] = pd.to_datetime(filtered_df["event_date"], errors="coerce")


# ───── KPIs ─────
st.title("🎯 Marketing Analytics Dashboard")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("💰 Total Revenue", f"${filtered_df['total_revenue'].sum():,.2f}")
kpi2.metric("⏱ Total Playtime", f"{filtered_df['total_playtime'].sum():,.0f} min")
kpi3.metric("👥 Unique Users", filtered_df['user_id'].nunique())
kpi4.metric("🎯 Campaigns Used", filtered_df['campaign_name'].nunique())

# ───── Revenue Trend Over Time ─────
st.subheader("📊 Revenue Trend Over Time")
if "event_date" in filtered_df.columns:
    #filtered_df["event_date"] = pd.to_datetime(filtered_df["event_date"], errors="coerce")
    filtered_df["event_date"] = pd.to_datetime(filtered_df["clicked_at"], errors="coerce")
    #trend_df = filtered_df.groupby(filtered_df["event_date"].dt.date)["total_revenue"].sum().reset_index()
    trend_df = filtered_df.groupby(filtered_df["clicked_at"].dt.date)["total_revenue"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.plot(trend_df["event_date"], trend_df["total_revenue"], marker='o', color="#FF6600")
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue ($)")
    ax.grid(True)
    st.pyplot(fig)
else:
    st.warning("📅 No 'event_date' column found for time-based trend chart.")

# ───── Ratio Indicators ─────
r1, r2 = st.columns(2)
with r1:
    st.subheader("📈 Equity Ratio")
    st.progress(0.7538)
with r2:
    st.subheader("🏦 Debt Equity Ratio")
    st.progress(0.011)

# ───── Revenue + Users by Source ─────
c1, c2 = st.columns(2)
with c1:
    st.subheader("💵 Revenue by Campaign")
    fig_rev, ax = plt.subplots(figsize=(3.5, 1.8))
    rev = filtered_df.groupby("campaign_name")["total_revenue"].sum().sort_values()
    ax.barh(rev.index, rev.values, color="#1f77b4")
    ax.set_xlabel("Revenue")
    st.pyplot(fig_rev)

with c2:
    st.subheader("🧩 Users by Source")
    fig_src, ax = plt.subplots(figsize=(3, 2))
    src_counts = filtered_df['source'].value_counts()
    ax.pie(src_counts.values, labels=src_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig_src)

# ───── Playtime + Revenue Share ─────
c1, c2 = st.columns(2)
with c1:
    st.subheader("📊 Playtime Trend by Source")
    fig_pt, ax = plt.subplots(figsize=(3, 2))
    trend = filtered_df.groupby('source')['total_playtime'].sum().sort_values(ascending=False)
    ax.bar(trend.index, trend.values, color="#2ca02c")
    ax.set_ylabel("Playtime (min)")
    ax.set_xlabel("Source")
    ax.set_xticklabels(trend.index, rotation=30, ha='right')
    fig_pt.tight_layout()
    st.pyplot(fig_pt)

with c2:
    st.subheader("🥧 Revenue Share by Source")
    pie = filtered_df.groupby("source")["total_revenue"].sum().reset_index()
    fig = px.pie(pie, values="total_revenue", names="source", title="Revenue Distribution", width=400, height=300)
    fig.update_layout(title_font_size=14, margin=dict(t=30, b=10, l=10, r=10))
    st.plotly_chart(fig)

# ───── Custom Charts ─────
def create_gauge_chart(value=68, label="Conversion Rate", color="#FF6600"):
    fig, ax = plt.subplots(figsize=(3.5, 1.8))
    ax.barh([0], [value], color=color)
    ax.set_xlim(0, 100)
    ax.set_title(label)
    ax.set_yticks([])
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.grid(True, linestyle='--', linewidth=0.5)
    return fig

g1, g2 = st.columns(2)
with g1:
    st.subheader("🎯 Conversion Rate")
    st.pyplot(create_gauge_chart())

with g2:
    st.subheader("📈 Monthly Playtime by Campaign")
    if "event_date" in filtered_df.columns:
        filtered_df["month"] = filtered_df["event_date"].dt.to_period("M").astype(str)
        monthly = filtered_df.groupby(['month', 'campaign_name'])['total_playtime'].sum().reset_index()
        pivot = monthly.pivot(index='month', columns='campaign_name', values='total_playtime')
        fig, ax = plt.subplots(figsize=(5, 3))
        for col in pivot.columns:
            ax.plot(pivot.index, pivot[col], label=col, marker='o', linewidth=2)
        ax.set_xlabel("Month")
        ax.set_ylabel("Playtime (min)")
        ax.set_title("Monthly Playtime")
        ax.legend(fontsize=6)
        ax.grid(True, linestyle='--', linewidth=0.5)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("📅 No 'event_date' column found to generate monthly trend.")