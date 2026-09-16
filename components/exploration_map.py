"""
MANGANEX — Exploration Map Component (Tab 1)
Interactive Folium map with prospectivity heatmap and deposit markers.
"""

import streamlit as st
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium
import branca.colormap as cm
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import COLORS, MAP_CENTER, MAP_ZOOM, MANGANESE_BELTS, PROSPECTIVITY_COLORS


def render_exploration_map(deposits_df, grid_df):
    """
    Render the interactive exploration map with prospectivity heatmap
    and deposit markers.
    """
    st.markdown(
        """
        <div style="margin-bottom: 1rem;">
            <h3 style="margin:0; color: #E2E8F0;">
                🗺️ Manganese Prospectivity Map
            </h3>
            <p style="color: #94A3B8; font-size: 0.85rem; margin-top: 0.3rem;">
                Heatmap shows AI-predicted prospectivity scores. Click markers for deposit details.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Map controls
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1, 1, 1])

    with ctrl_col1:
        map_style = st.selectbox(
            "Map Style",
            ["Dark", "Satellite", "Terrain", "Standard"],
            index=0,
            key="map_style",
        )

    with ctrl_col2:
        show_heatmap = st.checkbox("Show Prospectivity Heatmap", value=True, key="show_heatmap")

    with ctrl_col3:
        show_deposits = st.checkbox("Show Known Deposits", value=True, key="show_deposits")

    # Tile selection
    tiles_map = {
        "Dark": "CartoDB dark_matter",
        "Satellite": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        "Terrain": "https://stamen-tiles.a.ssl.fastly.net/terrain/{z}/{x}/{y}.jpg",
        "Standard": "OpenStreetMap",
    }

    tile_attr = {
        "Satellite": "Esri",
        "Terrain": "Stamen",
    }

    # Calculate dynamic map center
    if len(grid_df) > 0:
        center_lat = grid_df["latitude"].mean()
        center_lon = grid_df["longitude"].mean()
    else:
        center_lat, center_lon = MAP_CENTER

    # Create map
    tile_url = tiles_map.get(map_style, "CartoDB dark_matter")
    attr = tile_attr.get(map_style, None)

    if map_style in ["Satellite", "Terrain"]:
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=MAP_ZOOM,
            tiles=tile_url,
            attr=attr,
        )
    else:
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=MAP_ZOOM,
            tiles=tile_url,
        )

    # ─── Prospectivity Heatmap Layer ────────────────────────────
    if show_heatmap and len(grid_df) > 0:
        heat_data = grid_df[["latitude", "longitude", "prospectivity_score"]].values.tolist()

        HeatMap(
            heat_data,
            min_opacity=0.3,
            max_opacity=0.85,
            radius=18,
            blur=20,
            gradient={
                0.0: "#1a1a2e",
                0.2: "#16213e",
                0.4: "#3B82F6",
                0.6: "#10B981",
                0.8: "#F59E0B",
                1.0: "#EF4444",
            },
        ).add_to(m)

    # ─── Known Deposit Markers ──────────────────────────────────
    if show_deposits and len(deposits_df) > 0:
        marker_cluster = MarkerCluster(name="Known Deposits").add_to(m)

        for _, row in deposits_df.iterrows():
            # Color by grade
            if "High" in str(row.get("grade", "")):
                icon_color = "red"
                grade_badge = "🔴"
            elif "Medium" in str(row.get("grade", "")):
                icon_color = "orange"
                grade_badge = "🟠"
            else:
                icon_color = "blue"
                grade_badge = "🔵"

            popup_html = f"""
            <div style="
                font-family: 'Inter', sans-serif;
                min-width: 220px;
                padding: 8px;
            ">
                <h4 style="margin: 0 0 8px 0; color: #0D4F4F;">
                    {grade_badge} {row.get('deposit_id', 'N/A')}
                </h4>
                <table style="font-size: 12px; width: 100%;">
                    <tr><td style="color:#666;">State</td><td><b>{row.get('state', 'N/A')}</b></td></tr>
                    <tr><td style="color:#666;">District</td><td><b>{row.get('district', 'N/A')}</b></td></tr>
                    <tr><td style="color:#666;">Grade</td><td><b>{row.get('grade', 'N/A')}</b></td></tr>
                    <tr><td style="color:#666;">Mn Content</td><td><b>{row.get('mn_pct', 'N/A')}%</b></td></tr>
                    <tr><td style="color:#666;">Tonnage</td><td><b>{row.get('estimated_tonnage_mt', 'N/A')} MT</b></td></tr>
                    <tr><td style="color:#666;">Depth</td><td><b>{row.get('depth_m', 'N/A')} m</b></td></tr>
                    <tr><td style="color:#666;">Type</td><td><b>{row.get('geological_type', 'N/A')}</b></td></tr>
                    <tr><td style="color:#666;">Status</td><td><b>{row.get('status', 'N/A')}</b></td></tr>
                </table>
            </div>
            """

            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=folium.Popup(popup_html, max_width=280),
                tooltip=f"{row.get('deposit_id', '')} — {row.get('grade', '')}",
                icon=folium.Icon(color=icon_color, icon="info-sign"),
            ).add_to(marker_cluster)

    # ─── State Belt Boundaries ──────────────────────────────────
    for state, info in MANGANESE_BELTS.items():
        if state in deposits_df["state"].values:
            lat, lon = info["center"]
            folium.CircleMarker(
                location=[lat, lon],
                radius=25,
                color=info["color"],
                fill=True,
                fillColor=info["color"],
                fillOpacity=0.08,
                weight=1,
                opacity=0.4,
                tooltip=f"{state} Belt ({info['share_pct']}% of reserves)",
            ).add_to(m)

    # ─── Color Legend ───────────────────────────────────────────
    colormap = cm.LinearColormap(
        colors=["#1a1a2e", "#3B82F6", "#10B981", "#F59E0B", "#EF4444"],
        vmin=0.0,
        vmax=1.0,
        caption="Prospectivity Score",
    )
    colormap.add_to(m)

    # Layer control
    folium.LayerControl(collapsed=False).add_to(m)

    # Render map
    map_data = st_folium(m, width=None, height=550, returned_objects=[])

    # ─── Map Statistics ─────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

    with stat_col1:
        st.metric("Grid Cells Displayed", f"{len(grid_df):,}")
    with stat_col2:
        st.metric("Deposits Shown", f"{len(deposits_df):,}")
    with stat_col3:
        high_count = len(grid_df[grid_df["priority"] == "High"]) if len(grid_df) > 0 else 0
        st.metric("High Priority Zones", f"{high_count}")
    with stat_col4:
        states_count = grid_df["state"].nunique() if len(grid_df) > 0 else 0
        st.metric("States Covered", f"{states_count}")
