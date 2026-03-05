import warnings
warnings.simplefilter("ignore")

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timezone
from readData import (getAgingBucketCounts,getAgingBucketDetails)

# --------------------------------------------------
# GLOBAL PLOTLY CONFIG
# --------------------------------------------------
PLOTLY_CONFIG = {
    "displaylogo": False,
    "modeBarButtonsToRemove": [
        "zoom","pan","select","lasso2d",
        "zoomIn2d","zoomOut2d","autoScale2d","toggleSpikelines"
    ],
}

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="SNU Site Monitoring Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------
# CSS
# --------------------------------------------------
st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at top,#111827 0%,#020617 55%,#000000 100%);
    color:#e5e7eb;
}

.block-container{
    padding-top:1.5rem;
    padding-bottom:0.2rem;
    max-width:96%;
}

.card{
    background:#020617e6;
    border-radius:14px;
    border:1px solid #111827;
    padding:18px 20px;
}

.kpi-row button {
    height:92px !important;
    display:flex !important;
    flex-direction:column !important;
    justify-content:center !important;
    align-items:center !important;
    white-space:pre-wrap !important;
}

.section-title{
    font-size:14px;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
top_col1, top_col2 = st.columns([3,1])

with top_col1:
    st.markdown("""
        <h2 style="font-weight:600;margin-top:0.4rem;margin-bottom:0.15rem;">
            SNU Site Monitoring Dashboard
        </h2>
    """, unsafe_allow_html=True)

with top_col2:
    selected_date = st.date_input("Reference Date")

if not selected_date:
    st.stop()

reference_ts = int(
    datetime(
        selected_date.year,
        selected_date.month,
        selected_date.day,
        tzinfo=timezone.utc
    ).timestamp()
)

# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------
@st.cache_data
def load_data(reference_ts):
    counts = getAgingBucketCounts(reference_ts)
    details = getAgingBucketDetails(reference_ts)
    return counts, details

counts_df, details_df = load_data(reference_ts)

if counts_df.empty or details_df.empty:
    st.markdown(
        '<div class="card">No data available for the selected date.</div>',
        unsafe_allow_html=True,
    )
    st.stop()

# --------------------------------------------------
# DATA TRANSFORM
# --------------------------------------------------
daily_counts_df = counts_df.melt(
    id_vars=["refTimeStamp"],
    value_vars=["day1","day2","day3","day4","day5","day6","day7"],
    var_name="aging_bucket",
    value_name="sitecount",
)

weekly_counts_df = counts_df.melt(
    id_vars=["refTimeStamp"],
    value_vars=["week1","week2","week3","week4","week5"],
    var_name="aging_bucket",
    value_name="sitecount",
)

bucket_map={
    "week1":"<week1",
    "week2":">week1&<week2",
    "week3":">week2&<week3",
    "week4":">week3&<week4",
    "week5":">week4",
}

weekly_counts_df["aging_bucket"]=weekly_counts_df["aging_bucket"].map(bucket_map)

bucket_order=["<week1",">week1&<week2",">week2&<week3",">week3&<week4",">week4"]

# --------------------------------------------------
# CHARTS
# --------------------------------------------------
c1,c2 = st.columns(2)

with c1:

    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(
        x=daily_counts_df["aging_bucket"],
        y=daily_counts_df["sitecount"],
        mode="lines+markers+text",
        text=daily_counts_df["sitecount"],
        textposition="top center",
        cliponaxis=False,
        line=dict(width=3,color="#3b82f6"),
        fill="tozeroy",
        fillcolor="rgba(59,130,246,0.15)",
    ))

    fig1.update_layout(
        plot_bgcolor="#020617",
        paper_bgcolor="#020617",
        font=dict(color="#e5e7eb"),
        showlegend=False,
        margin=dict(l=80, r=80, t=30, b=40)
    )

    st.plotly_chart(fig1,use_container_width=True,config=PLOTLY_CONFIG)

with c2:

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=weekly_counts_df["aging_bucket"],
        y=weekly_counts_df["sitecount"],
        mode="lines+markers+text",
        text=weekly_counts_df["sitecount"],
        textposition="top center",
        cliponaxis=False,
        line=dict(width=3,color="#10b981"),
        fill="tozeroy",
        fillcolor="rgba(16,185,129,0.15)",
    ))

    fig2.update_layout(
        plot_bgcolor="#020617",
        paper_bgcolor="#020617",
        font=dict(color="#e5e7eb"),
        showlegend=False,
        margin=dict(l=80, r=80, t=30, b=40)
    )

    st.plotly_chart(fig2,use_container_width=True,config=PLOTLY_CONFIG)

# --------------------------------------------------
# KPI BUTTONS
# --------------------------------------------------
if "selected_bucket" not in st.session_state:
    st.session_state.selected_bucket="<week1"

st.markdown('<div class="kpi-row">', unsafe_allow_html=True)

kpi_cols = st.columns(len(bucket_order))

for i,cat in enumerate(bucket_order):

    val = weekly_counts_df.loc[
        weekly_counts_df["aging_bucket"]==cat,"sitecount"
    ].sum()

    display_text=f"{cat}  \n{int(val)}"

    with kpi_cols[i]:
        if st.button(display_text,key=f"kpi_btn_{cat}",use_container_width=True):
            st.session_state.selected_bucket=cat
            st.session_state.page=1
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

selected_bucket=st.session_state.selected_bucket

reverse_bucket_map = {
    "<week1": "week1",
    ">week1&<week2": "week2",
    ">week2&<week3": "week3",
    ">week3&<week4": "week4",
    ">week4": "week5",
}

db_bucket = reverse_bucket_map[selected_bucket]

# --------------------------------------------------
# TABLE CONTAINER (BEST UX)
# --------------------------------------------------
table_container = st.container()

with table_container:

    ROWS_PER_PAGE=10

    filtered_df = (
        details_df[details_df["weeklyBucket"] == db_bucket]
        [["smSiteCode", "smSiteName"]]
        .reset_index(drop=True)
    )

    if "page" not in st.session_state:
        st.session_state.page=1

    total_pages=max(1,(len(filtered_df)-1)//ROWS_PER_PAGE+1)

    st.session_state.page=min(st.session_state.page,total_pages)

    start=(st.session_state.page-1)*ROWS_PER_PAGE
    end=start+ROWS_PER_PAGE

    page_df=filtered_df.iloc[start:end]

    st.dataframe(page_df,use_container_width=True,hide_index=True)

    left,center,right=st.columns([3,2,3])

    with center:

        c1,c2,c3=st.columns([1,2,1])

        with c1:
            if st.button("⬅ Prev",use_container_width=True):
                if st.session_state.page>1:
                    st.session_state.page-=1
                    st.rerun()

        with c2:
            st.markdown(
                f'<div style="text-align:center;font-weight:600;padding-top:6px;font-size:13px;">Page {st.session_state.page} / {total_pages}</div>',
                unsafe_allow_html=True,
            )

        with c3:
            if st.button("Next ➡",use_container_width=True):
                if st.session_state.page<total_pages:
                    st.session_state.page+=1
                    st.rerun()
