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
# BOOTSTRAP
# --------------------------------------------------
@st.cache_resource
def bootstrap_project():
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
# GLOBAL CSS (FINAL)
# --------------------------------------------------
st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at top,#111827 0%,#020617 55%,#000000 100%);
    color:#e5e7eb;
}

.block-container{
    padding-top:0.6rem;
    padding-bottom:0.2rem;
    max-width:96%;
}

.card{
    background:#020617e6;
    border-radius:14px;
    border:1px solid #111827;
    padding:18px 20px;
    box-shadow:0 18px 40px rgba(15,23,42,0.65);
}

/* FULL SIZE CHARTS */
div[data-testid="stPlotlyChart"]{
    background:#020617e6;
    border-radius:14px;
    padding:6px 6px;
    border:1px solid #111827;
    box-shadow:0 18px 40px rgba(15,23,42,0.65);
    overflow:hidden !important;
}

/* SMALL HELP ICON */
[data-testid="stTooltipIcon"]{
    transform:scale(0.7);
    margin-left:4px!important;
}
[data-testid="stTooltipIcon"] svg{
    width:14px!important;
    height:14px!important;
}

/* COMPACT TOOLBAR */
div[data-testid="stPlotlyChart"] .modebar{
    transform:scale(0.65);
    transform-origin:top right;
}
div[data-testid="stPlotlyChart"] .modebar-btn{
    padding:2px!important;
    margin:0!important;
    border-radius:6px!important;
}
div[data-testid="stPlotlyChart"] .modebar-btn svg{
    width:14px!important;
    height:14px!important;
}

/* -------------------------------------------------- */
/* KPI BUTTONS ONLY — STACKED STYLE (SCOPED) */
/* -------------------------------------------------- */

.kpi-row button {
    height:92px !important;
    display:flex !important;
    flex-direction:column !important;
    justify-content:center !important;
    align-items:center !important;
    white-space:pre-wrap !important;
    line-height:1.2 !important;
    text-align:center !important;
    border-radius:14px !important;
}

.kpi-row button p{
    margin:0 !important;
}

.kpi-row button p:first-child{
    font-size:11px !important;
    color:#9ca3af !important;
    text-transform:uppercase !important;
    letter-spacing:0.05em !important;
}

.kpi-row button p:last-child{
    font-size:24px !important;
    font-weight:700 !important;
    color:#f9fafb !important;
}

.helper-text{
    font-size:12px;
    color:#9ca3af;
}

.section-title{
    font-size:14px;
    font-weight:600;
}

.header-right > div:first-child{
    padding-top:0.6rem;
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
        <div class="helper-text">
            Track site outage aging and quickly drill into affected sites.
        </div>
    """, unsafe_allow_html=True)

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

def is_empty(df):
    return df is None or df.empty

if (
    is_empty(daily_counts_df)
    or is_empty(weekly_counts_df)
    or is_empty(weekly_details_df)
):
    st.markdown(
        '<div class="card" style="text-align:center;font-size:18px;font-weight:600;">No data available for the selected date.</div>',
        unsafe_allow_html=True,
    )
    st.stop()

# --------------------------------------------------
# TRANSFORM DATA
# --------------------------------------------------
daily_counts_df = daily_counts_df.melt(
    id_vars=["ref_date"],
    value_vars=["day1","day2","day3","day4","day5","day6","day7"],
    var_name="aging_bucket",
    value_name="sitecount",
)

weekly_counts_df = weekly_counts_df.melt(
    id_vars=["ref_date"],
    value_vars=["w1","w2","w3","w4","w5"],
    var_name="aging_bucket",
    value_name="sitecount",
)

bucket_map={
    "w1":"<week1",
    "w2":">week1&<week2",
    "w3":">week2&<week3",
    "w4":">week3&<week4",
    "w5":">week4",
}
weekly_counts_df["aging_bucket"]=weekly_counts_df["aging_bucket"].map(bucket_map)

bucket_order=["<week1",">week1&<week2",">week2&<week3",">week3&<week4",">week4"]

# --------------------------------------------------
# CHARTS
# --------------------------------------------------

c1,c2 = st.columns(2)

with c1:
    st.markdown(
    '<div style="margin-top:0.6rem;margin-bottom:0.2rem;" class="section-title">Daily Aging Trends</div>',
    unsafe_allow_html=True,
    )
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
        autosize=True,
        height=None,
        plot_bgcolor="#020617",
        paper_bgcolor="#020617",
        font=dict(color="#e5e7eb"),
        showlegend=False,
        margin=dict(l=70,r=70,t=50,b=45),
    )
    st.plotly_chart(fig1,use_container_width=True,config=PLOTLY_CONFIG)

with c2:
    st.markdown(
    '<div style="margin-top:0.6rem;margin-bottom:0.2rem;" class="section-title">Weekly Aging Trends</div>',
    unsafe_allow_html=True,
    )
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
        autosize=True,
        height=None,
        plot_bgcolor="#020617",
        paper_bgcolor="#020617",
        font=dict(color="#e5e7eb"),
        showlegend=False,
        margin=dict(l=70,r=70,t=50,b=45),
    )
    st.plotly_chart(fig2,use_container_width=True,config=PLOTLY_CONFIG)

# --------------------------------------------------
# KPI BUTTONS (FINAL)
# --------------------------------------------------
if "selected_bucket" not in st.session_state:
    st.session_state.selected_bucket="<week1"

selected_cat = st.session_state.selected_bucket

st.markdown('<div class="kpi-row">', unsafe_allow_html=True)

kpi_cols = st.columns(len(bucket_order),gap="small")

for i,cat in enumerate(bucket_order):

    val = weekly_counts_df.loc[
        weekly_counts_df["aging_bucket"]==cat,"sitecount"
    ].sum()

    safe_cat = cat.replace("<","&lt;").replace(">","&gt;")
    display_text=f"{safe_cat}  \n{int(val)}"

    with kpi_cols[i]:
        if st.button(display_text,key=f"kpi_btn_{cat}",use_container_width=True):
            st.session_state.selected_bucket=cat
            st.session_state.page=1
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

selected_bucket=st.session_state.selected_bucket

# --------------------------------------------------
# TABLE + PAGINATION
# --------------------------------------------------
ROWS_PER_PAGE=10

filtered_df=(
    weekly_details_df[weekly_details_df["aging_bucket"]==selected_bucket]
    [["smsitecode","smsitename"]]
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

    with c2:
        st.markdown(
            f'<div style="text-align:center;font-weight:600;padding-top:6px;font-size:13px;">Page {st.session_state.page} / {total_pages}</div>',
            unsafe_allow_html=True,
        )

    with c3:
        if st.button("Next ➡",use_container_width=True):
            if st.session_state.page<total_pages:
                st.session_state.page+=1