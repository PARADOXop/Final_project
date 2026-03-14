import streamlit as st
import pandas as pd
import plotly.express as px
from utils.charts import *
from utils.formatters import *

def show():

    filtered_ranking = st.session_state['filtered_ranking']
    venue_df = st.session_state['venue_df']

    st.title("🌍 Country Analysis")
    st.caption("Which nations dominate tennis — and does where you're from determine your elite potential?")
    st.divider()

    # --------------------------------------------------------------------
    # Q1 — Which countries produce the most top-50 competitors?
    # --------------------------------------------------------------------

    st.subheader("Which countries produce the most top-50 competitors?")

    top50 = filtered_ranking[filtered_ranking['rank_position'] <= 50]

    top50_by_country = top50.groupby('country')['competitor_id'].count().reset_index(name='count')

    total = filtered_ranking.groupby('country')['competitor_id'].count()
    elite = top50.groupby('country')['competitor_id'].count()

    elite_df = pd.DataFrame({'total': total, 'top50': elite}).fillna(0).reset_index()
    elite_df['ratio'] = elite_df['top50'] / elite_df['total'] * 100

    c1, c2 = st.columns(2)

    with c1:
        bar_chart(top50_by_country, 'country', 'count', 'Top Countries by Top50 Players')
        st.caption("💡 USA and Czechia dominate the top 50 — together accounting for over 30 of the 50 spots across ATP and WTA tours.")

    with c2:
        bar_chart(elite_df, 'country', 'ratio', 'Country Elite Ratio — % of Competitors in Top 50')
        st.caption("💡 Smaller nations like Denmark and Norway convert a higher % of their competitors into top-50 players — quality over quantity.")

    st.divider()

    # --------------------------------------------------------------------
    # Q2 — Geographic mismatch: venues vs elite players
    # --------------------------------------------------------------------

    st.subheader("Which top-50 countries host no venues — and which venue-rich countries produce no elite players?")
    # normalize venue country names to title case
    venue_country_counts = venue_df['country_name'].str.title().value_counts().reset_index(name='venue_count')
    venue_country_counts.columns = ['country', 'venue_count']

    # top 50 competitor countries — already filtered via filtered_ranking
    top50_country_counts = top50.groupby('country')['competitor_id'].count().reset_index(name='top50_count')
    top50_country_counts = top50_country_counts[top50_country_counts['country'] != 'Neutral']

    # merge both
    mismatch_df = pd.merge(top50_country_counts, venue_country_counts, on='country', how='outer').fillna(0)
    mismatch_df['top50_count'] = mismatch_df['top50_count'].astype(int)
    mismatch_df['venue_count'] = mismatch_df['venue_count'].astype(int)
    mismatch_df['bubble_size'] = mismatch_df['top50_count'].clip(lower=1)
    mismatch_df = mismatch_df[mismatch_df['country'] != 'Neutral']

    fig = px.scatter(
        mismatch_df,
        x='venue_count',
        y='top50_count',
        color='country',
        size='bubble_size',
        size_max=30,
        title='Venue Hosting vs Elite Player Production by Country',
        labels={'venue_count': 'Number of Venues Hosted', 'top50_count': 'Top-50 Competitors'},
    )
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="v",
            x=1.02,
            y=1,
            font=dict(size=10),
        ),
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("💡 USA, Czechia and France are outliers — either producing many elite players without hosting proportionally, or vice versa. Many top-50 countries host zero venues.")