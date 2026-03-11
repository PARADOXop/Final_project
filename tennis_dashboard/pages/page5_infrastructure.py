import streamlit as st
import pandas as pd
import plotly.express as px
from utils.charts import *
from utils.formatters import *


def show():
    venue_df             = st.session_state['venue_df']
    complex_df           = st.session_state['complex_df']
    filtered_competition = st.session_state['filtered_competition']

    st.title("Infrastructure")
    st.caption("How is tennis infrastructure distributed globally — and where are the gaps in competition data?")
    st.divider()

    # --------------------------------------------------------------------
    # Q1 — Venue distribution by country
    # --------------------------------------------------------------------

    st.subheader("Which countries host the most tennis venues?")

    venue_by_country = venue_df['country_name'].str.title().value_counts().reset_index(name='count')
    venue_by_country.columns = ['country', 'count']

    c1, c2 = st.columns(2)
    with c1:
        bar_chart(
            venue_by_country.head(15),
            x='country', y='count',
            title='Top 15 Countries by Number of Venues'
        )
        st.caption("💡 USA hosts nearly 3x more venues than any other country — reflecting its massive domestic tennis infrastructure.")

    with c2:
        map(venue_by_country, location='country', color='count', title='Global Venue Distribution')
        st.caption("💡 Europe and North America dominate venue hosting, with Asia emerging as a growing tennis hub.")

    st.divider()

    # --------------------------------------------------------------------
    # Q2 — Complexes hosting most venues
    # --------------------------------------------------------------------

    st.subheader("Which complexes host the most venues?")

    venue_complex = venue_df.merge(complex_df, on='complex_id', how='left')
    venue_complex['country_name'] = venue_complex['country_name'].str.title()

    complex_counts = venue_complex.groupby(['name_y', 'country_name'])['id'].count().reset_index(name='venue_count')
    complex_counts.columns = ['complex_name', 'country', 'venue_count']
    complex_counts = complex_counts.sort_values('venue_count', ascending=False).head(15)

    bar_chart(complex_counts, x='complex_name', y='venue_count', title='Top 15 Complexes by Number of Venues')
    st.caption("💡 Buenos Aires Lawn Tennis Club leads globally with 29 venues — South America punches above its weight in tennis infrastructure.")

    st.divider()

    # --------------------------------------------------------------------
    # Q3 — Hierarchy depth vs category
    # --------------------------------------------------------------------

    st.subheader("Which categories have the most orphaned competitions?")

    comp = filtered_competition.copy()
    valid_ids = set(comp['id'].astype(str))

    def classify(val):
        val = str(val).strip()
        if val == 'ROOT':      return 'Root'
        elif val in valid_ids: return 'Child'
        else:                  return 'Orphaned'

    comp['hierarchy_flag'] = comp['parent_id'].apply(classify)

    orphan_df = comp[comp['hierarchy_flag'] == 'Orphaned'].groupby('category_name')['id'].count().reset_index(name='orphaned_count')
    total_df  = comp.groupby('category_name')['id'].count().reset_index(name='total_count')

    hierarchy_summary = orphan_df.merge(total_df, on='category_name')
    hierarchy_summary['orphan_pct'] = (hierarchy_summary['orphaned_count'] / hierarchy_summary['total_count'] * 100).round(1)
    hierarchy_summary = hierarchy_summary.sort_values('orphaned_count', ascending=False)

    bar_chart(hierarchy_summary, x='category_name', y='orphaned_count', title='Orphaned Competitions by Category')
    st.caption("💡 ITF Men and Women have the most orphaned competitions — data incompleteness is concentrated in grassroots categories, not elite ones.")
