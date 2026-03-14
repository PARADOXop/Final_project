import streamlit as st
import plotly.express as px
import pandas as pd

# ============================================================
# COLOR PALETTE
# Used for charts across the dashboard
# ============================================================

COLOR_PALETTE = [
    "#22D3EE",
    "#38BDF8",
    "#0EA5E9",
    "#0284C7",
    "#0369A1"
]


# ============================================================
# GLOBAL CHART STYLE
# Applies consistent styling to all charts
# ============================================================

def style_chart(fig, height=420):

    fig.update_layout(

        height=height,

        # background colors
        plot_bgcolor="#0F1C3D",
        paper_bgcolor="#0F1C3D",

        # font style
        font=dict(
            color="#E2E8F0",
            size=14
        ),

        # chart margins
        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        ),

        # grid styling
        xaxis=dict(
            showgrid=True,
            gridcolor="#1E293B"
        ),

        yaxis=dict(
            showgrid=True,
            gridcolor="#1E293B"
        )

    )

    return fig


# ============================================================
# BAR CHART
# ============================================================

def bar_chart(df, x, y, title=None, height=420):

    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        color_discrete_sequence=COLOR_PALETTE
    )

    fig = style_chart(fig, height)

    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# HISTOGRAM
# ============================================================

def hist_chart(df, x, title=None, height=420):

    fig = px.histogram(
        df,
        x=x,
        title=title,
        color_discrete_sequence=COLOR_PALETTE
    )

    fig = style_chart(fig, height)

    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# SCATTER CHART
# Used for relationships between two variables
# ============================================================

def scatter_chart(df, x, y, color=None, title=None, height=500):

    # Build figure depending on whether color column exists
    if color is not None and color in df.columns:

        fig = px.scatter(
            df,
            x=x,
            y=y,
            color=color,
            color_discrete_sequence=px.colors.qualitative.Plotly
        )

    else:

        fig = px.scatter(
            df,
            x=x,
            y=y,
            color_discrete_sequence=px.colors.qualitative.Plotly
        )

    # marker styling
    fig.update_traces(
        marker=dict(
            size=13,
            opacity=0.9
        )
    )

    # layout styling
    fig.update_layout(
        height=height,
        plot_bgcolor="#020B1F",
        paper_bgcolor="#020B1F",
        font=dict(color="#E2E8F0"),
        margin=dict(l=20, r=20, t=20, b=20),

        xaxis=dict(
            showgrid=True,
            gridcolor="#1E293B",
            title=x
        ),

        yaxis=dict(
            showgrid=True,
            gridcolor="#1E293B",
            title=y
        ),

        legend=dict(
            title=color if color else "",
            font=dict(size=11)
        )
    )

    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# WORLD MAP (CHOROPLETH)
# Shows geographic distributions
# ============================================================

def map(df, location, color, title=None, height=420):

    fig = px.choropleth(
        df,
        locations=location,
        locationmode="country names",
        color=color,
        title=title,
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        height=height,
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor="#E8EAEF",
        paper_bgcolor="#0F1C3D",

        geo=dict(
            bgcolor="#EFF1F5",
            projection_scale=1.15
        )
    )

    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# TABLE DISPLAY
# ============================================================

def show_table(df):
    st.dataframe(df, use_container_width=True)


# ============================================================
# KPI METRIC
# ============================================================

def kpi(title, value):
    st.metric(label=title, value=value)