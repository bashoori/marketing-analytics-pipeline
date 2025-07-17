import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from components.helpers import plot_gauge


st.plotly_chart(plot_gauge("Equity Ratio", 0.7538, "#00CC96"))
st.plotly_chart(plot_gauge("Debt Equity Ratio", 0.011, "#EF553B"))


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

# ✅ Rename clicked_at → event_date for consistency
df.rename(columns={"clicked_at": "event_date"}, inplace=True)
df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")

# 👀 Show columns
#st.write("🧾 Columns in the data:", df.columns.tolist())

# ───── Sidebar Filters ─────
st.sidebar.image("https://raw.githubusercontent.com/bashoori/repo/master/profile/ba.png", width=500)
st.sidebar.header("📂 Filters")
campaigns = st.sidebar.multiselect("📢 Campaign", df["campaign_name"].unique(), default=df["campaign_name"].unique())
sources = st.sidebar.multiselect("🌐 Source", df["source"].unique(), default=df["source"].unique())
filtered_df = df[df["campaign_name"].isin(campaigns) & df["source"].isin(sources)]

# ───── KPIs ─────
st.title("🎯 Marketing Analytics Dashboard")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("💰 Total Revenue", f"${filtered_df['total_revenue'].sum():,.2f}")
kpi2.metric("⏱ Total Playtime", f"{filtered_df['total_playtime'].sum():,.0f} min")
kpi3.metric("👥 Unique Users", filtered_df['user_id'].nunique())
kpi4.metric("🎯 Campaigns Used", filtered_df['campaign_name'].nunique())



# ───── Ratio Indicators with Numeric Values ─────
r1, r2 = st.columns(2)

with r1:
    equity_ratio = 0.7538
    st.subheader("📈 Equity Ratio")
    st.progress(equity_ratio)
    st.write(f"**{equity_ratio * 100:.1f}%**")  # Display as percent

with r2:
    debt_equity_ratio = 0.011
    st.subheader("🏦 Debt Equity Ratio")
    st.progress(debt_equity_ratio)
    st.write(f"**{debt_equity_ratio * 100:.1f}%**")  # Display as percent



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


# ───── Revenue Trend Over Time ─────

st.subheader("📈 Daily Revenue Trend by Campaign")

if "event_date" in filtered_df.columns:
    filtered_df["day"] = filtered_df["event_date"].dt.date

    daily_rev_campaign = (
        filtered_df.groupby(["day", "campaign_name"])["total_revenue"]
        .sum()
        .reset_index()
        .sort_values("day")
    )

    fig = px.line(
        daily_rev_campaign,
        x="day",
        y="total_revenue",
        color="campaign_name",
        markers=True,
        title="📈 Daily Revenue Trend by Campaign",
        labels={
            "day": "Date",
            "total_revenue": "Revenue ($)",
            "campaign_name": "Campaign"
        },
        template="plotly_white"
    )

    fig.update_layout(
        height=400,
        title_font_size=16,
        xaxis_title="Date",
        yaxis_title="Revenue ($)",
        margin=dict(t=40, b=10, l=10, r=10),
        xaxis_tickformat="%b %d, %Y",  # e.g. Jul 16, 2025
        xaxis_tickangle=-30,
        legend_title_text="Campaign",
        font=dict(size=12),
    )
    fig.update_traces(line=dict(width=2))
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("📅 No 'event_date' column found to generate daily revenue trend.")
#----------------------------------------
# 📈 Cumulative Revenue Trend

st.subheader("💹 Cumulative Revenue Over Time")

if "event_date" in filtered_df.columns:
    filtered_df["day"] = filtered_df["event_date"].dt.date

    daily_revenue = (
        filtered_df.groupby("day")["total_revenue"]
        .sum()
        .reset_index()
        .sort_values("day")
    )
    daily_revenue["cumulative_revenue"] = daily_revenue["total_revenue"].cumsum()

    fig = px.line(
        daily_revenue,
        x="day",
        y="cumulative_revenue",
        title="💹 Cumulative Revenue Over Time",
        markers=True,
        labels={"day": "Date", "cumulative_revenue": "Cumulative Revenue ($)"},
        template="plotly_white"
    )

    fig.update_traces(line=dict(color="#0077b6", width=2))
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Cumulative Revenue ($)",
        xaxis_tickformat="%b %d, %Y",
        xaxis_tickangle=-30,
        height=350,
        title_font_size=16,
        font=dict(size=12),
        margin=dict(t=40, b=10, l=10, r=10),
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("📅 No 'event_date' column found to generate cumulative trend.")


#--------------------------


import plotly.express as px

# Group and calculate daily revenue
filtered_df["day"] = filtered_df["event_date"].dt.date
daily_revenue = (
    filtered_df.groupby("day")["total_revenue"]
    .sum()
    .reset_index()
    .sort_values("day")
)

# Cumulative sum
daily_revenue["cumulative_revenue"] = daily_revenue["total_revenue"].cumsum()

# Plotly line chart
fig = px.line(
    daily_revenue,
    x="day",
    y="cumulative_revenue",
    title="📈 Cumulative Revenue Over Time",
    labels={
        "day": "Date",
        "cumulative_revenue": "Cumulative Revenue ($)"
    },
    markers=True,
    template="plotly_white"
)

# Optional styling
fig.update_layout(
    height=400,
    title_font_size=16,
    margin=dict(t=40, b=10, l=10, r=10),
    xaxis_tickangle=-45,
    xaxis_title="Date",
    yaxis_title="Cumulative Revenue ($)",
    hovermode="x unified"
)
fig.update_traces(line=dict(color="#0077b6", width=2))

# Show in Streamlit
st.plotly_chart(fig, use_container_width=True)
#------------------------------------
# 📈 Monthly Playtime by Campaign


with g2:
    st.subheader("📈 Monthly Playtime by Campaign")

    if "event_date" in filtered_df.columns:
        # Extract month
        filtered_df["month"] = filtered_df["event_date"].dt.to_period("M").astype(str)

        # Group and aggregate
        monthly = (
            filtered_df.groupby(["month", "campaign_name"])["total_playtime"]
            .sum()
            .reset_index()
        )

        # Plot with Plotly
        fig = px.line(
            monthly,
            x="month",
            y="total_playtime",
            color="campaign_name",
            markers=True,
            labels={
                "month": "Month",
                "total_playtime": "Playtime (min)",
                "campaign_name": "Campaign"
            },
            title="📈 Monthly Playtime by Campaign",
        )

        fig.update_layout(
            height=400,
            title_font_size=16,
            xaxis_tickangle=-45,
            margin=dict(t=40, b=10, l=10, r=10),
        )
        fig.update_traces(line=dict(width=2))

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("📅 No 'event_date' column found to generate monthly trend.")

        #-------------------
import plotly.graph_objects as go

def plot_gauge(title, value, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value * 100,
        number={'suffix': " %", 'font': {'size': 28}},
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 16}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': color},
            'bgcolor': "white",
            'steps': [
                {'range': [0, 25], 'color': '#f2f2f2'},
                {'range': [25, 50], 'color': '#d9d9d9'},
                {'range': [50, 75], 'color': '#bfbfbf'},
                {'range': [75, 100], 'color': '#a6a6a6'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 2},
                'thickness': 0.75,
                'value': value * 100
            }
        }
    ))
    fig.update_layout(margin=dict(t=30, b=10, l=10, r=10), height=250)
    return fig