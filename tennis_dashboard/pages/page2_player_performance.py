import streamlit as st
import pandas as pd
from utils.charts import *
from utils.filter import *
from utils.formatters import *

def show():

    filtered_ranking = st.session_state['filtered_ranking']

    st.title("📊 Player Performance")
    st.caption("Understand how player activity and tournament participation influence ranking performance.")
    st.divider()

    # --------------------------------------------------------------------
    # Competitions Played Distribution
    # --------------------------------------------------------------------

    c1, c2 = st.columns(2)

    with c1:
        hist_chart(filtered_ranking,'competitions_played',title='How many competitions do players typically participate in?')
        st.caption("💡 Most competitors play between 20–27 competitions, suggesting a consistent tour schedule regardless of ranking.")

    with c2:
        scatter_chart(filtered_ranking,'competitions_played','points','gender',title='How does the number of competitions relate to ranking points?')
        st.caption("💡 Near-zero correlation (r=0.009) between competitions played and points — playing more does not guarantee higher rankings.")

    st.divider()

    # --------------------------------------------------------------------
    # Performance by Rank Tier
    # --------------------------------------------------------------------

    tier_df = filtered_ranking.groupby('rank_tier',observed=True)[['points','competitions_played']].mean().round(2).reset_index()

    c3, c4 = st.columns(2)
    with c3:
        bar_chart(tier_df, x='rank_tier', y='points', title='Avg Points by Rank Tier')
        st.caption("💡 Top 10 players earn 7x more points than the 51–100 tier, proving elite dominance is disproportionate to effort.")
    with c4:
        bar_chart(tier_df, x='rank_tier', y='competitions_played', title='Avg Competitions Played by Rank Tier')
        st.caption("💡 Ranked 51–100 players compete the most but earn the fewest points per competition — quantity doesn't equal quality.")