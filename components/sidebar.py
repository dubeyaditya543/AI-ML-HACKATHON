"""
MineVision AI — Sidebar Navigation Component
Clean, modern dark sidebar navigation matching the MineVision AI command interface.
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import APP_TITLE, APP_SUBTITLE, ORG_NAME, PAGES


def render_sidebar():
    """
    Render the sidebar navigation for MineVision AI.
    Returns:
        str: Currently selected page name
    """
    with st.sidebar:
        # ─── Brand Header ─────────────────────────────────────────
        st.markdown(
            f"""
            <div class="brand-container" style="padding: 18px 8px 24px 8px; display: flex; align-items: center; gap: 10px;">
                <div style="
                    width: 10px;
                    height: 10px;
                    border-radius: 50%;
                    background: #c8842a;
                    box-shadow: 0 0 10px rgba(200, 132, 42, 0.7);
                    display: inline-block;
                "></div>
                <div style="
                    font-size: 1.15rem;
                    font-weight: 700;
                    color: #e0ddd0;
                    letter-spacing: 0.5px;
                    font-family: 'Inter', sans-serif;
                ">{APP_TITLE}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ─── Navigation Options ───────────────────────────────────
        nav_options = [
            ("Command Center", "⊞  Command Center"),
            ("Prospectivity Map", "⌖  Prospectivity Map"),
            ("Production Forecast", "📈  Production Forecast"),
            ("Risk Analysis", "🛡️  Risk Analysis"),
            ("Recommendations", "💡  Recommendations"),
        ]

        page_keys = [opt[0] for opt in nav_options]
        page_labels = [opt[1] for opt in nav_options]

        # Initialize session state for selected page if not present
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Command Center"

        # Find current index
        try:
            curr_idx = page_keys.index(st.session_state.current_page)
        except ValueError:
            curr_idx = 0

        selected_label = st.radio(
            "Navigation",
            options=page_labels,
            index=curr_idx,
            label_visibility="collapsed",
            key="nav_radio",
        )

        # Map label back to key
        selected_key = page_keys[page_labels.index(selected_label)]
        st.session_state.current_page = selected_key

        # ─── Sidebar Footer ───────────────────────────────────────
        st.markdown(
            f"""
            <div class="sidebar-footer" style="
                position: fixed;
                bottom: 24px;
                left: 18px;
                font-family: 'JetBrains Mono', 'Roboto Mono', monospace;
                font-size: 0.72rem;
                letter-spacing: 1px;
                color: #5a5a4a;
                line-height: 1.5;
                text-transform: uppercase;
            ">
                <div style="font-weight: 600; color: #7a7a68;">{ORG_NAME}</div>
                <div>{APP_SUBTITLE}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        return selected_key
