import streamlit as st
import pandas as pd
from utils.charts import *
from utils.filter import *
from utils.formatters import *


def show():

    filtered_ranking     = st.session_state['filtered_ranking']
    filtered_competitor  = st.session_state['filtered_competitor']
    filtered_competition = st.session_state['filtered_competition']
    venue_df             = st.session_state['venue_df']

    st.title("🏠 Overview")
    st.caption("How player performance, national representation, tournament participation, and global infrastructure shape success in professional tennis.")
    st.divider()

    # --------------------------------------------------------------------
    # KPIs
    # --------------------------------------------------------------------

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        kpi('Total Competitors', filtered_competitor['competitor_id'].nunique())

    with k2:
        kpi('Total Competitions', filtered_competition['id'].nunique())

    with k3:
        kpi('Total Venues', venue_df['id'].nunique())

    with k4:
        kpi('Total Countries', filtered_competitor['country'].nunique())

    st.divider()

    # --------------------------------------------------------------------
    # Rank Movement Distribution + Competition Categories
    # --------------------------------------------------------------------

    c1, c2 = st.columns(2)

    movement_dist = filtered_ranking['movement_category'].value_counts().reset_index(name='count')
    cat_dist = filtered_competition.groupby('category_name')['id'].count().reset_index(name='count').sort_values('count', ascending=False)

    with c1:
        bar_chart(movement_dist, x='movement_category', y='count', title='What is the distribution of rank movement?')
        st.caption("💡 More players lost ranking positions than gained, with ~10% showing no movement — likely due to inactivity.")

    with c2:
        bar_chart(cat_dist, x='category_name', y='count', title='How are competitions distributed across categories?')
        st.caption("💡 ITF tournaments make up over 65% of all competitions, highlighting tennis's vast grassroots infrastructure beneath the elite ATP/WTA circuit.")

    st.divider()

    # --------------------------------------------------------------------
    # Global Competitor Distribution
    # --------------------------------------------------------------------

    country_dist = filtered_competitor['country'].value_counts().reset_index(name='count')

    map(country_dist, location='country', color='count', title="Where do the world's top competitors come from?")
    st.caption("💡 USA leads with 103 competitors, nearly double second-placed France — reflecting deep tennis infrastructure and funding.")