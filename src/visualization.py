import plotly.express as px
import pandas as pd
import streamlit as st

# Aliases: maps user-spoken chart names to canonical types
CHART_TYPE_ALIASES = {
    # Bar / Column
    "bar": "bar",
    "column": "bar",
    "grouped bar": "bar",
    "grouped column": "bar",
    "stacked bar": "bar_stacked",
    "stacked column": "bar_stacked",
    "horizontal bar": "bar_h",
    "bar horizontal": "bar_h",

    # Line
    "line": "line",
    "trend": "line",
    "time series": "line",

    # Pie / Donut
    "pie": "pie",
    "donut": "donut",
    "doughnut": "donut",

    # Area
    "area": "area",
    "stacked area": "area_stacked",

    # Scatter
    "scatter": "scatter",
    "bubble": "scatter",

    # Histogram
    "histogram": "histogram",

    # Box / Violin
    "box": "box",
    "violin": "violin",

    # Treemap
    "treemap": "treemap",
    "tree map": "treemap",

    # Funnel
    "funnel": "funnel",
}

def _normalize_chart_type(raw_type: str) -> str:
    """Normalize raw LLM chart type string to a canonical type key."""
    t = raw_type.lower().strip()
    # Strip common suffixes
    for suffix in [" chart", " graph", " plot", " diagram"]:
        t = t.replace(suffix, "")
    t = t.strip()
    return CHART_TYPE_ALIASES.get(t, t)


def _match_column(target: str, columns: list) -> str:
    """Helper to find the actual column name even if underscores/spaces/case differ."""
    if not target: return target
    if target in columns: return target
    
    t_norm = target.lower().replace("_", " ").strip()
    for col in columns:
        if col.lower().replace("_", " ").strip() == t_norm:
            return col
    return target


