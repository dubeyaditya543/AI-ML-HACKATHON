"""
MineVision AI — Executive Command Center Component
Pixel-perfect reproduction of the Command Center dashboard from reference screenshot.
"""

import streamlit as st
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import COLORS, MINE_BLOCKS


def render_command_center(production_df=None, deposits_df=None, grid_df=None):
    """
    Render the Executive Command Center matching the reference UI screenshot.
    """
    # ─── Title and Subtitle ─────────────────────────────────────────
    st.markdown(
        """<div style="margin-bottom: 22px;">
<h2 style="margin: 0; font-size: 1.45rem; font-weight: 700; color: #e0ddd0; letter-spacing: -0.2px; font-family: 'Inter', -apple-system, sans-serif;">Executive Command Center</h2>
<p style="margin: 4px 0 0 0; font-size: 0.82rem; color: #7a7a6c; font-family: 'Inter', -apple-system, sans-serif;">Fleet-wide production outlook and reserve status across active mine blocks</p>
</div>""",
        unsafe_allow_html=True,
    )

    # ─── 5 KPI Metric Cards Row ─────────────────────────────────────
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

    with kpi_col1:
        st.markdown(
            """<div class="mv-kpi-card">
<div class="mv-kpi-header"><span>PREDICTED PRODUCTION</span><span style="color: #c94a2a; font-size: 0.95rem;">↘</span></div>
<div class="mv-kpi-value">4,210 <span class="mv-kpi-unit">t</span></div>
</div>""",
            unsafe_allow_html=True,
        )

    with kpi_col2:
        st.markdown(
            """<div class="mv-kpi-card">
<div class="mv-kpi-header"><span>TARGET PRODUCTION</span><span></span></div>
<div class="mv-kpi-value">4,900 <span class="mv-kpi-unit">t</span></div>
</div>""",
            unsafe_allow_html=True,
        )

    with kpi_col3:
        st.markdown(
            """<div class="mv-kpi-card">
<div class="mv-kpi-header"><span>SHORTFALL RISK</span><span style="color: #c8842a; font-size: 0.85rem;">⚠️</span></div>
<div class="mv-kpi-value" style="color: #c8842a;">34<span class="mv-kpi-unit" style="color: #c8842a;">%</span></div>
</div>""",
            unsafe_allow_html=True,
        )

    with kpi_col4:
        st.markdown(
            """<div class="mv-kpi-card">
<div class="mv-kpi-header"><span>RECOVERABLE PRODUCTION</span><span></span></div>
<div class="mv-kpi-value" style="color: #5c9e47;">3,200 <span class="mv-kpi-unit" style="color: #5c9e47;">t</span></div>
</div>""",
            unsafe_allow_html=True,
        )

    with kpi_col5:
        st.markdown(
            """<div class="mv-kpi-card">
<div class="mv-kpi-header"><span>HIGH PROSPECTIVITY AREAS</span><span style="color: #c8842a; font-size: 0.85rem;">🥞</span></div>
<div class="mv-kpi-value" style="color: #c8842a;">9</div>
</div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # ─── Two Column Layout: Mine Block Status & Shortfall Risk ──────
    col_left, col_right = st.columns(2)

    with col_left:
        # Mine Block Status Card
        mine_rows = [
            ("Balaghat Mine", "ACTIVE", "#5c9e47"),
            ("Ukwa Mine", "ACTIVE", "#5c9e47"),
            ("Dongri Buzurg Mine", "ACTIVE", "#5c9e47"),
            ("Gumgaon Mine", "MAINTENANCE", "#c9a02a"),
            ("Kandri Mine", "ACTIVE", "#5c9e47"),
            ("Munsar Mine", "IDLE", "#5a5a4a"),
        ]

        rows_html = "".join([
            f'<div class="mv-table-row">'
            f'<span class="mv-row-name">{name}</span>'
            f'<span class="mv-row-status" style="color: {color};">{status}</span>'
            f'</div>'
            for name, status, color in mine_rows
        ])

        mine_status_html = (
            f'<div class="mv-panel-card">'
            f'<div class="mv-panel-title">Mine Block Status</div>'
            f'<div class="mv-table-list">'
            f'{rows_html}'
            f'</div>'
            f'</div>'
        )
        st.markdown(mine_status_html, unsafe_allow_html=True)

    with col_right:
        # Highest Shortfall Risk Card
        risk_rows = [
            {
                "name": "Gumgaon Mine",
                "shortfall": "390 t",
                "pill": "Critical",
                "pill_bg": "#381a17",
                "pill_color": "#df5444",
                "pill_border": "rgba(223, 84, 68, 0.3)",
            },
            {
                "name": "Balaghat Mine",
                "shortfall": "270 t",
                "pill": "High",
                "pill_bg": "#362215",
                "pill_color": "#d97838",
                "pill_border": "rgba(217, 120, 56, 0.3)",
            },
            {
                "name": "Ukwa Mine",
                "shortfall": "60 t",
                "pill": "Moderate",
                "pill_bg": "#302613",
                "pill_color": "#c89f36",
                "pill_border": "rgba(200, 159, 54, 0.3)",
            },
            {
                "name": "Kandri Mine",
                "shortfall": "0 t",
                "pill": "Low",
                "pill_bg": "#192817",
                "pill_color": "#5c9e47",
                "pill_border": "rgba(92, 158, 71, 0.3)",
            },
        ]

        risk_rows_html = "".join([
            f'<div class="mv-risk-row">'
            f'<div>'
            f'<div class="mv-risk-mine-name">{r["name"]}</div>'
            f'<div class="mv-risk-subtext">Shortfall: {r["shortfall"]}</div>'
            f'</div>'
            f'<div>'
            f'<span class="mv-risk-pill" style="background: {r["pill_bg"]}; color: {r["pill_color"]}; border: 1px solid {r["pill_border"]};">{r["pill"]}</span>'
            f'</div>'
            f'</div>'
            for r in risk_rows
        ])

        shortfall_risk_html = (
            f'<div class="mv-panel-card">'
            f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">'
            f'<div class="mv-panel-title" style="margin-bottom: 0;">Highest Shortfall Risk</div>'
            f'<span style="color: #6a6a5a; font-size: 0.85rem;">◎</span>'
            f'</div>'
            f'<div class="mv-risk-list">'
            f'{risk_rows_html}'
            f'</div>'
            f'</div>'
        )
        st.markdown(shortfall_risk_html, unsafe_allow_html=True)
