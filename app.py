"""
MineVision AI — Mn Reserve Intelligence Platform
Main Streamlit Application

Built for Smart India Hackathon 2026
Problem Statement: AI/ML & Satellite Technology for Manganese Reserve Estimation
                   and Production Shortfall Mitigation
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys

# ─── Page Configuration ──────────────────────────────────────────
st.set_page_config(
    page_title="MineVision AI — Mn Reserve Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Path Setup ──────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from config.settings import COLORS, APP_TITLE, APP_SUBTITLE, ORG_NAME, PROBLEM_STATEMENT
from components.sidebar import render_sidebar
from components.command_center import render_command_center
from components.prospectivity_map import render_prospectivity_map
from components.production_forecast import render_production_forecast
from components.risk_analysis import render_risk_analysis
from components.recommendations import render_recommendations

# ─── Custom CSS Styling ──────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* ── Global Styles ─────────────────────────────────────── */
    html, body, [class*="st-"] {
        font-family: 'Inter', -apple-system, sans-serif;
    }

    .stApp {
        background-color: #141410 !important;
        color: #e0ddd0 !important;
    }

    /* ── Hide Streamlit Default Chrome ─────────────────────── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {display: none;}

    /* ── Reduce Top Padding ────────────────────────────────── */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2.2rem !important;
        padding-right: 2.2rem !important;
        max-width: 100% !important;
    }

    /* ── Sidebar Styling ───────────────────────────────────── */
    [data-testid="stSidebar"] {
        background-color: #1a1a14 !important;
        border-right: 1px solid #282920 !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        background-color: #1a1a14 !important;
    }

    /* Custom Radio styling for Sidebar Navigation */
    [data-testid="stSidebar"] .stRadio {
        margin-top: 0.5rem;
    }

    [data-testid="stSidebar"] .stRadio > div {
        gap: 6px;
    }

    [data-testid="stSidebar"] .stRadio label {
        background: transparent !important;
        border: 1px solid transparent;
        border-radius: 4px;
        padding: 9px 14px !important;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        width: 100%;
        box-sizing: border-box;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(200, 132, 42, 0.08) !important;
        border-color: rgba(200, 132, 42, 0.2) !important;
    }

    /* Hide the circular radio indicator */
    [data-testid="stSidebar"] .stRadio label [data-testid="stWidgetLabel"] input,
    [data-testid="stSidebar"] .stRadio input[type="radio"],
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }

    /* Selected state */
    [data-testid="stSidebar"] .stRadio label[data-checked="true"],
    [data-testid="stSidebar"] .stRadio label:has(input:checked) {
        background: rgba(200, 132, 42, 0.12) !important;
        border: 1px solid #c8842a !important;
        color: #e0ddd0 !important;
    }

    [data-testid="stSidebar"] .stRadio label div p {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.86rem !important;
        font-weight: 500 !important;
        color: #b0ad9e !important;
        margin: 0 !important;
    }

    [data-testid="stSidebar"] .stRadio label:has(input:checked) div p {
        color: #e0ddd0 !important;
        font-weight: 600 !important;
    }

    /* ── Top Status Bar ────────────────────────────────────── */
    .mv-topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 0 16px 0;
        margin-bottom: 8px;
        border-bottom: 1px solid #23241c;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        letter-spacing: 0.5px;
    }

    .mv-topbar-live {
        color: #c8842a;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .mv-topbar-sih {
        color: #6a6a5a;
    }

    /* ── KPI Metric Cards ──────────────────────────────────── */
    .mv-kpi-card {
        background: #1c1d17;
        border: 1px solid #282920;
        border-radius: 4px;
        padding: 12px 14px;
        min-height: 78px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .mv-kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: #7a7a6c;
        letter-spacing: 0.4px;
        text-transform: uppercase;
    }

    .mv-kpi-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.55rem;
        font-weight: 700;
        color: #e0ddd0;
        letter-spacing: -0.5px;
        line-height: 1.1;
        margin-top: 4px;
    }

    .mv-kpi-unit {
        font-size: 0.85rem;
        font-weight: 400;
        color: #7a7a6c;
        margin-left: 2px;
    }

    /* ── Panel Cards ───────────────────────────────────────── */
    .mv-panel-card {
        background: #1c1d17;
        border: 1px solid #282920;
        border-radius: 4px;
        padding: 16px 18px;
    }

    .mv-panel-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.88rem;
        font-weight: 600;
        color: #e0ddd0;
        margin-bottom: 12px;
        letter-spacing: -0.2px;
    }

    /* ── Table & List Rows ─────────────────────────────────── */
    .mv-table-list, .mv-risk-list {
        display: flex;
        flex-direction: column;
    }

    .mv-table-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 11px 4px;
        border-bottom: 1px solid #24251e;
    }

    .mv-table-row:last-child {
        border-bottom: none;
    }

    .mv-row-name {
        font-size: 0.84rem;
        color: #d0cdbf;
        font-weight: 400;
    }

    .mv-row-status {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* ── Shortfall Risk Rows ───────────────────────────────── */
    .mv-risk-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 9px 4px;
        border-bottom: 1px solid #24251e;
    }

    .mv-risk-row:last-child {
        border-bottom: none;
    }

    .mv-risk-mine-name {
        font-size: 0.84rem;
        color: #d0cdbf;
        font-weight: 500;
    }

    .mv-risk-subtext {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #7a7a6c;
        margin-top: 2px;
    }

    .mv-risk-pill {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─── Load Data ───────────────────────────────────────────────────
@st.cache_data
def load_app_data():
    """Load and cache datasets."""
    data_dir = os.path.join(PROJECT_ROOT, "data")
    deposits_path = os.path.join(data_dir, "manganese_deposits.csv")
    grid_path = os.path.join(data_dir, "prospectivity_grid.csv")
    prod_path = os.path.join(data_dir, "production_data.csv")

    deposits_df = pd.read_csv(deposits_path) if os.path.exists(deposits_path) else pd.DataFrame()
    grid_df = pd.read_csv(grid_path) if os.path.exists(grid_path) else pd.DataFrame()
    prod_df = pd.read_csv(prod_path) if os.path.exists(prod_path) else pd.DataFrame()

    return deposits_df, grid_df, prod_df

deposits_df, grid_df, prod_df = load_app_data()

# ─── Top Status Bar ──────────────────────────────────────────────
st.markdown(
    f"""
    <div class="mv-topbar">
        <div class="mv-topbar-live">
            <span>((•)) LIVE</span>
            <span style="color: #4a4a3a;">|</span>
            <span style="color: #8a8a7a;">Synthetic Demonstration Data</span>
        </div>
        <div class="mv-topbar-sih">
            {PROBLEM_STATEMENT}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─── Sidebar Navigation ──────────────────────────────────────────
selected_page = render_sidebar()

# ─── Page Router ─────────────────────────────────────────────────
if selected_page == "Command Center":
    render_command_center(prod_df, deposits_df, grid_df)
elif selected_page == "Prospectivity Map":
    render_prospectivity_map(grid_df, deposits_df)
elif selected_page == "Production Forecast":
    render_production_forecast(prod_df)
elif selected_page == "Risk Analysis":
    render_risk_analysis()
elif selected_page == "Recommendations":
    render_recommendations(grid_df)
