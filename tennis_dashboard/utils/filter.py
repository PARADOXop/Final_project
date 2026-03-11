import streamlit as st

# ------------------------------------------
# Multiselect filter
# ------------------------------------------

def multi_filter(df, col, label=None):
    base_work = sorted(df[col].dropna().unique())
    selected = st.multiselect(label, base_work)
    return selected


# ------------------------------------------
# Rank range filter
# ------------------------------------------

def rank_filter(df, col, label=None):
    min_rank = int(df[col].dropna().min())
    max_rank = int(df[col].dropna().max())
    selected_range = st.slider(label, min_value=min_rank, max_value=max_rank, value=(min_rank, max_rank))
    return selected_range



# ------------------------------------------
# Apply filters to a dataframe
# ------------------------------------------

def apply_filters(df, filters: dict):
    """
    filters = {'column_name': selected_list}
    Only filters if selection is non-empty.
    """
    for col, selected in filters.items():
        if selected and col in df.columns:
            df = df[df[col].isin(selected)]
    return df