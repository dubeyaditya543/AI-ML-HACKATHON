"""
MineVision AI — AI Prospectivity Map Component
Interactive dark geospatial map matching the MineVision AI reference screenshot.
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import COLORS, PROSPECTIVITY, MINE_BLOCKS


def render_prospectivity_map(grid_df, deposits_df):
    """
    Render the AI Prospectivity Map interface.
    Matches the reference screenshot with map on left, legend/inspector/category on right.
    """
    # ─── Title and Subtitle ─────────────────────────────────────────
    st.markdown(
        """<div style="margin-bottom: 20px;">
<h2 style="margin: 0; font-size: 1.45rem; font-weight: 700; color: #e0ddd0; letter-spacing: -0.2px; font-family: 'Inter', -apple-system, sans-serif;">AI Prospectivity Map</h2>
<p style="margin: 4px 0 0 0; font-size: 0.82rem; color: #7a7a6c; font-family: 'Inter', -apple-system, sans-serif;">Prospectivity scoring over 50m grid cells, drill-hole overlay, satellite-derived indicators</p>
</div>""",
        unsafe_allow_html=True,
    )

    # ─── Two-Column Layout (Map Left ~72%, Inspector/Legend Right ~28%) ──
    map_col, right_col = st.columns([2.5, 1])

    # Filter or center on Nagpur - Balaghat MOIL belt
    center_lat = 21.35
    center_lon = 79.45

    # Filter grid for central belt or take top cells
    moil_grid = grid_df[
        (grid_df["latitude"].between(20.6, 22.2)) & 
        (grid_df["longitude"].between(78.6, 80.8))
    ].copy()

    if len(moil_grid) < 20:
        display_grid = grid_df.copy().sort_values("prospectivity_score", ascending=False).head(120)
    else:
        display_grid = moil_grid.sort_values("prospectivity_score", ascending=False)

    with map_col:
        # Build Folium map with dark satellite/imagery basemap matching reference image
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=9,
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri, Maxar, Earthstar Geographics",
            control_scale=False,
            zoom_control=True,
        )

        # Add an optional OpenStreetMap tile layer for toggle
        folium.TileLayer(
            tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
            attr="&copy; OpenStreetMap contributors",
            name="OpenStreetMap",
        ).add_to(m)
        
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri Satellite",
            name="Satellite Imagery",
            overlay=False,
            control=True,
        ).add_to(m)

        folium.LayerControl(position="topright").add_to(m)

        # Add prospectivity markers
        # High (>75%): Amber/Orange circles (#d4882e)
        # Moderate (50-75%): Teal/Cyan circles (#4aada8)
        # Low (<50%): Slate circles (#7a8585)
        # Drill holes: Small white circles with dark border (#ffffff)

        sample_cells = display_grid.head(100)

        for _, row in sample_cells.iterrows():
            score = row["prospectivity_score"]
            lat, lon = row["latitude"], row["longitude"]

            if score >= 0.75:
                color = "#c8842a"
                fill_color = "#c8842a"
                radius = 10
                fill_opacity = 0.68
                label_prio = "High"
            elif score >= 0.50:
                color = "#4aada8"
                fill_color = "#4aada8"
                radius = 7
                fill_opacity = 0.52
                label_prio = "Moderate"
            else:
                color = "#7a8585"
                fill_color = "#7a8585"
                radius = 5
                fill_opacity = 0.40
                label_prio = "Low"

            popup_html = f"""<div style="font-family: monospace; font-size: 11px; color: #e0ddd0; background: #1a1a14; padding: 6px; border-radius: 4px; border: 1px solid #3a3a2a;">
