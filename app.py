import textwrap

import streamlit as st
import pandas as pd
import plotly.express as px
import textwrap

from scoring_engine import (
    calculate_risk_score,
    get_priority,
    get_score_breakdown
)



# App page setup


st.set_page_config(
    page_title="Security Alert Prioritization",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)



# Styling tweaks for the dashboard look and feel


st.markdown(
    """
    <style>

    /* Main page */
    .stApp {
        background-color: #0e1117;
    }

    [data-testid="stAppViewContainer"] .main .block-container {
        padding-top: 0.35rem !important;
    }

    .main-header {
        padding: 0 0 4px 0;
    }

    /* Header */
    .main-title {
        font-size: 38px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }

    .main-subtitle {
        color: #9ca3af;
        font-size: 15px;
        margin-bottom: 20px;
    }

    /* KPI Cards */
    .metric-card {
        background: #171b24;
        border: 1px solid #262c38;
        border-radius: 10px;
        padding: 16px 18px;
        min-height: 105px;
    }

    .metric-label {
        color: #9ca3af;
        font-size: 13px;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 650;
    }

    .critical-value {
        color: #ff5c5c;
    }

    .high-value {
        color: #ff9f43;
    }

    .medium-value {
        color: #f6c85f;
    }

    .low-value {
        color: #55d68a;
    }

    /* Section headers */
    .section-title {
        font-size: 20px;
        font-weight: 650;
        margin-top: 8px;
        margin-bottom: 12px;
    }

    /* Top alert card */
    .top-alert {
        background: #151922;
        border: 1px solid #292f3b;
        border-radius: 9px;
        padding: 13px 16px;
        margin-bottom: 8px;
    }

    .alert-id {
        font-weight: 650;
        font-size: 15px;
    }

    .alert-type {
        color: #d1d5db;
        font-size: 14px;
    }

    .alert-asset {
        color: #9ca3af;
        font-size: 13px;
    }

    /* Risk badge */
    .risk-badge {
        display: inline-block;
        padding: 4px 9px;
        border-radius: 5px;
        font-size: 12px;
        font-weight: 650;
    }

    .critical-badge {
        background: #3a171b;
        color: #ff6b6b;
    }

    .high-badge {
        background: #3a2816;
        color: #ffad5c;
    }

    .medium-badge {
        background: #393117;
        color: #f6ce67;
    }

    .low-badge {
        background: #143022;
        color: #61d995;
    }

    /* Info box */
    .methodology-box {
        background: #151922;
        border: 1px solid #292f3b;
        border-radius: 10px;
        padding: 18px 20px;
        margin-top: 10px;
    }

    .methodology-item {
        margin-bottom: 7px;
        color: #d1d5db;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #11151d;
        border-right: 1px solid #252b35;
        padding-top: 14px;
    }

    section[data-testid="stSidebar"] > div:first-child {
        padding-left: 8px;
        padding-right: 8px;
    }

    section[data-testid="stSidebar"] .stMarkdown h2 {
        font-size: 25px;
        font-weight: 700;
        letter-spacing: -0.2px;
        margin-bottom: 10px;
        color: #f2f4f7;
    }

    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stCaption {
        color: #98a4b7;
        font-size: 13px;
    }

    section[data-testid="stSidebar"] label {
        font-weight: 600;
        color: #e6ebf2;
    }

    section[data-testid="stSidebar"] .stTextInput > div,
    section[data-testid="stSidebar"] .stSelectbox > div,
    section[data-testid="stSidebar"] .stMultiSelect > div {
        background: #141b27;
        border: 1px solid #2b3545;
        border-radius: 12px;
        box-shadow: none;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    section[data-testid="stSidebar"] .stTextInput > div:focus-within,
    section[data-testid="stSidebar"] .stSelectbox > div:focus-within,
    section[data-testid="stSidebar"] .stMultiSelect > div:focus-within {
        border-color: #4e617d;
        box-shadow: 0 0 0 1px rgba(78, 97, 125, 0.35);
    }

    section[data-testid="stSidebar"] .stTextInput input,
    section[data-testid="stSidebar"] .stSelectbox div[role="button"],
    section[data-testid="stSidebar"] .stMultiSelect div[role="button"] {
        color: #f3f5f8;
        background: transparent;
        border: none;
    }

    section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
        background: #2a3344;
        border: 1px solid #3a465a;
        border-radius: 8px;
        padding: 4px 9px;
        margin: 2px;
    }

    section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] span {
        color: #dde5f1;
        font-weight: 550;
    }

    section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] svg {
        color: #aeb9c8;
    }

    section[data-testid="stSidebar"] .stSlider {
        margin-top: 10px;
    }

    section[data-testid="stSidebar"] .stSlider .MuiSlider-thumb {
        color: #ff6b6b;
        box-shadow: 0 0 0 4px rgba(255, 107, 107, 0.18);
    }

    section[data-testid="stSidebar"] .stSlider .MuiSlider-rail {
        background: #374151;
    }

    section[data-testid="stSidebar"] .stSlider .MuiSlider-track {
        background: linear-gradient(90deg, #44d19d, #ff6b6b);
    }

    /* Dividers */
    hr {
        border-color: #272d38;
    }

    </style>
    """,
    unsafe_allow_html=True
)



