import streamlit as st

#------------------------------
# multiselect filter
#------------------------------------------

def multi_filter(df, col, label = None): # use this for country, category, gender
    base_work = sorted(df[col].dropna().unique()) # remove Null and sort uniques
    selected = st.multiselect(label, base_work)
    return selected


#------------------------------------------
# Rank range filter
#------------------------------------------

def rank_filter(df, col, label = None): # rank

    min_rank = int(df[col].min())
    max_rank = int(df[col].max())
    selected_range = st.slider(label, min_value = min_rank, max_value = max_rank, value = (min_rank, max_rank))
    return selected_range