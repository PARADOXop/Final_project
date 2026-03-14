from sqlalchemy import create_engine
import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path

# ---------------------------------------------------
# LOAD .env SAFELY
# ---------------------------------------------------

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)

# ---------------------------------------------------
# DATABASE ENGINE
# ---------------------------------------------------

@st.cache_resource
def get_engine():

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME")

    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    return engine


# ---------------------------------------------------
# LOAD TABLES
# ---------------------------------------------------

@st.cache_data
def load_tables():

    engine = get_engine()

    tables = [
        "category",
        "competition",
        "competitor",
        "complex",
        "ranking",
        "venue"
    ]

    dfs = {
        t: pd.read_sql_query(f"SELECT * FROM tennis.{t}", engine)
        for t in tables
    }

    return dfs