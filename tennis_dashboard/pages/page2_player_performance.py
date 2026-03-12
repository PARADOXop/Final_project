import streamlit as st
import pandas as pd
from utils.charts import *
from utils.filter import *
from utils.formatters import *


def show():
    filtered_ranking = st.session_state['filtered_ranking']

    st.title("Player Performance")
    st.caption("How do competitors differ in activity, output, and ranking tier — and does playing more actually help?")
    st.divider()

    # --------------------------------------------------------------------
    # Q1 — Competitions played distribution
    # --------------------------------------------------------------------

    hist_chart(filtered_ranking, x='competitions_played', title='How many competitions does each competitor play?')
    st.caption("💡 Most competitors play between 20–27 competitions, suggesting a consistent tour schedule regardless of ranking.")

    # --------------------------------------------------------------------
    # Q2 — Correlation: competitions played vs points
    # --------------------------------------------------------------------

    scatter_chart(
        filtered_ranking,
        x='competitions_played',
        y='points',
        color='gender',
        title='Does playing more competitions lead to more ranking points?'
    )
    st.caption("💡 Near-zero correlation (r=0.009) between competitions played and points — playing more does not guarantee higher rankings.")

    # --------------------------------------------------------------------
    # Q3 — Rank tier analysis
    # --------------------------------------------------------------------

    tier_df = filtered_ranking.groupby('rank_tier', observed=True)[['points', 'competitions_played']].mean().round(2).reset_index()

    c1, c2 = st.columns(2)
    with c1:
        bar_chart(tier_df, x='rank_tier', y='points', title='Avg Points by Rank Tier')
        st.caption("💡 Top 10 players earn 7x more points than the 51–100 tier, proving elite dominance is disproportionate to effort.")
    with c2:
        bar_chart(tier_df, x='rank_tier', y='competitions_played', title='Avg Competitions Played by Rank Tier')
        st.caption("💡 Ranked 51–100 players compete the most but earn the fewest points per competition — quantity doesn't equal quality.")