import warnings
warnings.simplefilter("ignore")

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from createData import initialize_views
from readData import (
    get_daily_counts,
    get_weekly_counts,
    get_daily_details,
    get_weekly_details,
)

@st.cache_resource
def bootstrap_project():
    """
    Runs once when Streamlit server starts.
    Creates/updates DB views before UI loads.
    """
    initialize_views()
    return True

bootstrap_project()

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="SNU Site Monitoring Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------
# DARK THEME / GLOBAL CSS + ENHANCED KPI STYLES
# --------------------------------------------------
st.markdown(
    """
<style>
/* App background */
.stApp {
    background: radial-gradient(circle at top, #111827 0%, #020617 55%, #000000 100%);
    color: #e5e7eb;
}

/* Main container */
.block-container {
    padding-top: 0.6rem;
    padding-bottom: 0.2rem;
    max-width: 96%;
}

/* Typography */
h1, h2, h3 {
    color: #f9fafb;
    letter-spacing: 0.03em;
}

/* Generic card */
.card {
    background: #020617e6;
    border-radius: 14px;
    border: 1px solid #111827;
    padding: 18px 20px;
    box-shadow: 0 18px 40px rgba(15, 23, 42, 0.65);
}

/* Chart container */
div[data-testid="stPlotlyChart"] {
    background: #020617e6;
    border-radius: 14px;
    padding: 12px 14px;
    border: 1px solid #111827;
    box-shadow: 0 18px 40px rgba(15, 23, 42, 0.65);
}

/* Dataframe container */
[data-testid="stDataFrame"] {
    background: #020617e6;
    border-radius: 14px;
    border: 1px solid #111827;
    box-shadow: 0 18px 40px rgba(15, 23, 42, 0.65);
}

/* KPI buttons – ENHANCED PROFESSIONAL CARD STYLE */
.kpi-container {
    position: relative;
    border-radius: 16px;
    border: 1px solid #1f2937;
    background: radial-gradient(circle at top, #020617, #020617f2);
    height: 96px;
    padding: 12px 12px 10px 12px;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.7);
    transition: all 160ms ease-out;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 6px;
}

/* Selected KPI state */
.kpi-container.selected {
    background: radial-gradient(circle at top left, #1d4ed8, #0f766e) !important;
    border-color: #60a5fa !important;
    box-shadow: 0 18px 40px rgba(37, 99, 235, 0.5);
    transform: translateY(-1px);
}

/* Hover state */
.kpi-container:hover {
    border-color: #60a5fa;
    box-shadow: 0 14px 30px rgba(37, 99, 235, 0.3);
    transform: translateY(-2px);
}

/* Top accent bar */
.kpi-accent {
    width: 100%;
    height: 3px;
    border-radius: 999px;
    background: linear-gradient(90deg, #3b82f6, #22c55e);
    opacity: 0.9;
}

/* Selected accent */
.kpi-container.selected .kpi-accent {
    background: linear-gradient(90deg, #22c55e, #a855f7);
}

/* KPI label */
.kpi-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #9ca3af;
    font-weight: 600;
}

/* Selected label */
.kpi-container.selected .kpi-label {
    color: #cbd5f5;
}

/* KPI value */
.kpi-value {
    font-size: 24px;
    font-weight: 700;
    color: #f9fafb;
    margin-top: -2px;
}

/* Pagination buttons */
.pagination-btn > button {
    border-radius: 999px !important;
    border: 1px solid #374151 !important;
    background: #020617 !important;
    color: #e5e7eb !important;
    font-size: 13px !important;
    padding: 0.25rem 0.75rem !important;
    transition: all 150ms ease-out !important;
}
.pagination-btn > button:hover {
    border-color: #60a5fa !important;
    background: #020617e6 !important;
}

/* Date input */
[data-testid="stDateInput"] input {
    background-color: #020617 !important;
    color: #e5e7eb !important;
    border-radius: 8px !important;
    border: 1px solid #374151 !important;
}

/* Helper text */
.helper-text {
    font-size: 12px;
    color: #9ca3af;
}

/* Section titles */
.section-title {
    font-size: 14px;
    font-weight: 600;
}

/* Header right alignment */
.header-right > div:first-child {
    padding-top: 0.6rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
top_col1, top_col2 = st.columns([3, 1])

with top_col1:
    st.markdown(
        """
        <h2 style="
            font-weight: 600;
            margin-top: 0.4rem;
            margin-bottom: 0.15rem;
        ">
            SNU Site Monitoring Dashboard
        </h2>
        <div class="helper-text">
            Track site outage aging and quickly drill into affected sites for daily and weekly windows.
        </div>
        """,
        unsafe_allow_html=True,
    )

with top_col2:
    with st.container():
        st.markdown('<div class="header-right">', unsafe_allow_html=True)
        selected_date = st.date_input(
            "Reference Date",
            help="Select the reference date to load daily and weekly site aging metrics.",
        )
        st.markdown("</div>", unsafe_allow_html=True)

if not selected_date:
    st.stop()

selected_date_str = str(selected_date)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
with st.spinner("Loading site aging data..."):
    daily_counts_df = get_daily_counts(selected_date_str)
    weekly_counts_df = get_weekly_counts(selected_date_str)
    daily_details_df = get_daily_details(selected_date_str)
    weekly_details_df = get_weekly_details(selected_date_str)

# --------------------------------------------------
# NO DATA HANDLING
# --------------------------------------------------
def is_empty(df: pd.DataFrame | None) -> bool:
    return df is None or df.empty

if (
    is_empty(daily_counts_df)
    or is_empty(weekly_counts_df)
    or is_empty(weekly_details_df)
):
    st.markdown(
        """
        <div class="card" style="text-align:center; font-size:18px; font-weight:600;">
            No data available for the selected date.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# --------------------------------------------------
# TRANSFORM DATA
# --------------------------------------------------
daily_counts_df = daily_counts_df.melt(
    id_vars=["ref_date"],
    value_vars=["day1", "day2", "day3", "day4", "day5", "day6", "day7"],
    var_name="aging_bucket",
    value_name="sitecount",
)

weekly_counts_df = weekly_counts_df.melt(
    id_vars=["ref_date"],
    value_vars=["w1", "w2", "w3", "w4", "w5"],
    var_name="aging_bucket",
    value_name="sitecount",
)

bucket_map = {
    "w1": "<week1",
    "w2": ">week1&<week2",
    "w3": ">week2&<week3",
    "w4": ">week3&<week4",
    "w5": ">week4",
}
weekly_counts_df["aging_bucket"] = weekly_counts_df["aging_bucket"].map(bucket_map)

bucket_order = ["<week1", ">week1&<week2", ">week2&<week3", ">week3&<week4", ">week4"]
weekly_counts_df["aging_bucket"] = pd.Categorical(
    weekly_counts_df["aging_bucket"], categories=bucket_order, ordered=True
)
weekly_counts_df = weekly_counts_df.sort_values("aging_bucket")

daily_counts_df["aging_bucket"] = pd.Categorical(
    daily_counts_df["aging_bucket"],
    categories=["day1", "day2", "day3", "day4", "day5", "day6", "day7"],
    ordered=True,
)
daily_counts_df = daily_counts_df.sort_values("aging_bucket")

# --------------------------------------------------
# SUMMARY KPIs ROW
# --------------------------------------------------
total_daily = int(daily_counts_df["sitecount"].sum())
total_weekly = int(weekly_counts_df["sitecount"].sum())

k1, k2, k3 = st.columns([1.1, 1.1, 1])

with k1:
    st.markdown(
        f"""
        <div class="card">
            <div style="font-size:13px; text-transform:uppercase; color:#9ca3af;">
                Total Daily Sites
            </div>
            <div style="font-size:26px; font-weight:700; margin-top:4px;">
                {total_daily}
            </div>
            <div class="helper-text" style="margin-top:2px;">
                Sum of all day buckets for the selected date.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k2:
    st.markdown(
        f"""
        <div class="card">
            <div style="font-size:13px; text-transform:uppercase; color:#9ca3af;">
                Total Weekly Sites
            </div>
            <div style="font-size:26px; font-weight:700; margin-top:4px;">
                {total_weekly}
            </div>
            <div class="helper-text" style="margin-top:2px;">
                Sum of all weekly aging buckets.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k3:
    st.markdown(
        """
        <div class="card">
            <div style="font-size:13px; text-transform:uppercase; color:#9ca3af;">
                How to Use
            </div>
            <div style="font-size:13px; margin-top:4px; line-height:1.4;">
                1. Change the reference date on the top-right.<br>
                2. Use weekly aging cards below to filter sites.<br>
                3. Scroll the table or navigate pages via Prev / Next.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# CHARTS
# --------------------------------------------------
st.markdown(
    '<div style="margin-top:0.6rem; margin-bottom:0.2rem;" class="section-title">Aging Trends</div>',
    unsafe_allow_html=True,
)

c1, c2 = st.columns(2)

with c1:
    fig1 = go.Figure()
    fig1.add_trace(
        go.Scatter(
            x=daily_counts_df["aging_bucket"],
            y=daily_counts_df["sitecount"],
            mode="lines+markers+text",
            text=daily_counts_df["sitecount"],
            textposition="top center",
            cliponaxis=False,
            textfont=dict(color="#f9fafb", size=11),
            line=dict(width=3, color="#3b82f6"),
            fill="tozeroy",
            fillcolor="rgba(59,130,246,0.15)",
        )
    )
    fig1.update_layout(
        title=dict(text="Daily Aging (Day-wise)", x=0.02, xanchor="left", font=dict(size=14, color="#e5e7eb")),
        xaxis=dict(title="Day Buckets", showgrid=False),
        yaxis=dict(title="Site Count", gridcolor="#1f2933"),
        height=260,
        plot_bgcolor="#020617",
        paper_bgcolor="#020617",
        font=dict(color="#e5e7eb"),
        showlegend=False,
        margin=dict(l=60, r=40, t=60, b=40),
    )
    st.plotly_chart(fig1, width="stretch")

with c2:
    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(
            x=weekly_counts_df["aging_bucket"],
            y=weekly_counts_df["sitecount"],
            mode="lines+markers+text",
            text=weekly_counts_df["sitecount"],
            textposition="top center",
            cliponaxis=False,
            textfont=dict(color="#f9fafb", size=11),
            line=dict(width=3, color="#10b981"),
            fill="tozeroy",
            fillcolor="rgba(16,185,129,0.15)",
        )
    )
    fig2.update_layout(
        title=dict(text="Weekly Aging (Weeks)", x=0.02, xanchor="left", font=dict(size=14, color="#e5e7eb")),
        xaxis=dict(title="Week Buckets", showgrid=False),
        yaxis=dict(title="Site Count", gridcolor="#1f2933"),
        height=260,
        plot_bgcolor="#020617",
        paper_bgcolor="#020617",
        font=dict(color="#e5e7eb"),
        showlegend=False,
        margin=dict(l=60, r=40, t=60, b=40),
    )
    st.plotly_chart(fig2, width="stretch")

# --------------------------------------------------
# WEEKLY KPI CARDS (INITIALIZED VERSION)
# --------------------------------------------------

# 1. INITIALIZE STATE FIRST (Prevents the AttributeError)
if "selected_bucket" not in st.session_state:
    st.session_state.selected_bucket = "<week1"

# 2. Get the current selected value for the CSS injection
selected_cat = st.session_state.selected_bucket

st.markdown(
    f"""
    <style>
    /* Base Button Style (Unselected) */
    div[data-testid="stColumn"] button {{
        background: radial-gradient(circle at top, #020617, #020617f2) !important;
        border: 1px solid #1f2937 !important;
        border-radius: 16px !important;
        height: 100px !important;
        width: 100% !important;
        padding: 12px !important;
        transition: all 160ms ease-out !important;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.7) !important;
        white-space: pre-wrap !important;
        color: #9ca3af !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        font-size: 11px !important;
        line-height: 1.6 !important;
    }}

    /* DYNAMIC SELECTED STATE: Injecting selected color for the active key */
    /* Target specifically the button whose key matches our selection */
    div[data-testid="stColumn"] button[key="kpi_btn_{selected_cat}"] {{
        background: radial-gradient(circle at top left, #1d4ed8, #0f766e) !important;
        border-color: #60a5fa !important;
        box-shadow: 0 18px 40px rgba(37, 99, 235, 0.5) !important;
        color: #ffffff !important;
        transform: translateY(-1px);
    }}

    /* Hover effect */
    div[data-testid="stColumn"] button:hover {{
        border-color: #60a5fa !important;
        transform: translateY(-2px) !important;
    }}
    </style>
    
    <div style="margin-top:0.6rem; margin-bottom:0.2rem;">
        <span class="section-title">Weekly Aging Buckets</span>
        <span class="helper-text"> &nbsp;• Click a bucket to view sites in that band.</span>
    </div>
    """,
    unsafe_allow_html=True,
)

categories = bucket_order
kpi_cols = st.columns(len(categories), gap="small")

for i, cat in enumerate(categories):
    val = weekly_counts_df.loc[
        weekly_counts_df["aging_bucket"] == cat, "sitecount"
    ].sum()

    display_text = f"{cat}\n{int(val)}"

    with kpi_cols[i]:
        if st.button(display_text, key=f"kpi_btn_{cat}", width="stretch"):
            st.session_state.selected_bucket = cat
            st.session_state.page = 1
            st.rerun()

selected_bucket = st.session_state.selected_bucket

# --------------------------------------------------
# TABLE WITH PAGINATION
# --------------------------------------------------
ROWS_PER_PAGE = 10

st.markdown(
    f"""
    <div style="margin-top:0.8rem; margin-bottom:0.2rem;">
        <span class="section-title">Sites in Weekly Bucket: {selected_bucket}</span>
        <span class="helper-text"> &nbsp;({ROWS_PER_PAGE} per page)</span>
    </div>
    """,
    unsafe_allow_html=True,
)

filtered_df = (
    weekly_details_df[weekly_details_df["aging_bucket"] == selected_bucket][
        ["smsitecode", "smsitename"]
    ]
    .reset_index(drop=True)
)

if "page" not in st.session_state:
    st.session_state.page = 1

total_pages = max(1, (len(filtered_df) - 1) // ROWS_PER_PAGE + 1)
st.session_state.page = min(st.session_state.page, total_pages)

start = (st.session_state.page - 1) * ROWS_PER_PAGE
end = start + ROWS_PER_PAGE
page_df = filtered_df.iloc[start:end]

st.dataframe(
    page_df,
    width="stretch",
    hide_index=True,
)

# --------------------------------------------------
# INLINE CENTERED PAGINATION
# --------------------------------------------------
left, center, right = st.columns([3, 2, 3])

with center:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        with st.container():
            st.markdown('<div class="pagination-btn">', unsafe_allow_html=True)
            if st.button("⬅ Prev", key="prev", width="stretch"):
                if st.session_state.page > 1:
                    st.session_state.page -= 1
            st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown(
            f"""
            <div style="text-align:center;font-weight:600;padding-top:6px; font-size:13px;">
                Page {st.session_state.page} / {total_pages}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        with st.container():
            st.markdown('<div class="pagination-btn">', unsafe_allow_html=True)
            if st.button("Next ➡", key="next", width="stretch"):
                if st.session_state.page < total_pages:
                    st.session_state.page += 1
            st.markdown("</div>", unsafe_allow_html=True)