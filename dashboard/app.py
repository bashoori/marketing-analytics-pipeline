import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from components.helpers import plot_gauge

# ───── Streamlit Setup ─────
st.set_page_config(page_title="EA Marketing Dashboard", layout="wide")
plt.rcParams.update({
    'font.size': 7, 'axes.titlesize': 7, 'axes.labelsize': 7,
    'xtick.labelsize': 6, 'ytick.labelsize': 6, 'legend.fontsize': 6
})

# ───── Load Environment and DB ─────
load_dotenv()
conn_str = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(conn_str)

@st.cache_data
def load_data():
    return pd.read_sql("SELECT * FROM user_campaign_summary", engine)

df = load_data()
df.rename(columns={"clicked_at": "event_date"}, inplace=True)
df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")

# ───── Sidebar Filters ─────
st.sidebar.image("https://raw.githubusercontent.com/bashoori/repo/master/profile/ba.png", width=500)
st.sidebar.header("📂 Filters")
campaigns = st.sidebar.multiselect("Campaign", df["campaign_name"].unique(), default=df["campaign_name"].unique())
sources = st.sidebar.multiselect("Source", df["source"].unique(), default=df["source"].unique())
df_filtered = df[df["campaign_name"].isin(campaigns) & df["source"].isin(sources)]

# 🌙 Dark Mode Toggle
dark_mode = st.sidebar.toggle("🌙 Dark Mode (beta)", value=False)
if dark_mode:
    st.markdown("<style>body { background-color: #111; color: #eee; }</style>", unsafe_allow_html=True)


# ───── KPIs ─────
st.title("🎯 Marketing Analytics Dashboard")
k1, k2, k3, k4 = st.columns(4)
k1.metric("💰 Total Revenue", f"${df_filtered['total_revenue'].sum():,.2f}")
k2.metric("⏱ Total Playtime", f"{df_filtered['total_playtime'].sum():,.0f} min")
k3.metric("👥 Unique Users", df_filtered['user_id'].nunique())
k4.metric("🎯 Campaigns Used", df_filtered['campaign_name'].nunique())

# ───── Ratio Indicators ─────
r1, r2 = st.columns(2)
equity_ratio = 0.7538
debt_equity_ratio = 0.011

with r1:
    st.subheader("📈 Equity Ratio")
    st.progress(equity_ratio)
    st.write(f"**{equity_ratio * 100:.1f}%**")
    st.plotly_chart(plot_gauge("Equity Ratio", equity_ratio, "#00CC96"))

with r2:
    st.subheader("🏦 Debt Equity Ratio")
    st.progress(debt_equity_ratio)
    st.write(f"**{debt_equity_ratio * 100:.1f}%**")
    st.plotly_chart(plot_gauge("Debt Equity Ratio", debt_equity_ratio, "#EF553B"))

# ───── Revenue + Users by Category ─────
c1, c2 = st.columns(2)

with c1:
    st.subheader("💵 Revenue by Campaign")
    fig1, ax1 = plt.subplots(figsize=(3.5, 1.8))
    rev = df_filtered.groupby("campaign_name")["total_revenue"].sum().sort_values()
    ax1.barh(rev.index, rev.values, color="#1f77b4")
    ax1.set_xlabel("Revenue")
    st.pyplot(fig1)

with c2:
    st.subheader("🧩 Users by Source")
    fig2, ax2 = plt.subplots(figsize=(3, 2))
    src_counts = df_filtered['source'].value_counts()
    ax2.pie(src_counts.values, labels=src_counts.index, autopct='%1.1f%%', startangle=90)
    ax2.axis('equal')
    st.pyplot(fig2)

# ───── Playtime and Revenue by Source ─────
c3, c4 = st.columns(2)

with c3:
    st.subheader("📊 Playtime Trend by Source")
    fig3, ax3 = plt.subplots(figsize=(3, 2))
    trend = df_filtered.groupby('source')['total_playtime'].sum().sort_values(ascending=False)
    ax3.bar(trend.index, trend.values, color="#2ca02c")
    ax3.set_ylabel("Playtime (min)")
    ax3.set_xlabel("Source")
    ax3.set_xticklabels(trend.index, rotation=30, ha='right')
    fig3.tight_layout()
    st.pyplot(fig3)

with c4:
    st.subheader("🥧 Revenue Share by Source")
    pie = df_filtered.groupby("source")["total_revenue"].sum().reset_index()
    fig4 = px.pie(pie, values="total_revenue", names="source", title="Revenue Distribution", width=400, height=300)
    fig4.update_layout(title_font_size=14, margin=dict(t=30, b=10, l=10, r=10))
    st.plotly_chart(fig4)



    # 📥 Download Button
st.markdown("### 📥 Export Filtered Data")
st.download_button(
    label="Download CSV",
    data=df_filtered.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)