# Read alert data from CSV


df = pd.read_csv("data/alerts.csv")



# Compute score and priority for each alert


df["risk_score"] = df.apply(
    calculate_risk_score,
    axis=1
)

df["priority"] = df["risk_score"].apply(
    get_priority
)

df = df.sort_values(
    by="risk_score",
    ascending=False
).reset_index(drop=True)



# Main heading


st.markdown(
    """
    <div class="main-header">
        <div class="main-title">🛡️ Security Alert Prioritization</div>
        <div class="main-subtitle">
            Risk-based ranking of security alerts using severity,
            asset importance, and event context.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)



# KPI counts used in summary cards


total_alerts = len(df)

critical_count = len(
    df[df["priority"] == "CRITICAL"]
)

high_count = len(
    df[df["priority"] == "HIGH"]
)

medium_count = len(
    df[df["priority"] == "MEDIUM"]
)

low_count = len(
    df[df["priority"] == "LOW"]
)



# Top summary cards


col1, col2, col3, col4, col5 = st.columns(5)


with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">TOTAL ALERTS</div>
            <div class="metric-value">{total_alerts}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">🔴 CRITICAL</div>
            <div class="metric-value critical-value">
                {critical_count}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">🟠 HIGH</div>
            <div class="metric-value high-value">
                {high_count}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">🟡 MEDIUM</div>
            <div class="metric-value medium-value">
                {medium_count}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col5:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">🟢 LOW</div>
            <div class="metric-value low-value">
                {low_count}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")



# Sidebar filters


with st.sidebar:

    st.markdown("## 🔎 Alert Filters")

    st.caption(
        "Narrow down alerts for investigation."
    )

    search_text = st.text_input(
        "Search",
        placeholder="Alert ID, asset, IP..."
    )

    selected_priority = st.multiselect(
        "Priority",
        options=[
            "CRITICAL",
            "HIGH",
            "MEDIUM",
            "LOW"
        ],
        default=[
            "CRITICAL",
            "HIGH",
            "MEDIUM",
            "LOW"
        ]
    )

    selected_alert_type = st.multiselect(
        "Alert Type",
        options=sorted(
            df["alert_type"].unique()
        ),
        default=sorted(
            df["alert_type"].unique()
        )
    )

    minimum_score = st.slider(
        "Minimum Risk Score",
        min_value=0,
        max_value=100,
        value=0
    )

    st.divider()

    st.caption(
        "20 sample security alerts"
    )



# Apply selected filters


filtered_df = df[
    (df["priority"].isin(selected_priority))
    &
    (df["alert_type"].isin(selected_alert_type))
    &
    (df["risk_score"] >= minimum_score)
]



# Free-text search across key fields


if search_text:

    search_text = search_text.lower()

    search_mask = (
        df["alert_id"].astype(str).str.lower().str.contains(
            search_text,
            na=False
        )
        |
        df["alert_type"].astype(str).str.lower().str.contains(
            search_text,
            na=False
        )
        |
        df["asset"].astype(str).str.lower().str.contains(
            search_text,
            na=False
        )
        |
        df["source_ip"].astype(str).str.lower().str.contains(
            search_text,
            na=False
        )
    )

    filtered_df = filtered_df[
        search_mask.loc[filtered_df.index]
    ]



# Highlight the top five highest-risk alerts


st.markdown(
    '<div class="section-title">🚨 Top Priority Alerts</div>',
    unsafe_allow_html=True
)

top_alerts = df.head(5)
# Full prioritized alert table
for _, alert in top_alerts.iterrows():
    priority = alert["priority"]
    badge_color = {
        "CRITICAL": "#ff4b4b",
        "HIGH": "#ff8c42",
        "MEDIUM": "#fbbf24",
        "LOW": "#36cfc9",
    }.get(priority, "#a8b1c1")

    st.markdown(
        f"""
        <div style="
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 12px;
            background: rgba(15, 23, 42, 0.75);
            padding: 18px 16px;
            margin-bottom: 12px;
        ">
            <div style="display:flex; justify-content:space-between; align-items:center; gap:12px;">
                <div>
                    <div style="font-size: 0.9rem; color: #dfe4ee; font-weight: 600; margin-bottom: 4px;">
                        {alert['alert_id']}
                    </div>
                    <div style="font-size: 1rem; color: #f8f9fb; font-weight: 600; margin-bottom: 4px;">
                        {alert['alert_type']}
                    </div>
                    <div style="font-size: 0.8rem; color: #a7b0c2;">
                        Affected asset: {alert['asset']}
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="
                        display: inline-block;
                        background: {badge_color};
                        color: white;
                        border-radius: 999px;
                        padding: 6px 10px;
                        font-size: 0.7rem;
                        font-weight: 700;
                        letter-spacing: 0.04em;
                        margin-bottom: 8px;
                    ">{priority}</div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: #ffffff;">
                        {alert['risk_score']:.1f}
                    </div>
                    <div style="font-size: 0.7rem; color: #8f96a3;">/100</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# PRIORITIZED ALERT TABLE


st.markdown(
    '<div class="section-title">📋 Prioritized Security Alerts</div>',
    unsafe_allow_html=True
)

if len(filtered_df) > 0:

    display_columns = [
        "alert_id",
        "alert_type",
        "asset",
        "severity",
        "asset_criticality",
        "risk_score",
        "priority"
    ]

    display_df = filtered_df[
        display_columns
    ].copy()

    display_df["risk_score"] = display_df[
        "risk_score"
    ].round(1)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No alerts match the selected filters."
    )



