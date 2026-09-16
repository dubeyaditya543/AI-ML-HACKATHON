"""
MineVision AI — Production Forecast Component
Historical production, shortfall modeling, and interactive what-if simulation.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import COLORS, MINE_BLOCKS, PRODUCTION_YEARS


def render_production_forecast(production_df=None):
    """
    Render the Production Forecast & What-If Simulator.
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
            ">Production Forecast & Shortfall Simulator</h2>
            <p style="
                margin: 4px 0 0 0;
                font-size: 0.82rem;
                color: #7a7a6c;
                font-family: 'Inter', -apple-system, sans-serif;
            ">Multi-year production outlook, national demand gap analysis, and interactive operational levers</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ─── Top Metric Cards ──────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            """
            <div class="mv-kpi-card">
                <div class="mv-kpi-header"><span>BASE FORECAST 2025</span><span style="color:#c8842a;">📈</span></div>
                <div class="mv-kpi-value">4,210 <span class="mv-kpi-unit">kt</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            """
            <div class="mv-kpi-card">
                <div class="mv-kpi-header"><span>NATIONAL TARGET</span></div>
                <div class="mv-kpi-value">4,900 <span class="mv-kpi-unit">kt</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            """
            <div class="mv-kpi-card">
                <div class="mv-kpi-header"><span>PROJECTED SHORTFALL</span><span style="color:#c94a2a;">⚠️</span></div>
                <div class="mv-kpi-value" style="color: #c94a2a;">690 <span class="mv-kpi-unit" style="color:#c94a2a;">kt</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m4:
        st.markdown(
            """
            <div class="mv-kpi-card">
                <div class="mv-kpi-header"><span>GAP CLOSURE FEASIBILITY</span></div>
                <div class="mv-kpi-value" style="color: #5c9e47;">84.2<span class="mv-kpi-unit" style="color:#5c9e47;">%</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # ─── Historical & Forecast Chart ───────────────────────────────
    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028]
    historical_prod = [2820, 2900, 2650, 3100, 3350, 3600, 3850]
    forecast_baseline = [None]*6 + [3850, 4210, 4350, 4520, 4700]
    target_prod = [3200, 3400, 3600, 3900, 4200, 4500, 4700, 4900, 5100, 5300, 5500]

    fig = go.Figure()

    # Target line
    fig.add_trace(go.Scatter(
        x=years,
        y=target_prod,
        mode="lines+markers",
        name="Target Demand",
        line=dict(color="#c94a2a", width=2, dash="dash"),
        marker=dict(size=5, color="#c94a2a"),
    ))

    # Historical
    fig.add_trace(go.Scatter(
        x=years[:7],
        y=historical_prod,
        mode="lines+markers",
        name="Actual Production",
        line=dict(color="#4aada8", width=3),
        marker=dict(size=6, color="#4aada8"),
        fill="tozeroy",
        fillcolor="rgba(74, 173, 168, 0.08)",
    ))

    # Baseline forecast
    fig.add_trace(go.Scatter(
        x=years[6:],
        y=forecast_baseline[6:],
        mode="lines+markers",
        name="AI Baseline Forecast",
        line=dict(color="#c8842a", width=3),
        marker=dict(size=6, color="#c8842a"),
        fill="tozeroy",
        fillcolor="rgba(200, 132, 42, 0.08)",
    ))

    fig.update_layout(
        title=dict(text="Fleet-Wide Manganese Production Trajectory vs Target (kt)", font=dict(color="#e0ddd0", size=14)),
        paper_bgcolor="#1a1a14",
        plot_bgcolor="#141410",
        height=360,
        margin=dict(l=40, r=20, t=50, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#8a8a7a", size=11)),
        xaxis=dict(gridcolor="#282920", tickfont=dict(color="#8a8a7a")),
        yaxis=dict(gridcolor="#282920", tickfont=dict(color="#8a8a7a")),
    )

    st.plotly_chart(fig, use_container_width=True)

    # ─── What-If Scenario Levers ───────────────────────────────────
    st.markdown(
        """
        <div class="mv-panel-card" style="margin-top: 10px;">
            <div class="mv-panel-title" style="display: flex; align-items: center; gap: 8px;">
                <span>⚙️ Interactive What-If Scenario Levers</span>
            </div>
            <div style="font-size: 0.8rem; color: #7a7a6c; margin-bottom: 14px;">
                Adjust operational levers to model shortfall mitigation and simulate recovered production volume.
            </div>
        """,
        unsafe_allow_html=True,
    )

    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        capacity_boost = st.slider(
            "Underground Mechanization (% capacity)",
            min_value=0,
            max_value=30,
            value=12,
            step=2,
            format="+%d%%",
        )
    with sc2:
        fast_track_blocks = st.slider(
            "Fast-Track Exploration Blocks",
            min_value=0,
            max_value=5,
            value=2,
            step=1,
            format="%d blocks",
        )
    with sc3:
        beneficiation_tech = st.slider(
            "Ore Beneficiation Yield Gain",
            min_value=0,
            max_value=20,
            value=8,
            step=2,
            format="+%d%%",
        )

    # Calculate simulated gain
    base_prod = 4210
    target = 4900
    base_shortfall = target - base_prod

    added_by_capacity = base_prod * (capacity_boost / 100.0)
    added_by_blocks = fast_track_blocks * 180  # approx 180kt per block
    added_by_beneficiation = base_prod * (beneficiation_tech / 100.0) * 0.4

    simulated_prod = base_prod + added_by_capacity + added_by_blocks + added_by_beneficiation
    new_shortfall = max(0, target - simulated_prod)
    shortfall_recovered = min(base_shortfall, simulated_prod - base_prod)
    pct_closed = min(100.0, (shortfall_recovered / base_shortfall) * 100 if base_shortfall > 0 else 100)

    st.markdown(
        f"""
            <div style="
                margin-top: 14px;
                padding: 14px;
                background: #141410;
                border: 1px solid #2e2f24;
                border-radius: 6px;
                display: flex;
                justify-content: space-around;
                align-items: center;
                text-align: center;
            ">
                <div>
                    <div style="font-size: 0.72rem; color: #7a7a6c; font-family: monospace;">SIMULATED OUTPUT</div>
                    <div style="font-size: 1.35rem; font-weight: 700; color: #5c9e47; font-family: monospace;">{simulated_prod:,.0f} t</div>
                </div>
                <div style="border-left: 1px solid #282920; height: 36px;"></div>
                <div>
                    <div style="font-size: 0.72rem; color: #7a7a6c; font-family: monospace;">SHORTFALL CLOSED</div>
                    <div style="font-size: 1.35rem; font-weight: 700; color: #c8842a; font-family: monospace;">+{shortfall_recovered:,.0f} t</div>
                </div>
                <div style="border-left: 1px solid #282920; height: 36px;"></div>
                <div>
                    <div style="font-size: 0.72rem; color: #7a7a6c; font-family: monospace;">TARGET GAP RESOLVED</div>
                    <div style="font-size: 1.35rem; font-weight: 700; color: #4aada8; font-family: monospace;">{pct_closed:.1f}%</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
