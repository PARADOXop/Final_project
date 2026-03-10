import streamlit as st
from db_connection import get_engine
import psycopg2
import os
import dotenv
import pandas as pd
import utils
from utils.charts import *
from utils.filter import *
from db_connection import load_tables

tables = load_tables()

category_df, competition_df, competitor_df, complex_df, ranking_df, venue_df = load_tables().values()


with st.sidebar:

    category_filter = multi_filter(
        category_df,
        "category_name",
        "Category"
    )

    competition_filter = multi_filter(
        venue_df,
        "country_name",
        "country"
    )

    country_filter = multi_filter(
        ranking_df,
        "gender",
        "gender"
    )

    rank_range = rank_filter(
        ranking_df,
        "rank_position",
        "rank"
    )
    
    