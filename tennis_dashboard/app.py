import streamlit as st
import pandas as pd
import os
from db_connection import load_tables
from utils.charts import *
from utils.filter import *
from utils.formatters import *
import importlib


# ============================================================
# STREAMLIT PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Tennis Analytics",
    page_icon="🎾",
    layout="wide"
)


# ============================================================
# GLOBAL DASHBOARD STYLE (CSS)
# ============================================================

st.markdown("""
<style>

/* ===== MAIN APP ===== */

.stApp{
background:#020B1F;
color:#E2E8F0;
font-family:Segoe UI, sans-serif;
}

/* ===== PAGE CONTAINER ===== */

.block-container{
padding-top:1rem;
padding-left:1.5rem;
padding-right:1.5rem;
max-width:100%;
}

/* ===== SIDEBAR ===== */

[data-testid="stSidebarNav"] {
display: none;
}

section[data-testid="stSidebar"]{
background:#0B1630;
width:250px;
border-right:1px solid #1E293B;
}

section[data-testid="stSidebar"] label{
font-size:13px;
color:#CBD5F5;
}

section[data-testid="stSidebar"] h1{
color:#FFFFFF;
font-size:20px;
margin-bottom:6px;
}

/* sidebar navigation hover */

section[data-testid="stSidebar"] .stRadio label:hover{
background:rgba(34,211,238,0.1);
border-radius:6px;
}

/* ===== KPI CARDS ===== */

div[data-testid="metric-container"]{
background:#020B1F;
border:2px solid #22D3EE;
border-radius:8px;
padding:4px 8px;
min-height:50px;
box-shadow:0 0 6px rgba(34,211,238,0.2);
}

div[data-testid="metric-container"] label{
font-size:13px;
color:#CBD5F5;
}

div[data-testid="metric-container"] div{
font-size:20px;
font-weight:600;
}

/* ===== CHART CARDS ===== */

.element-container:has(.js-plotly-plot){
background:#0F1C3D;
border-radius:10px;
border-top:4px solid #22D3EE;
padding:12px;
box-shadow:0 0 10px rgba(34,211,238,0.2);
}

.element-container:has(.js-plotly-plot):hover{
box-shadow:0 0 18px rgba(34,211,238,0.5);
}

/* ===== CHART SIZE ===== */

.js-plotly-plot{
min-height:360px;
}

/* ===== TITLES ===== */

h1{
font-size:30px;
margin-bottom:0.2rem;
}

h2{
font-size:18px;
color:#22D3EE;
margin-bottom:0.1rem;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def get_clean_data():

    category_df, competition_df, competitor_df, complex_df, ranking_df, venue_df = load_tables().values()

    competitor_df = strip_whitespace(competitor_df, ['country','country_code'])
    venue_df = strip_whitespace(venue_df, ['country_name','country_code'])

    ranking_df = add_movement_category(ranking_df)
    ranking_df = add_rank_tier(ranking_df,'rank_position')
    ranking_df = merge_competitor_names(ranking_df,competitor_df)

    competition_df = competition_df.merge(
        category_df,
        left_on='category_id',
        right_on='id',
        suffixes=('','_cat')
    )

    return category_df,competition_df,competitor_df,complex_df,ranking_df,venue_df


# load data
category_df,competition_df,competitor_df,complex_df,ranking_df,venue_df = get_clean_data()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🎾 Tennis Analytics")

    # -----------------------------
    # Page Navigation
    # -----------------------------

    selected_page = st.radio("Navigate",[
        "Overview",
        "Player Performance",
        "Ranking & Competition Dynamics",
        "Country Analysis",
        "Infrastructure"
    ])

    st.divider()

    # -----------------------------
    # Filters
    # -----------------------------

    st.header("Filters")

    gender_filter = multi_filter(ranking_df,'gender','Gender')
    country_filter = multi_filter(competitor_df,'country','Country')
    category_filter = multi_filter(category_df,'category_name','Category')

    tier_filter = multi_filter(
        pd.DataFrame({'rank_tier':['Top 10','11–50','51–100','100+']}),
        'rank_tier',
        'Rank Tier'
    )

    rank_range = rank_filter(ranking_df,'rank_position','Rank Range')


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_ranking = apply_filters(ranking_df.copy(),{
    'gender':gender_filter,
    'country':country_filter,
    'rank_tier':tier_filter
})

filtered_ranking = filtered_ranking[
    (filtered_ranking['rank_position']>=rank_range[0]) &
    (filtered_ranking['rank_position']<=rank_range[1])
]

filtered_competitor = apply_filters(
    competitor_df.copy(),
    {'country':country_filter}
)

filtered_competition = apply_filters(
    competition_df.copy(),
    {'gender':gender_filter,'category_name':category_filter}
)


# ============================================================
# STORE DATA IN SESSION STATE
# ============================================================

st.session_state.update({
    'filtered_ranking':filtered_ranking,
    'filtered_competitor':filtered_competitor,
    'filtered_competition':filtered_competition,
    'category_df':category_df,
    'competition_df':competition_df,
    'competitor_df':competitor_df,
    'complex_df':complex_df,
    'ranking_df':ranking_df,
    'venue_df':venue_df
})


# ============================================================
# PAGE ROUTING
# ============================================================

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


# reload page
importlib.reload(page)

# run page
page.show()