def render_chart(df: pd.DataFrame, chart_config: dict):
    """Render a Plotly chart based on the configuration."""
    raw_type = chart_config.get("CHART_TYPE", "").lower()
    chart_type = _normalize_chart_type(raw_type)

    x_axis = _match_column(chart_config.get("X_AXIS"), df.columns)
    y_axis = _match_column(chart_config.get("Y_AXIS"), df.columns)
    color  = _match_column(chart_config.get("COLOR"), df.columns) or None  # empty string → None

    common_kwargs = dict(
        template="seaborn",
        color_discrete_sequence=px.colors.qualitative.Safe,
    )

    fig = None

    # ── Vertical grouped/stacked bar (column chart) ──────────────────────────
    if chart_type == "bar":
        if not x_axis or not y_axis:
            st.warning("Column chart requires X_AXIS and Y_AXIS.")
            return
        barmode = "group" if color else "relative"
        fig = px.bar(df, x=x_axis, y=y_axis, color=color,
                     barmode=barmode, **common_kwargs)

    elif chart_type == "bar_stacked":
        if not x_axis or not y_axis:
            st.warning("Stacked column chart requires X_AXIS and Y_AXIS.")
            return
        fig = px.bar(df, x=x_axis, y=y_axis, color=color,
                     barmode="stack", **common_kwargs)

    # ── Horizontal bar ───────────────────────────────────────────────────────
    elif chart_type == "bar_h":
        if not x_axis or not y_axis:
            st.warning("Horizontal bar chart requires X_AXIS and Y_AXIS.")
            return
        # Swap axes for a horizontal layout
        fig = px.bar(df, x=y_axis, y=x_axis, color=color,
                     orientation="h", **common_kwargs)

    # ── Line ─────────────────────────────────────────────────────────────────
    elif chart_type == "line":
        if not x_axis or not y_axis:
            st.warning("Line chart requires X_AXIS and Y_AXIS.")
            return
        fig = px.line(df, x=x_axis, y=y_axis, color=color,
                      markers=True, **common_kwargs)

    # ── Area ─────────────────────────────────────────────────────────────────
    elif chart_type == "area":
        if not x_axis or not y_axis:
            st.warning("Area chart requires X_AXIS and Y_AXIS.")
            return
        fig = px.area(df, x=x_axis, y=y_axis, color=color, **common_kwargs)

    elif chart_type == "area_stacked":
        if not x_axis or not y_axis:
            st.warning("Stacked area chart requires X_AXIS and Y_AXIS.")
            return
        fig = px.area(df, x=x_axis, y=y_axis, color=color,
                      groupnorm="", **common_kwargs)

    # ── Pie ──────────────────────────────────────────────────────────────────
    elif chart_type == "pie":
        # Auto-detect if missing
        if not x_axis:
            cats = df.select_dtypes(exclude="number").columns.tolist()
            x_axis = cats[0] if cats else df.columns[0]
        if not y_axis:
            nums = df.select_dtypes(include="number").columns.tolist()
            y_axis = nums[0] if nums else df.columns[-1]

        fig = px.pie(df, names=x_axis, values=y_axis, **common_kwargs)

    # ── Donut ────────────────────────────────────────────────────────────────
    elif chart_type == "donut":
        # Auto-detect if missing
        if not x_axis:
            cats = df.select_dtypes(exclude="number").columns.tolist()
            x_axis = cats[0] if cats else df.columns[0]
        if not y_axis:
            nums = df.select_dtypes(include="number").columns.tolist()
            y_axis = nums[0] if nums else df.columns[-1]

        fig = px.pie(df, names=x_axis, values=y_axis, hole=0.45, **common_kwargs)

    # ── Scatter ──────────────────────────────────────────────────────────────
    elif chart_type == "scatter":
        if not x_axis or not y_axis:
            st.warning("Scatter chart requires X_AXIS and Y_AXIS.")
            return
        fig = px.scatter(df, x=x_axis, y=y_axis, color=color, **common_kwargs)

    # ── Histogram ────────────────────────────────────────────────────────────
    elif chart_type == "histogram":
        col = x_axis or y_axis
        if not col:
            st.warning("Histogram requires at least X_AXIS.")
            return
        fig = px.histogram(df, x=col, color=color, **common_kwargs)

    # ── Box ──────────────────────────────────────────────────────────────────
    elif chart_type == "box":
        if not x_axis or not y_axis:
            st.warning("Box plot requires X_AXIS and Y_AXIS.")
            return
        fig = px.box(df, x=x_axis, y=y_axis, color=color, **common_kwargs)

    # ── Violin ───────────────────────────────────────────────────────────────
    elif chart_type == "violin":
        if not x_axis or not y_axis:
            st.warning("Violin plot requires X_AXIS and Y_AXIS.")
            return
        fig = px.violin(df, x=x_axis, y=y_axis, color=color,
                        box=True, **common_kwargs)

    # ── Treemap ──────────────────────────────────────────────────────────────
    elif chart_type == "treemap":
        path_cols = [c for c in [color, x_axis] if c]
        if not path_cols or not y_axis:
            st.warning("Treemap requires X_AXIS (path) and Y_AXIS (values).")
            return
        fig = px.treemap(df, path=path_cols, values=y_axis, **common_kwargs)

    # ── Funnel ───────────────────────────────────────────────────────────────
    elif chart_type == "funnel":
        if not x_axis or not y_axis:
            st.warning("Funnel chart requires X_AXIS and Y_AXIS.")
            return
        fig = px.funnel(df, x=y_axis, y=x_axis, **common_kwargs)

    else:
        st.warning(f"Unsupported chart type: '{raw_type}'. "
                   f"Supported types: bar/column, line, pie, donut, area, "
                   f"scatter, histogram, box, violin, treemap, funnel, "
                   f"horizontal bar, stacked bar/area.")
        return

    fig.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=50, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#212529", family="'Rubik', sans-serif"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="center", x=0.5),
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
                    k = key.strip().upper()
                    v = value.strip()
                    
                    # Normalize common aliases to X_AXIS, Y_AXIS, COLOR
                    if any(x in k for x in ["NAMES", "LABEL", "CATEGORY", "X_AXIS", "X-AXIS"]):
                        config["X_AXIS"] = v
                    elif any(x in k for x in ["VALUES", "VALUE", "Y_AXIS", "Y-AXIS", "MEASURE"]):
                        config["Y_AXIS"] = v
                    elif any(x in k for x in ["COLOR", "LEGEND", "SERIES"]):
                        config["COLOR"] = v
                    else:
                        config[k] = v
    return config