# Analytics section


st.divider()

st.markdown(
    '<div class="section-title">📊 Alert Analytics</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# Priority distribution chart

with col1:

    priority_counts = (
        df["priority"]
        .value_counts()
        .reset_index()
    )

    priority_counts.columns = [
        "priority",
        "count"
    ]

    priority_order = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    priority_palette = {
        "CRITICAL": "#ff4d4d",
        "HIGH": "#ff8c42",
        "MEDIUM": "#f7c948",
        "LOW": "#2ec27e",
    }

    priority_counts = priority_counts[
        priority_counts["priority"].isin(priority_order)
    ].copy()
    priority_counts["priority"] = pd.Categorical(
        priority_counts["priority"],
        categories=priority_order,
        ordered=True,
    )
    priority_counts = priority_counts.sort_values("priority")

    fig_priority = px.pie(
        priority_counts,
        names="priority",
        values="count",
        hole=0.55,
        color_discrete_sequence=[
            priority_palette[p] for p in priority_order if p in priority_counts["priority"].tolist()
        ],
    )

    fig_priority.update_traces(
        textinfo="percent",
        texttemplate="%{percent:.0%}",
        insidetextfont=dict(color="#111111", size=18),
        textfont=dict(color="#111111", size=18 ),
    )

    fig_priority.update_layout(
        title="Priority Distribution",
        template="plotly_dark",
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        ),
        legend_title=""
    )

    st.plotly_chart(
        fig_priority,
        use_container_width=True
    )


# Alert type distribution chart

with col2:

    alert_type_counts = (
        df["alert_type"]
        .value_counts()
        .reset_index()
    )

    alert_type_counts.columns = [
        "alert_type",
        "count"
    ]

    alert_palette = [
        "#00bcd4",
        "#36cfc9",
        "#facc15",
        "#fb923c",
        "#f87171",
        "#a78bfa",
        "#f472b6",
    ]

    fig_alerts = px.bar(
        alert_type_counts,
        x="alert_type",
        y="count",
        color="alert_type",
        color_discrete_sequence=alert_palette[:len(alert_type_counts)]
    )

    fig_alerts.update_layout(
        title="Alerts by Type",
        template="plotly_dark",
        xaxis_tickangle=-35,
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        ),
        xaxis_title="",
        yaxis_title="Alerts",
        showlegend=False,
    )

    st.plotly_chart(
        fig_alerts,
        use_container_width=True
    )



# Risk score breakdown for one selected alert


st.divider()

st.markdown(
    '<div class="section-title">📐 Risk Score Breakdown</div>',
    unsafe_allow_html=True
)

