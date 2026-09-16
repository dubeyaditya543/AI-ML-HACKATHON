"""
MANGANEX — Production Simulator Component (Tab 3)
Historical production analysis, shortfall visualization, and what-if scenario planning.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import COLORS, CHART_COLORS, MANGANESE_BELTS
from utils.chart_utils import (
    create_line_chart,
    create_area_chart,
    create_bar_chart,
    get_plotly_layout,
)


def render_production_simulator(production_df, grid_df):
    """
    Render the production simulator tab with historical analysis,
    shortfall visualization, and what-if scenarios.
    """
    st.markdown(
        """
        <div style="margin-bottom: 1rem;">
            <h3 style="margin:0; color: #E2E8F0;">
                🏭 Production Shortfall Simulator
            </h3>
            <p style="color: #94A3B8; font-size: 0.85rem; margin-top: 0.3rem;">
                Analyze production gaps and simulate scenarios for overcoming shortfalls.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if len(production_df) == 0:
        st.warning("No production data matches the current filters.")
        return

    # ─── Section 1: Production vs Target Over Time ──────────────
    st.markdown("##### 📈 National Production vs Target")

    # Aggregate by year
    yearly = (
        production_df
        .groupby("year")
        .agg({
            "actual_production_kt": "sum",
            "target_production_kt": "sum",
            "shortfall_kt": "sum",
        })
        .reset_index()
    )

    # Create custom area chart showing the gap
    fig_production = go.Figure()

    # Target line (dashed)
    fig_production.add_trace(go.Scatter(
        x=yearly["year"],
        y=yearly["target_production_kt"],
        mode="lines+markers",
        name="Target Production",
        line=dict(color=COLORS["accent"], width=2.5, dash="dash"),
        marker=dict(size=7, symbol="diamond"),
    ))

    # Actual production (solid with fill)
    fig_production.add_trace(go.Scatter(
        x=yearly["year"],
        y=yearly["actual_production_kt"],
        mode="lines+markers",
        name="Actual Production",
        line=dict(color=COLORS["primary"], width=3),
        marker=dict(size=7),
        fill="tonexty",
        fillcolor="rgba(239,68,68,0.12)",
    ))

    fig_production.update_layout(
        get_plotly_layout("", 380),
        yaxis_title="Production (KT)",
        xaxis_title="Year",
        hovermode="x unified",
    )

    # Add annotation for shortfall area
    fig_production.add_annotation(
        x=yearly["year"].iloc[len(yearly) // 2],
        y=(yearly["target_production_kt"].mean() + yearly["actual_production_kt"].mean()) / 2,
        text="⚠️ Shortfall Gap",
        showarrow=False,
        font=dict(size=13, color=COLORS["danger"]),
        bgcolor="rgba(239,68,68,0.15)",
        bordercolor=COLORS["danger"],
        borderwidth=1,
        borderpad=6,
    )

    st.plotly_chart(fig_production, use_container_width=True)

    # ─── Section 2: State-wise Breakdown ────────────────────────
    st.markdown("---")
    st.markdown("##### 🗺️ State-wise Production Analysis")

    view_col1, view_col2 = st.columns([3, 2])

    with view_col1:
        # State-wise stacked production chart
        latest_year = production_df["year"].max()
        state_prod = (
            production_df[production_df["year"] == latest_year]
            .sort_values("actual_production_kt", ascending=True)
        )

        fig_state = go.Figure()

        fig_state.add_trace(go.Bar(
            y=state_prod["state"],
            x=state_prod["actual_production_kt"],
            name="Actual",
            orientation="h",
            marker=dict(color=COLORS["primary"], cornerradius=4),
        ))

        fig_state.add_trace(go.Bar(
            y=state_prod["state"],
            x=state_prod["shortfall_kt"],
            name="Shortfall",
            orientation="h",
            marker=dict(color=COLORS["danger"], cornerradius=4, opacity=0.7),
        ))

        fig_state.update_layout(
            get_plotly_layout(f"State-wise Production ({latest_year})", 380),
            barmode="stack",
            xaxis_title="Production (KT)",
        )

        st.plotly_chart(fig_state, use_container_width=True)

    with view_col2:
        # Key metrics for latest year
        st.markdown(f"###### Key Metrics ({latest_year})")

        total_actual = state_prod["actual_production_kt"].sum()
        total_target = state_prod["target_production_kt"].sum()
        total_shortfall = state_prod["shortfall_kt"].sum()
        avg_utilization = production_df[production_df["year"] == latest_year]["capacity_utilization_pct"].mean()
        total_mines = production_df[production_df["year"] == latest_year]["active_mines"].sum()

        metrics_data = [
            ("Total Actual", f"{total_actual:,.0f} KT", COLORS["primary"]),
            ("Total Target", f"{total_target:,.0f} KT", COLORS["accent"]),
            ("Total Shortfall", f"{total_shortfall:,.0f} KT", COLORS["danger"]),
            ("Avg Capacity Util.", f"{avg_utilization:.1f}%", COLORS["info"]),
            ("Active Mines", f"{total_mines}", COLORS["primary"]),
        ]

        for label, value, color in metrics_data:
            st.markdown(
                f"""
                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 0.6rem 0.8rem;
                    margin-bottom: 0.4rem;
                    background: rgba(26,26,46,0.6);
                    border-left: 3px solid {color};
                    border-radius: 0 6px 6px 0;
                ">
                    <span style="color:#94A3B8; font-size:0.85rem;">{label}</span>
                    <span style="color:{color}; font-weight:700; font-size:1rem;">{value}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ─── Section 3: What-If Scenario Simulator ──────────────────
    st.markdown("---")
    st.markdown("##### 🔮 What-If Scenario Simulator")
    st.markdown(
        '<p style="color: #94A3B8; font-size: 0.8rem;">'
        "Adjust parameters to simulate how exploration and operational changes could close the production gap."
        "</p>",
        unsafe_allow_html=True,
    )

    sim_col1, sim_col2 = st.columns([1, 1])

    with sim_col1:
        st.markdown("###### Operational Levers")

        capacity_increase = st.slider(
            "Capacity Utilization Increase (%)",
            0, 30, 10,
            help="How much existing mine capacity could be better utilized",
            key="capacity_increase",
        )

        new_mines = st.slider(
            "New Mines Commissioned",
            0, 20, 5,
            help="Number of new mines from exploration targets",
            key="new_mines",
        )

        avg_mine_output = st.slider(
            "Avg New Mine Output (KT/year)",
            10, 100, 40,
            help="Expected annual production from each new mine",
            key="avg_mine_output",
        )

        tech_improvement = st.slider(
            "Technology Efficiency Gain (%)",
            0, 25, 5,
            help="Improvement from better extraction technology",
            key="tech_improvement",
        )

    with sim_col2:
        st.markdown("###### Demand & Market")

        demand_growth = st.slider(
            "Annual Demand Growth (%)",
            0.0, 10.0, 3.0, 0.5,
            help="Expected annual increase in manganese demand",
            key="demand_growth",
        )

        forecast_years = st.slider(
            "Forecast Horizon (years)",
            1, 10, 5,
            help="Number of years to project forward",
            key="forecast_years",
        )

        # ─── Run Simulation ─────────────────────────────────────
        # Current baseline
        current_actual = total_actual
        current_target = total_target
        current_shortfall = total_shortfall

        # Calculate improvements
        capacity_boost = current_actual * (capacity_increase / 100)
        new_mine_output = new_mines * avg_mine_output
        tech_boost = current_actual * (tech_improvement / 100)
        total_improvement = capacity_boost + new_mine_output + tech_boost

        projected_actual = current_actual + total_improvement
        projected_target = current_target * (1 + demand_growth / 100) ** forecast_years
        projected_shortfall = max(0, projected_target - projected_actual)

        # Display results
        st.markdown("###### Simulation Results")

        improvement_pct = (total_improvement / current_actual * 100) if current_actual > 0 else 0
        gap_closed = ((current_shortfall - projected_shortfall) / current_shortfall * 100) if current_shortfall > 0 else 100

        result_color = COLORS["primary"] if gap_closed > 50 else COLORS["accent"] if gap_closed > 20 else COLORS["danger"]

        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, rgba(26,26,46,0.9), rgba(22,33,62,0.7));
                border: 1px solid {result_color}40;
                border-radius: 10px;
                padding: 1rem;
                text-align: center;
            ">
                <div style="font-size: 2rem; font-weight: 800; color: {result_color};">
                    {gap_closed:.1f}%
                </div>
                <div style="color: #94A3B8; font-size: 0.8rem;">
                    of shortfall gap closed
                </div>
                <div style="margin-top: 0.5rem; font-size: 0.75rem; color: #64748B;">
                    +{total_improvement:,.0f} KT additional production
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ─── Projection Chart ───────────────────────────────────────
    st.markdown("---")
    st.markdown("##### 📊 Production Forecast")

    # Build forecast DataFrame
    forecast_data = []
    base_year = latest_year

    for y in range(forecast_years + 1):
        year = base_year + y
        # Gradual improvement ramp-up
        ramp = min(1.0, y / max(1, forecast_years * 0.6))
        proj_actual = current_actual + total_improvement * ramp
        proj_target = current_target * (1 + demand_growth / 100) ** y

        forecast_data.append({
            "year": year,
            "projected_production": proj_actual,
            "projected_demand": proj_target,
            "gap": max(0, proj_target - proj_actual),
        })

    forecast_df = pd.DataFrame(forecast_data)

    fig_forecast = go.Figure()

    fig_forecast.add_trace(go.Scatter(
        x=forecast_df["year"],
        y=forecast_df["projected_demand"],
        mode="lines+markers",
        name="Projected Demand",
        line=dict(color=COLORS["danger"], width=2.5, dash="dash"),
        marker=dict(size=7, symbol="diamond"),
    ))

    fig_forecast.add_trace(go.Scatter(
        x=forecast_df["year"],
        y=forecast_df["projected_production"],
        mode="lines+markers",
        name="Projected Production",
        line=dict(color=COLORS["primary"], width=3),
        marker=dict(size=7),
        fill="tonexty",
        fillcolor="rgba(16,185,129,0.1)",
    ))

    fig_forecast.update_layout(
        get_plotly_layout("", 350),
        yaxis_title="Production (KT)",
        xaxis_title="Year",
        hovermode="x unified",
    )

    st.plotly_chart(fig_forecast, use_container_width=True)

    # ─── Scenario Summary Cards ─────────────────────────────────
    sc1, sc2, sc3, sc4 = st.columns(4)

    with sc1:
        st.metric(
            "From Capacity",
            f"+{capacity_boost:,.0f} KT",
            f"+{capacity_increase}% utilization",
        )
    with sc2:
        st.metric(
            "From New Mines",
            f"+{new_mine_output:,.0f} KT",
            f"{new_mines} mines × {avg_mine_output} KT",
        )
    with sc3:
        st.metric(
            "From Technology",
            f"+{tech_boost:,.0f} KT",
            f"+{tech_improvement}% efficiency",
        )
    with sc4:
        st.metric(
            "Projected Shortfall",
            f"{projected_shortfall:,.0f} KT",
            f"{'-' if projected_shortfall < current_shortfall else '+'}{abs(projected_shortfall - current_shortfall):,.0f} KT",
            delta_color="inverse",
        )
