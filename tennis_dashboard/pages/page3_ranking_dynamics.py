import streamlit as st
import pandas as pd
from utils.charts import *
from utils.formatters import *


def show():
    filtered_ranking     = st.session_state['filtered_ranking']
    filtered_competition = st.session_state['filtered_competition']

    st.title("📈 Ranking & Competition Dynamics")
    st.caption("Who is rising and falling fast — and how deep does the competition hierarchy go?")
    st.divider()

    # --------------------------------------------------------------------
    # Q1 — Rank movement outliers
    # --------------------------------------------------------------------

    st.subheader("Who are the biggest movers in the rankings?")

    gain_threshold = filtered_ranking['movement'].quantile(0.95)
    loss_threshold = filtered_ranking['movement'].quantile(0.05)

    gainers = filtered_ranking[filtered_ranking['movement'] >= gain_threshold][
        ['name', 'country', 'movement', 'competitions_played', 'tour', 'rank_position']
    ].sort_values('movement', ascending=False).reset_index(drop=True)

    losers = filtered_ranking[filtered_ranking['movement'] <= loss_threshold][
        ['name', 'country', 'movement', 'competitions_played', 'tour', 'rank_position']
    ].sort_values('movement').reset_index(drop=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🔺 Top 5% Gainers")
        bar_chart(
            gainers.head(10),
            x='name', y='movement',
            title='Biggest Rank Gainers'
        )
        st.caption("💡 Top gainers tend to have moderate competition counts — strategic scheduling, not volume, drives big jumps.")
        show_table(gainers.head(10))

    with c2:
        st.markdown("#### 🔻 Top 5% Losers")
        bar_chart(
            losers.head(10),
            x='name', y='movement',
            title='Biggest Rank Losers'
        )
        st.caption("💡 Top losers often played more competitions — suggesting injury, fatigue, or form loss after heavy schedules.")
        show_table(losers.head(10))

    st.divider()

    # --------------------------------------------------------------------
    # Q2 — Competition parent-child hierarchy
    # --------------------------------------------------------------------

    st.subheader("Which categories have the most orphaned competitions?")

    comp = filtered_competition.copy()
    valid_ids = set(comp['id'].astype(str))

    def classify(val):
        val = str(val).strip()
        if val == 'ROOT':   return 'Root'
        elif val in valid_ids: return 'Child'
        else:               return 'Orphaned'

    comp['hierarchy_flag'] = comp['parent_id'].apply(classify)

    hierarchy_df = comp.groupby(['category_name', 'hierarchy_flag'])['id'].count().reset_index(name='count')

    # stacked bar
    import plotly.express as px
    fig = px.bar(
        hierarchy_df,
        x='category_name',
        y='count',
        color='hierarchy_flag',
        title='Competition Hierarchy by Category',
        color_discrete_sequence=['#1f77b4', '#d62728', '#2ca02c'],
        barmode='stack'
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, width='stretch')
    st.caption("💡 Most ATP, WTA, and Challenger competitions are orphaned — meaning parent references are missing, concentrated in elite categories.")
