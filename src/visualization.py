import plotly.express as px
import pandas as pd
import streamlit as st

def render_chart(df: pd.DataFrame, chart_config: dict):
    """Render a Plotly chart based on the configuration."""
    chart_type = chart_config.get("CHART_TYPE", "").lower()
    x_axis = chart_config.get("X_AXIS")
    y_axis = chart_config.get("Y_AXIS")
    color = chart_config.get("COLOR")

    if not x_axis or not y_axis:
        return

    if chart_type == "bar":
        fig = px.bar(df, x=x_axis, y=y_axis, color=color, template="plotly_white", color_discrete_sequence=px.colors.qualitative.Safe)
    elif chart_type == "line":
        fig = px.line(df, x=x_axis, y=y_axis, color=color, template="plotly_white", color_discrete_sequence=px.colors.qualitative.Safe)
    elif chart_type == "pie":
        fig = px.pie(df, names=x_axis, values=y_axis, template="plotly_white", color_discrete_sequence=px.colors.qualitative.Safe)
    elif chart_type == "scatter":
        fig = px.scatter(df, x=x_axis, y=y_axis, color=color, template="plotly_white", color_discrete_sequence=px.colors.qualitative.Safe)
    else:
        st.warning(f"Unsupported chart type: {chart_type}")
        return

    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#212529")
    )
    st.plotly_chart(fig, width="stretch")

def parse_chart_config(text: str) -> dict:
    """Parse chart configuration from the LLM's interpretation response."""
    config = {}
    if "---" in text:
        parts = text.split("---")
        if len(parts) >= 3:
            config_lines = parts[-2].strip().split("\n")
            for line in config_lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    config[key.strip()] = value.strip()
    return config