if len(filtered_df) > 0:

    st.markdown(
        """
        <div style="
            background: #131922;
            border: 1px solid #2c3542;
            border-radius: 12px;
            padding: 14px 16px 12px 16px;
            margin-bottom: 18px;
        ">
            <div style="font-size: 0.8rem; color: #aab2bf; margin-bottom: 8px;">
                Select an alert to inspect
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected_alert_id = st.selectbox(
        "",
        filtered_df["alert_id"].tolist(),
        label_visibility="collapsed",
    )

    selected_alert = filtered_df[
        filtered_df["alert_id"] == selected_alert_id
    ].iloc[0]

    breakdown = get_score_breakdown(
        selected_alert
    )

    st.markdown(
        f"""
        <div style="
            font-size: 1.05rem;
            color: #e5e7eb;
            margin: 12px 0 16px 0;
            font-weight: 600;
        ">
            {selected_alert['alert_type']} • {selected_alert['asset']}
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div style="background: #151b26; border: 1px solid #2a3441; border-radius: 12px; padding: 16px; min-height: 150px;">
                <div style="font-size: 0.9rem; color: #b1bac7; margin-bottom: 10px;">Severity</div>
                <div style="font-size: 2.2rem; font-weight: 700; color: #ff6b6b; line-height: 1.1;">{score}/100</div>
                <div style="font-size: 0.82rem; color: #9aa4b2; margin-top: 16px;">Weight: 40% • +{contribution}</div>
            </div>
            """.format(score=breakdown['severity_score'], contribution=breakdown['severity_contribution']),
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div style="background: #151b26; border: 1px solid #2a3441; border-radius: 12px; padding: 16px; min-height: 150px;">
                <div style="font-size: 0.9rem; color: #b1bac7; margin-bottom: 10px;">Asset Importance</div>
                <div style="font-size: 2.2rem; font-weight: 700; color: #62d0ff; line-height: 1.1;">{score}/100</div>
                <div style="font-size: 0.82rem; color: #9aa4b2; margin-top: 16px;">Weight: 30% • +{contribution}</div>
            </div>
            """.format(score=breakdown['asset_score'], contribution=breakdown['asset_contribution']),
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div style="background: #151b26; border: 1px solid #2a3441; border-radius: 12px; padding: 16px; min-height: 150px;">
                <div style="font-size: 0.9rem; color: #b1bac7; margin-bottom: 10px;">Event Context</div>
                <div style="font-size: 2.2rem; font-weight: 700; color: #ffd166; line-height: 1.1;">{score}/100</div>
                <div style="font-size: 0.82rem; color: #9aa4b2; margin-top: 16px;">Weight: 30% • +{contribution}</div>
            </div>
            """.format(score=breakdown['context_score'], contribution=breakdown['context_contribution']),
            unsafe_allow_html=True,
        )

    with col4:
        priority_color = {
            "CRITICAL": ("#3a171b", "#ff6b6b"),
            "HIGH": ("#3a2816", "#ffad5c"),
            "MEDIUM": ("#393117", "#f6ce67"),
            "LOW": ("#143022", "#61d995"),
        }.get(selected_alert["priority"], ("#1a1219", "#ff8fab"))

        bg_color, text_color = priority_color

        st.markdown(
            """
            <div style="background: {bg}; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px; min-height: 150px;">
                <div style="font-size: 0.9rem; color: #e5e7eb; margin-bottom: 10px;">Final Risk</div>
                <div style="font-size: 2.2rem; font-weight: 700; color: {text}; line-height: 1.1;">{score}/100</div>
                <div style="font-size: 0.82rem; color: #f3f4f6; margin-top: 16px;">Priority: {priority}</div>
            </div>
            """.format(
                bg=bg_color,
                text=text_color,
                score=breakdown['final_score'],
                priority=selected_alert['priority'],
            ),
            unsafe_allow_html=True,
        )



# Scoring methodology notes


st.divider()

st.markdown(
    '<div class="section-title">⚙️ Risk Scoring Methodology</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="methodology-box">

    <div class="methodology-item">
    <b>Severity — 40%</b><br>
    Measures how serious the detected security event is.
    </div>

    <div class="methodology-item">
    <b>Asset Importance — 30%</b><br>
    Measures the business importance or sensitivity of
    the affected asset.
    </div>

    <div class="methodology-item">
    <b>Event Context — 30%</b><br>
    Considers surrounding conditions such as repeated
    attempts, malicious IPs, after-hours activity,
    and affected users.
    </div>

    <br>

    <div class="methodology-item">
    <b>Priority Thresholds</b><br>
    🔴 Critical: 90–100 &nbsp; | &nbsp;
    🟠 High: 70–89 &nbsp; | &nbsp;
    🟡 Medium: 40–69 &nbsp; | &nbsp;
    🟢 Low: 0–39
    </div>

    </div>
    """,
    unsafe_allow_html=True
)

# Footer

st.divider()

st.markdown(
    "<div style='text-align: center; color: #8c8c8c; font-size: 0.9rem;'>"
    "Security Alert Prioritization — Project by Vatsal Gajjar (SOC Intern)"
    "</div>",
    unsafe_allow_html=True,
)
