"""
MineVision AI — Risk Analysis Component
Fleet-wide risk scoring, grade dilution vulnerability, and reserve depletion horizons.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import COLORS, MINE_BLOCKS


def render_risk_analysis():
    """
    Render the Risk Analysis page.
    """
    st.markdown(
        """
        <div style="margin-bottom: 22px;">
            <h2 style="
                margin: 0;
                font-size: 1.45rem;
                font-weight: 700;
                color: #e0ddd0;
                letter-spacing: -0.2px;
                font-family: 'Inter', -apple-system, sans-serif;
            ">Fleet Risk & Reserve Depletion Analysis</h2>
            <p style="
                margin: 4px 0 0 0;
                font-size: 0.82rem;
                color: #7a7a6c;
                font-family: 'Inter', -apple-system, sans-serif;
            ">Comprehensive vulnerability evaluation covering grade dilution, operational downtime, and fault zones</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ─── 4 Metric Cards ──────────────────────────────────────────
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.markdown(
            """
            <div class="mv-kpi-card">
                <div class="mv-kpi-header"><span>OVERALL FLEET RISK</span><span style="color:#c8842a;">⚠️</span></div>
                <div class="mv-kpi-value" style="color:#c8842a;">MEDIUM <span class="mv-kpi-unit">5.8/10</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with r2:
        st.markdown(
            """
            <div class="mv-kpi-card">
                <div class="mv-kpi-header"><span>CRITICAL BLOCKS</span><span style="color:#c94a2a;">●</span></div>
                <div class="mv-kpi-value" style="color:#c94a2a;">1 <span class="mv-kpi-unit">Gumgaon</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with r3:
        st.markdown(
            """
            <div class="mv-kpi-card">
                <div class="mv-kpi-header"><span>AVG GRADE DILUTION</span></div>
                <div class="mv-kpi-value" style="color:#e0ddd0;">-2.4<span class="mv-kpi-unit">% Mn/yr</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with r4:
        st.markdown(
            """
            <div class="mv-kpi-card">
                <div class="mv-kpi-header"><span>RESERVE LIFE INDEX</span></div>
                <div class="mv-kpi-value" style="color:#5c9e47;">18.4 <span class="mv-kpi-unit">years</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # ─── Risk Matrix Scatter Chart & Mine Vulnerability ──────────
    col1, col2 = st.columns([1.4, 1])

    with col1:
        mines = ["Gumgaon", "Balaghat", "Ukwa", "Dongri Buzurg", "Kandri", "Munsar", "Tirodi", "Chikla"]
        downtime_prob = [0.82, 0.65, 0.42, 0.35, 0.20, 0.70, 0.30, 0.25]
        production_impact = [390, 270, 60, 45, 10, 80, 25, 20]
        grades = [38, 46, 42, 44, 40, 35, 41, 39]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=downtime_prob,
            y=production_impact,
            mode="markers+text",
            text=mines,
            textposition="top center",
            textfont=dict(color="#e0ddd0", size=11),
            marker=dict(
                size=[g * 0.45 for g in grades],
                color=["#c94a2a", "#d97838", "#c89f36", "#5c9e47", "#5c9e47", "#8a8a7a", "#5c9e47", "#5c9e47"],
                line=dict(color="#1a1a14", width=1.5),
            ),
        ))

        fig.update_layout(
            title=dict(text="Risk Matrix: Downtime Probability vs Tonnage Impact", font=dict(color="#e0ddd0", size=13)),
            paper_bgcolor="#1a1a14",
            plot_bgcolor="#141410",
            height=340,
            margin=dict(l=40, r=20, t=50, b=30),
            xaxis=dict(title="Downtime / Geological Fault Probability", gridcolor="#282920", tickfont=dict(color="#8a8a7a")),
            yaxis=dict(title="Annual Shortfall Impact (kt)", gridcolor="#282920", tickfont=dict(color="#8a8a7a")),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown(
            """
            <div class="mv-panel-card" style="height: 340px; overflow-y: auto;">
                <div class="mv-panel-title">Vulnerability Register</div>
                <div class="mv-table-list">
                    <div class="mv-table-row">
                        <div>
                            <span class="mv-row-name">Gumgaon Mine</span>
                            <div style="font-size: 0.7rem; color: #7a7a6c;">High water ingress & fault line</div>
                        </div>
                        <span class="mv-risk-pill" style="background:#381a17; color:#df5444; border: 1px solid rgba(223,84,68,0.3);">Critical</span>
                    </div>
                    <div class="mv-table-row">
                        <div>
                            <span class="mv-row-name">Balaghat Mine</span>
                            <div style="font-size: 0.7rem; color: #7a7a6c;">Deep shaft hoisting capacity limit</div>
                        </div>
                        <span class="mv-risk-pill" style="background:#362215; color:#d97838; border: 1px solid rgba(217,120,56,0.3);">High</span>
                    </div>
                    <div class="mv-table-row">
                        <div>
                            <span class="mv-row-name">Munsar Mine</span>
                            <div style="font-size: 0.7rem; color: #7a7a6c;">Low-grade ore body (35% Mn)</div>
                        </div>
                        <span class="mv-risk-pill" style="background:#302613; color:#c89f36; border: 1px solid rgba(200,159,54,0.3);">Moderate</span>
                    </div>
                    <div class="mv-table-row">
                        <div>
                            <span class="mv-row-name">Ukwa Mine</span>
                            <div style="font-size: 0.7rem; color: #7a7a6c;">Haul road gradient wear</div>
                        </div>
                        <span class="mv-risk-pill" style="background:#302613; color:#c89f36; border: 1px solid rgba(200,159,54,0.3);">Moderate</span>
                    </div>
                    <div class="mv-table-row">
                        <div>
                            <span class="mv-row-name">Kandri Mine</span>
                            <div style="font-size: 0.7rem; color: #7a7a6c;">Stable rock mechanics, continuous ops</div>
                        </div>
                        <span class="mv-risk-pill" style="background:#192817; color:#5c9e47; border: 1px solid rgba(92,158,71,0.3);">Low</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
