"""
MANGANEX — Chart Utility Functions
Plotly chart helpers with consistent dark theme styling.
"""

import plotly.graph_objects as go
import plotly.express as px
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import COLORS, CHART_COLORS


def get_plotly_layout(title="", height=400, show_legend=True):
    """
    Get a consistent Plotly layout with dark theme.
    """
    return go.Layout(
        title=dict(
            text=title,
            font=dict(size=16, color=COLORS["text"], family="Inter, sans-serif"),
            x=0.0,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=40, r=20, t=50, b=40),
        font=dict(color=COLORS["text_muted"], family="Inter, sans-serif", size=12),
        showlegend=show_legend,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=COLORS["text_muted"]),
        ),
        xaxis=dict(
            gridcolor="rgba(51,65,85,0.3)",
            zerolinecolor="rgba(51,65,85,0.3)",
        ),
        yaxis=dict(
            gridcolor="rgba(51,65,85,0.3)",
            zerolinecolor="rgba(51,65,85,0.3)",
        ),
    )


def create_bar_chart(df, x, y, title="", color=None, orientation="v", height=400):
    """Create a styled bar chart."""
    fig = go.Figure()

    bar_color = color or COLORS["primary"]

    if orientation == "h":
        fig.add_trace(go.Bar(
            y=df[x], x=df[y],
            orientation="h",
            marker=dict(
                color=bar_color,
                line=dict(color=bar_color, width=0),
                cornerradius=4,
            ),
        ))
    else:
        fig.add_trace(go.Bar(
            x=df[x], y=df[y],
            marker=dict(
                color=bar_color,
                line=dict(color=bar_color, width=0),
                cornerradius=4,
            ),
        ))

    fig.update_layout(get_plotly_layout(title, height, show_legend=False))
    return fig


def create_line_chart(df, x, y_cols, title="", colors=None, height=400, fill=False):
    """Create a styled multi-line chart."""
    fig = go.Figure()
    colors = colors or CHART_COLORS

    for i, y_col in enumerate(y_cols):
        fig.add_trace(go.Scatter(
            x=df[x],
            y=df[y_col],
            mode="lines+markers",
            name=y_col.replace("_", " ").title(),
            line=dict(color=colors[i % len(colors)], width=2.5),
            marker=dict(size=6, color=colors[i % len(colors)]),
            fill="tozeroy" if fill and i == 0 else None,
            fillcolor=f"rgba({int(colors[i % len(colors)][1:3], 16)},{int(colors[i % len(colors)][3:5], 16)},{int(colors[i % len(colors)][5:7], 16)},0.1)" if fill and i == 0 else None,
        ))

    fig.update_layout(get_plotly_layout(title, height))
    return fig


def create_area_chart(df, x, y_actual, y_target, title="", height=400):
    """Create a styled area chart showing gap between actual and target."""
    fig = go.Figure()

    # Target line
    fig.add_trace(go.Scatter(
        x=df[x], y=df[y_target],
        mode="lines",
        name="Target",
        line=dict(color=COLORS["accent"], width=2, dash="dash"),
    ))

    # Actual line with fill
    fig.add_trace(go.Scatter(
        x=df[x], y=df[y_actual],
        mode="lines+markers",
        name="Actual",
        line=dict(color=COLORS["primary"], width=2.5),
        marker=dict(size=5),
        fill="tonexty",
        fillcolor="rgba(239,68,68,0.15)",
    ))

    fig.update_layout(get_plotly_layout(title, height))
    return fig


def create_radar_chart(categories, values_list, names, title="", height=450):
    """Create a radar/spider chart for comparing targets across features."""
    fig = go.Figure()

    colors = CHART_COLORS
    for i, (values, name) in enumerate(zip(values_list, names)):
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],  # Close the polygon
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor=f"rgba({int(colors[i % len(colors)][1:3], 16)},{int(colors[i % len(colors)][3:5], 16)},{int(colors[i % len(colors)][5:7], 16)},0.15)",
            line=dict(color=colors[i % len(colors)], width=2),
            name=name,
        ))

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                gridcolor="rgba(51,65,85,0.3)",
                color=COLORS["text_muted"],
            ),
            angularaxis=dict(
                gridcolor="rgba(51,65,85,0.3)",
                color=COLORS["text_muted"],
            ),
        ),
        **{k: v for k, v in get_plotly_layout(title, height).to_plotly_json().items()
           if k not in ["xaxis", "yaxis"]},
    )
    return fig


def create_donut_chart(labels, values, title="", height=350):
    """Create a styled donut chart."""
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=CHART_COLORS[:len(labels)]),
        textfont=dict(color="white", size=12),
        hoverinfo="label+percent+value",
    )])

    fig.update_layout(get_plotly_layout(title, height))
    return fig


def create_feature_importance_chart(feature_names, importances, title="Feature Importance", height=450):
    """Create a horizontal bar chart for ML feature importances."""
    # Sort by importance
    sorted_pairs = sorted(zip(feature_names, importances), key=lambda x: x[1])
    names, values = zip(*sorted_pairs)

    # Create gradient colors
    n = len(names)
    colors = [
        f"rgba({int(16 + (59-16)*i/n)},{int(185 + (130-185)*i/n)},{int(129 + (246-129)*i/n)},0.85)"
        for i in range(n)
    ]

    fig = go.Figure(go.Bar(
        y=list(names),
        x=list(values),
        orientation="h",
        marker=dict(color=colors, cornerradius=4),
        text=[f"{v:.3f}" for v in values],
        textposition="outside",
        textfont=dict(color=COLORS["text_muted"], size=11),
    ))

    fig.update_layout(get_plotly_layout(title, height, show_legend=False))
    fig.update_layout(xaxis_title="Importance Score")
    return fig
