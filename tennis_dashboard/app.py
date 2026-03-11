import streamlit as st
import pandas as pd
import os
from db_connection import load_tables
from utils.charts import *
from utils.filter import *
from utils.formatters import *
import importlib

st.set_page_config(page_title="Tennis Analytics", page_icon="🎾", layout="wide")
st.set_page_config(page_title="Tennis Analytics", page_icon="🎾", layout="wide")

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)
# ------------------------------------------------------------------------
# LOAD & CLEAN DATA
# ------------------------------------------------------------------------

@st.cache_data
def get_clean_data():
    category_df, competition_df, competitor_df, complex_df, ranking_df, venue_df = load_tables().values()

    competitor_df = strip_whitespace(competitor_df, ['country', 'country_code'])
    venue_df      = strip_whitespace(venue_df, ['country_name', 'country_code'])
    ranking_df    = add_movement_category(ranking_df)
    ranking_df    = add_rank_tier(ranking_df, rank_col='rank_position')
    ranking_df    = merge_competitor_names(ranking_df, competitor_df)
    competition_df = competition_df.merge(
        category_df, left_on='category_id', right_on='id', suffixes=('', '_cat')
    )

    return category_df, competition_df, competitor_df, complex_df, ranking_df, venue_df

category_df, competition_df, competitor_df, complex_df, ranking_df, venue_df = get_clean_data()

# ------------------------------------------------------------------------
# SIDEBAR — GLOBAL FILTERS
# ------------------------------------------------------------------------

with st.sidebar:
    st.title("🎾 Tennis Analytics")
    st.divider()
    st.header("Global Filters")

    gender_filter   = multi_filter(ranking_df, 'gender', 'Gender')
    country_filter  = multi_filter(competitor_df, 'country', 'Country')
    category_filter = multi_filter(category_df, 'category_name', 'Category')
    tier_filter     = multi_filter(
        pd.DataFrame({'rank_tier': ['Top 10', '11–50', '51–100', '100+']}),
        'rank_tier', 'Rank Tier'
    )
    rank_range = rank_filter(ranking_df, 'rank_position', 'Rank Range')

    st.divider()
    selected_page = st.radio("Navigate", [
        "Overview",
        "Player Performance",
        "Ranking & Competition Dynamics",
        "Country Analysis",
        "Infrastructure"
    ])

# ------------------------------------------------------------------------
# FILTERED DATAFRAMES
# ------------------------------------------------------------------------

filtered_ranking = apply_filters(ranking_df.copy(), {
    'gender': gender_filter, 'country': country_filter, 'rank_tier': tier_filter
})
filtered_ranking = filtered_ranking[
    (filtered_ranking['rank_position'] >= rank_range[0]) &
    (filtered_ranking['rank_position'] <= rank_range[1])
]

filtered_competitor = apply_filters(competitor_df.copy(), {'country': country_filter})

filtered_competition = apply_filters(competition_df.copy(), {
    'gender': gender_filter, 'category_name': category_filter
})

# store in session_state so pages can access
st.session_state.update({
    'filtered_ranking'    : filtered_ranking,
    'filtered_competitor' : filtered_competitor,
    'filtered_competition': filtered_competition,
    'category_df'         : category_df,
    'competition_df'      : competition_df,
    'competitor_df'       : competitor_df,
    'complex_df'          : complex_df,
    'ranking_df'          : ranking_df,
    'venue_df'            : venue_df,
})

# ------------------------------------------------------------------------
# PAGE ROUTING
# ------------------------------------------------------------------------

if selected_page == "Overview":
    import pages.page1_overview as page
elif selected_page == "Player Performance":
    import pages.page2_player_performance as page
elif selected_page == "Ranking & Competition Dynamics":
    import pages.page3_ranking_dynamics as page
elif selected_page == "Country Analysis":
    import pages.page4_country_analysis as page
elif selected_page == "Infrastructure":
    import pages.page5_infrastructure as page
importlib.reload(page)
page.show()