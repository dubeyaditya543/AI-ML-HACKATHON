"""
MANGANEX — Target Ranking Component (Tab 2)
Ranked exploration targets, feature importance, and comparative analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import COLORS, CHART_COLORS
from utils.chart_utils import (
    create_feature_importance_chart,
    create_radar_chart,
    create_donut_chart,
)


def render_target_ranking(grid_df, model_metrics=None):
    """
    Render the target ranking tab with sorted targets,
    feature importance, and comparative analysis.
    """
    st.markdown(
        """
        <div style="margin-bottom: 1rem;">
            <h3 style="margin:0; color: #E2E8F0;">
                📊 Exploration Target Ranking
            </h3>
            <p style="color: #94A3B8; font-size: 0.85rem; margin-top: 0.3rem;">
                AI-ranked exploration targets sorted by prospectivity score with feature analysis.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if len(grid_df) == 0:
        st.warning("No targets match the current filters. Adjust sidebar settings.")
        return

    # ─── Top Targets Table ──────────────────────────────────────
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("##### 🏆 Top Exploration Targets")

        # Prepare display DataFrame
        top_n = st.slider("Number of targets", 5, 50, 20, key="top_n_targets")

        display_df = (
            grid_df
            .sort_values("prospectivity_score", ascending=False)
            .head(top_n)
            .reset_index(drop=True)
        )
        display_df.index = display_df.index + 1
        display_df.index.name = "Rank"

        # Select columns for display
        display_cols = [
            "cell_id", "state", "latitude", "longitude",
            "prospectivity_score", "confidence", "priority",
            "mn_proxy", "ferrous_index", "clay_index", "ndvi",
        ]
        display_cols = [c for c in display_cols if c in display_df.columns]

        # Style the DataFrame
        styled_df = display_df[display_cols].style.background_gradient(
            subset=["prospectivity_score"],
            cmap="RdYlGn",
            vmin=0, vmax=1,
        ).background_gradient(
            subset=["confidence"],
            cmap="Blues",
            vmin=0.3, vmax=1,
        ).format({
            "prospectivity_score": "{:.4f}",
            "confidence": "{:.4f}",
            "latitude": "{:.4f}",
            "longitude": "{:.4f}",
            "mn_proxy": "{:.4f}",
            "ferrous_index": "{:.4f}",
            "clay_index": "{:.4f}",
            "ndvi": "{:.4f}",
        })

        st.dataframe(styled_df, use_container_width=True, height=450)

        # CSV download button
        csv_data = display_df[display_cols].to_csv(index=True)
        st.download_button(
            label="📥 Download Targets as CSV",
            data=csv_data,
            file_name="manganex_top_targets.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col_right:
        # ─── Priority Distribution ──────────────────────────────
        st.markdown("##### 📈 Priority Distribution")

        priority_counts = grid_df["priority"].value_counts()
        fig_donut = create_donut_chart(
            labels=priority_counts.index.tolist(),
            values=priority_counts.values.tolist(),
            title="",
            height=280,
        )
        st.plotly_chart(fig_donut, use_container_width=True)

        # ─── State-wise Target Count ────────────────────────────
        st.markdown("##### 🗺️ Targets by State")

        state_high = (
            grid_df[grid_df["priority"] == "High"]
            .groupby("state")
            .size()
            .sort_values(ascending=False)
            .reset_index(name="high_priority_count")
        )

        if len(state_high) > 0:
            for _, row in state_high.iterrows():
                pct = row["high_priority_count"] / len(grid_df[grid_df["priority"] == "High"]) * 100
                st.markdown(
                    f"""
                    <div style="
                        display: flex;
                        align-items: center;
                        margin-bottom: 0.4rem;
                        padding: 0.4rem 0.6rem;
                        background: rgba(26,26,46,0.5);
                        border-radius: 6px;
                    ">
                        <div style="flex:1; font-size:0.85rem; color:#E2E8F0;">{row['state']}</div>
                        <div style="font-size:0.85rem; color:#10B981; font-weight:600; margin-right:0.5rem;">{row['high_priority_count']}</div>
                        <div style="
                            width: 80px; height: 6px;
                            background: rgba(51,65,85,0.5);
                            border-radius: 3px;
                            overflow: hidden;
                        ">
                            <div style="
                                width: {pct}%;
                                height: 100%;
                                background: linear-gradient(90deg, #10B981, #3B82F6);
                                border-radius: 3px;
                            "></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ─── Feature Importance & Radar Charts ──────────────────────
    st.markdown("---")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("##### 🔬 Feature Importance")

        if model_metrics and "feature_importances" in model_metrics:
            feat_imp = model_metrics["feature_importances"]
            names = list(feat_imp.keys())
            values = list(feat_imp.values())
        else:
            # Compute from data correlation with prospectivity
            feature_cols = [
                "ndvi", "clay_index", "ferrous_index", "mn_proxy",
                "elevation", "slope", "distance_to_fault",
            ]
            available = [c for c in feature_cols if c in grid_df.columns]
            names = available
            values = [
                abs(grid_df[c].corr(grid_df["prospectivity_score"]))
                for c in available
            ]

        fig_imp = create_feature_importance_chart(names, values, title="", height=400)
        st.plotly_chart(fig_imp, use_container_width=True)

    with chart_col2:
        st.markdown("##### 🕸️ Top 5 Targets — Feature Comparison")

        top5 = grid_df.sort_values("prospectivity_score", ascending=False).head(5)

        radar_features = ["ndvi", "clay_index", "ferrous_index", "mn_proxy"]
        radar_features = [f for f in radar_features if f in top5.columns]

        if len(radar_features) >= 3 and len(top5) > 0:
            # Normalize features to 0-1 for radar chart
            values_list = []
            label_names = []
            for _, row in top5.iterrows():
                vals = []
                for f in radar_features:
                    col_min = grid_df[f].min()
                    col_max = grid_df[f].max()
                    col_range = col_max - col_min
                    normalized = (row[f] - col_min) / col_range if col_range > 0 else 0.5
                    vals.append(round(normalized, 3))
                values_list.append(vals)
                label_names.append(row.get("cell_id", f"Target {_ + 1}"))

            categories = [f.replace("_", " ").title() for f in radar_features]

            fig_radar = create_radar_chart(
                categories, values_list, label_names,
                title="", height=400,
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        else:
            st.info("Insufficient data for radar comparison.")

    # ─── Summary Statistics ─────────────────────────────────────
    st.markdown("---")
    st.markdown("##### 📋 Summary Statistics")

    summary_cols = st.columns(4)

    with summary_cols[0]:
        avg_score = grid_df["prospectivity_score"].mean()
        st.metric("Avg Prospectivity", f"{avg_score:.3f}")

    with summary_cols[1]:
        median_score = grid_df["prospectivity_score"].median()
        st.metric("Median Score", f"{median_score:.3f}")

    with summary_cols[2]:
        std_score = grid_df["prospectivity_score"].std()
        st.metric("Score Std Dev", f"{std_score:.3f}")

    with summary_cols[3]:
        avg_conf = grid_df["confidence"].mean()
        st.metric("Avg Confidence", f"{avg_conf:.3f}")
