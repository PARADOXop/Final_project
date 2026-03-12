import streamlit as st
import plotly.express as px
import pandas as pd


# -----------------------------------
# COLOR PALETTE
# -----------------------------------

COLOR_PALETTE = [
    "#1f77b4",  # blue
    "#ff7f0e",  # orange
    "#2ca02c",  # green
    "#d62728",  # red
    "#9467bd",  # purple
    "#8c564b",  # brown
]


# -----------------------------------
# MAP
# -----------------------------------

def map(df, location, color, title=None):
    fig = px.choropleth(
        df,
        locations=location,
        locationmode="country names",
        color=color,
        color_continuous_scale="Blues",
        title=title
    )
    st.plotly_chart(fig, use_container_width=True)


# -----------------------------------
# BAR CHART
# -----------------------------------

def bar_chart(df: pd.DataFrame, x: str, y: str, title: str = None):
    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)


# -----------------------------------
# HISTOGRAM
# -----------------------------------

def hist_chart(df: pd.DataFrame, x: str, title: str = None, nbins: int = 20):
    fig = px.histogram(
        df,
        x=x,
        nbins=nbins,
        title=title,
        color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


# -----------------------------------
# SCATTER PLOT
# -----------------------------------

def scatter_chart(df: pd.DataFrame, x: str, y: str, color: str = None, title: str = None):
    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        color_discrete_sequence=COLOR_PALETTE
    )
    st.plotly_chart(fig, use_container_width=True)


# -----------------------------------
# LINE CHART
# -----------------------------------

def line_chart(df: pd.DataFrame, x: str, y: str, title: str = None):
    fig = px.line(
        df,
        x=x,
        y=y,
        title=title,
        markers=True,
        color_discrete_sequence=COLOR_PALETTE
    )
    st.plotly_chart(fig, use_container_width=True)


# -----------------------------------
# AREA CHART
# -----------------------------------

def area_chart(df: pd.DataFrame, x: str, y: str, title: str = None):
    fig = px.area(
        df,
        x=x,
        y=y,
        title=title,
        color_discrete_sequence=COLOR_PALETTE
    )
    st.plotly_chart(fig, use_container_width=True)


# -----------------------------------
# PIE CHART
# -----------------------------------

def pie_chart(df: pd.DataFrame, names: str, values: str, title: str = None):
    fig = px.pie(
        df,
        names=names,
        values=values,
        title=title,
        color_discrete_sequence=COLOR_PALETTE
    )
    st.plotly_chart(fig, use_container_width=True)


# -----------------------------------
# DATA TABLE
# -----------------------------------

def show_table(df: pd.DataFrame):
    st.dataframe(df, use_container_width=True)


# -----------------------------------
# SINGLE KPI
# -----------------------------------

def kpi(title: str, value):
    st.metric(label=title, value=value)


# -----------------------------------
# KPI WITH DELTA
# -----------------------------------

def kpi_delta(title: str, value, delta):
    st.metric(label=title, value=value, delta=delta)


# -----------------------------------
# MULTIPLE KPIs ROW
# -----------------------------------

def kpi_row(metrics: dict):
    cols = st.columns(len(metrics))
    for col, (label, value) in zip(cols, metrics.items()):
        col.metric(label, value)