<b style="color: #c8842a;">{row['cell_id']}</b><br>
Score: <b>{score*100:.1f}%</b> ({label_prio})<br>
Coords: {lat:.3f}°, {lon:.3f}°<br>
NDVI: {row.get('ndvi', 0):.2f}<br>
Mn Proxy: {row.get('mn_proxy', 0):.2f}
</div>"""

            folium.CircleMarker(
                location=[lat, lon],
                radius=radius,
                color=color,
                weight=1.5,
                fill=True,
                fill_color=fill_color,
                fill_opacity=fill_opacity,
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f"{row['cell_id']} · Score: {score*100:.1f}%",
            ).add_to(m)

        # Add Drill Hole Locations from MINE_BLOCKS
        for mb in MINE_BLOCKS:
            folium.CircleMarker(
                location=[mb["lat"], mb["lon"]],
                radius=4,
                color="#000000",
                weight=1,
                fill=True,
                fill_color="#ffffff",
                fill_opacity=1.0,
                tooltip=f"Drill Hole / Mine: {mb['name']}",
            ).add_to(m)

        # Render Folium Map
        map_output = st_folium(
            m,
            width=None,
            height=540,
            returned_objects=["last_object_clicked"],
            key="prospectivity_folium_map",
        )

    with right_col:
        # Card 1: Legend
        legend_html = (
            '<div class="mv-panel-card" style="margin-bottom: 14px;">'
            '<div class="mv-panel-title">Legend</div>'
            '<div style="font-family: \'Inter\', sans-serif; font-size: 0.8rem; color: #b0ad9e; display: flex; flex-direction: column; gap: 10px;">'
            '<div style="display: flex; align-items: center; gap: 10px;">'
            '<div style="width: 10px; height: 10px; border-radius: 50%; background: #c8842a; box-shadow: 0 0 6px rgba(200,132,42,0.8);"></div>'
            '<span>High prospectivity (&gt;75%)</span>'
            '</div>'
            '<div style="display: flex; align-items: center; gap: 10px;">'
            '<div style="width: 10px; height: 10px; border-radius: 50%; background: #4aada8; box-shadow: 0 0 6px rgba(74,173,168,0.8);"></div>'
            '<span>Moderate (50-75%)</span>'
            '</div>'
            '<div style="display: flex; align-items: center; gap: 10px;">'
            '<div style="width: 10px; height: 10px; border-radius: 50%; background: #7a8585;"></div>'
            '<span>Low priority (&lt;50%)</span>'
            '</div>'
            '<div style="display: flex; align-items: center; gap: 10px;">'
            '<div style="width: 7px; height: 7px; border-radius: 50%; background: #ffffff; border: 1px solid #141410; box-shadow: 0 0 4px #ffffff;"></div>'
            '<span>Drill hole location</span>'
            '</div>'
            '</div>'
            '</div>'
        )
        st.markdown(legend_html, unsafe_allow_html=True)

        # Card 2: Cell Inspector
        top_cells = display_grid.head(15).reset_index(drop=True)
        selected_cell_id = st.selectbox(
            "Inspect Cell:",
            options=["-- Click map or select cell --"] + list(top_cells["cell_id"]),
            index=0,
            label_visibility="collapsed",
        )

        selected_row = None
        if selected_cell_id != "-- Click map or select cell --":
            match = display_grid[display_grid["cell_id"] == selected_cell_id]
            if not match.empty:
                selected_row = match.iloc[0]

        if selected_row is not None:
            inspector_body = (
                f'<div style="font-family: \'JetBrains Mono\', monospace; font-size: 0.78rem; color: #b0ad9e; line-height: 1.6;">'
                f'<div style="display: flex; justify-content: space-between; border-bottom: 1px solid #2a2a1e; padding-bottom: 4px; margin-bottom: 6px;">'
                f'<span style="color: #7a7a6a;">Cell ID:</span>'
                f'<span style="color: #c8842a; font-weight: 600;">{selected_row["cell_id"]}</span>'
                f'</div>'
                f'<div style="display: flex; justify-content: space-between; margin-bottom: 4px;">'
                f'<span style="color: #7a7a6a;">Coordinates:</span>'
                f'<span>{selected_row["latitude"]:.3f}°, {selected_row["longitude"]:.3f}°</span>'
                f'</div>'
                f'<div style="display: flex; justify-content: space-between; margin-bottom: 4px;">'
                f'<span style="color: #7a7a6a;">AI Score:</span>'
                f'<span style="color: #c8842a; font-weight: 600;">{selected_row["prospectivity_score"]*100:.1f}%</span>'
                f'</div>'
                f'<div style="display: flex; justify-content: space-between; margin-bottom: 4px;">'
                f'<span style="color: #7a7a6a;">Est. Mn Grade:</span>'
                f'<span style="color: #5c9e47;">44.6% Mn</span>'
                f'</div>'
                f'<div style="margin-top: 8px; padding-top: 6px; border-top: 1px solid #2a2a1e;">'
                f'<div style="font-size: 0.7rem; color: #7a7a6c; margin-bottom: 4px;">SPECTRAL INDICES (SENTINEL-2)</div>'
                f'<div style="display: flex; justify-content: space-between;">'
                f'<span>NDVI:</span> <span>{selected_row.get("ndvi", 0.22):.2f}</span>'
                f'</div>'
                f'<div style="display: flex; justify-content: space-between;">'
                f'<span>Clay Index:</span> <span>{selected_row.get("clay_index", 1.84):.2f}</span>'
                f'</div>'
                f'<div style="display: flex; justify-content: space-between;">'
                f'<span>Ferrous Index:</span> <span>{selected_row.get("ferrous_index", 1.45):.2f}</span>'
                f'</div>'
                f'<div style="display: flex; justify-content: space-between;">'
                f'<span>Mn Proxy:</span> <span style="color: #c8842a;">{selected_row.get("mn_proxy", 0.32):.2f}</span>'
                f'</div>'
                f'</div>'
                f'</div>'
            )
        else:
            inspector_body = (
                '<div style="font-family: \'Inter\', sans-serif; font-size: 0.78rem; color: #6a6a5a; line-height: 1.4;">'
                'Click a prospectivity cell on the map to inspect it.'
                '</div>'
            )

        inspector_card_html = (
            f'<div class="mv-panel-card" style="margin-bottom: 14px;">'
            f'<div class="mv-panel-title">Cell Inspector</div>'
            f'{inspector_body}'
            f'</div>'
        )
        st.markdown(inspector_card_html, unsafe_allow_html=True)

        # Card 3: Data Category
        category_card_html = (
            '<div class="mv-panel-card">'
            '<div class="mv-panel-title">Data Category</div>'
            '<div style="font-family: \'Inter\', sans-serif; font-size: 0.78rem; color: #7a7a6a; line-height: 1.5;">'
            'Prospectivity cells and drill holes shown here are a <span style="color: #c8842a; font-weight: 500;">Demonstration Synthetic Dataset</span>. Satellite layers are public imagery providers; no MOIL confidential data is used.'
            '</div>'
            '</div>'
        )
        st.markdown(category_card_html, unsafe_allow_html=True)
