"""
MineVision AI — Strategic Recommendations Component
AI-driven exploration drill targets and operational mitigation interventions.
"""

import streamlit as st
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import COLORS


def render_recommendations(grid_df=None):
    """
    Render AI Recommendations and Action Plan.
    """
    st.markdown(
        """<div style="margin-bottom: 22px;">
<h2 style="margin: 0; font-size: 1.45rem; font-weight: 700; color: #e0ddd0; letter-spacing: -0.2px; font-family: 'Inter', -apple-system, sans-serif;">Strategic Recommendations & Action Plan</h2>
<p style="margin: 4px 0 0 0; font-size: 0.82rem; color: #7a7a6c; font-family: 'Inter', -apple-system, sans-serif;">Prioritized exploratory drill targets, beneficiation recovery tuning, and mine uptime interventions</p>
</div>""",
        unsafe_allow_html=True,
    )

    # ─── Priority Drill Targets Table ─────────────────────────────
    targets_html = (
        '<div class="mv-panel-card" style="margin-bottom: 20px;">'
        '<div class="mv-panel-title">🎯 Top Recommended Exploration Drill Targets</div>'
        '<div style="font-size: 0.78rem; color: #7a7a6c; margin-bottom: 12px;">'
        'Identified via Random Forest + Sentinel-2 multispectral anomaly detection (SWIR absorption & Mn proxy)'
        '</div>'
        '<div class="mv-table-list">'
        '<div class="mv-table-row" style="background: #141410; font-family: monospace; font-size: 0.72rem; color: #7a7a6c; padding: 6px 12px;">'
        '<span style="flex: 1.2;">TARGET ID / LOCATION</span>'
        '<span style="flex: 1;">COORDINATES</span>'
        '<span style="flex: 0.8;">AI SCORE</span>'
        '<span style="flex: 0.8;">EST. GRADE</span>'
        '<span style="flex: 0.8;">PRIORITY</span>'
        '</div>'
        '<div class="mv-table-row">'
        '<span class="mv-row-name" style="flex: 1.2;">CELL-00005 (Balaghat East)</span>'
        '<span style="flex: 1; font-family: monospace; font-size: 0.78rem; color: #b0ad9e;">21.824°N, 80.241°E</span>'
        '<span style="flex: 0.8; font-family: monospace; color: #c8842a; font-weight: 600;">91.5%</span>'
        '<span style="flex: 0.8; font-family: monospace; color: #5c9e47;">47.2% Mn</span>'
        '<span style="flex: 0.8;"><span class="mv-risk-pill" style="background:#362215; color:#d97838; border:1px solid rgba(217,120,56,0.3);">High Prio</span></span>'
        '</div>'
        '<div class="mv-table-row">'
        '<span class="mv-row-name" style="flex: 1.2;">CELL-00002 (Tirodi Extension)</span>'
        '<span style="flex: 1; font-family: monospace; font-size: 0.78rem; color: #b0ad9e;">21.962°N, 79.745°E</span>'
        '<span style="flex: 0.8; font-family: monospace; color: #c8842a; font-weight: 600;">88.2%</span>'
        '<span style="flex: 0.8; font-family: monospace; color: #5c9e47;">45.1% Mn</span>'
        '<span style="flex: 0.8;"><span class="mv-risk-pill" style="background:#362215; color:#d97838; border:1px solid rgba(217,120,56,0.3);">High Prio</span></span>'
        '</div>'
        '<div class="mv-table-row">'
        '<span class="mv-row-name" style="flex: 1.2;">CELL-00014 (Dongri North)</span>'
        '<span style="flex: 1; font-family: monospace; font-size: 0.78rem; color: #b0ad9e;">21.710°N, 79.912°E</span>'
        '<span style="flex: 0.8; font-family: monospace; color: #4aada8; font-weight: 600;">82.0%</span>'
        '<span style="flex: 0.8; font-family: monospace; color: #5c9e47;">43.8% Mn</span>'
        '<span style="flex: 0.8;"><span class="mv-risk-pill" style="background:#302613; color:#c89f36; border:1px solid rgba(200,159,54,0.3);">Med Prio</span></span>'
        '</div>'
        '<div class="mv-table-row">'
        '<span class="mv-row-name" style="flex: 1.2;">CELL-00021 (Parsheoni West)</span>'
        '<span style="flex: 1; font-family: monospace; font-size: 0.78rem; color: #b0ad9e;">21.385°N, 79.215°E</span>'
        '<span style="flex: 0.8; font-family: monospace; color: #4aada8; font-weight: 600;">76.4%</span>'
        '<span style="flex: 0.8; font-family: monospace; color: #5c9e47;">41.0% Mn</span>'
        '<span style="flex: 0.8;"><span class="mv-risk-pill" style="background:#302613; color:#c89f36; border:1px solid rgba(200,159,54,0.3);">Med Prio</span></span>'
        '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(targets_html, unsafe_allow_html=True)

    # ─── Operational Interventions Row ────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="mv-panel-card">'
            '<div class="mv-panel-title">⚡ High-Impact Operational Interventions</div>'
            '<div style="display: flex; flex-direction: column; gap: 12px; margin-top: 8px;">'
            '<div style="background: #141410; padding: 12px; border-radius: 4px; border-left: 3px solid #df5444;">'
            '<div style="font-size: 0.85rem; font-weight: 600; color: #e0ddd0;">Gumgaon Mine Dewatering & Shaft Support</div>'
            '<div style="font-size: 0.76rem; color: #8a8a7a; margin-top: 3px;">'
            'Deploy high-capacity sub-surface submersible pumps. Restoring full operations closes <b>390 kt</b> shortfall.'
            '</div></div>'
            '<div style="background: #141410; padding: 12px; border-radius: 4px; border-left: 3px solid #d97838;">'
            '<div style="font-size: 0.85rem; font-weight: 600; color: #e0ddd0;">Balaghat Deep-Shaft Skip Hoisting Modernization</div>'
            '<div style="font-size: 0.76rem; color: #8a8a7a; margin-top: 3px;">'
            'Upgrade double-drum hoist system to increase cycle speed by 22%, yielding +<b>270 kt</b> throughput.'
            '</div></div></div></div>',
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            '<div class="mv-panel-card">'
            '<div class="mv-panel-title">🔬 Mineral Beneficiation Upgrades</div>'
            '<div style="display: flex; flex-direction: column; gap: 12px; margin-top: 8px;">'
            '<div style="background: #141410; padding: 12px; border-radius: 4px; border-left: 3px solid #5c9e47;">'
            '<div style="font-size: 0.85rem; font-weight: 600; color: #e0ddd0;">Dense Media Separation (DMS) at Dongri Buzurg</div>'
            '<div style="font-size: 0.76rem; color: #8a8a7a; margin-top: 3px;">'
            'Upgrade low-grade silicious manganese ore from 30% Mn to 42% Mn, unlocking <b>180 kt</b> sub-economic reserves.'
            '</div></div>'
            '<div style="background: #141410; padding: 12px; border-radius: 4px; border-left: 3px solid #c8842a;">'
            '<div style="font-size: 0.85rem; font-weight: 600; color: #e0ddd0;">Wet High-Intensity Magnetic Separation (WHIMS)</div>'
            '<div style="font-size: 0.76rem; color: #8a8a7a; margin-top: 3px;">'
            'Recover fine manganese slimes from tailings ponds across Ukwa and Kandri, capturing +<b>65 kt</b> high-purity fines.'
            '</div></div></div></div>',
            unsafe_allow_html=True,
        )
