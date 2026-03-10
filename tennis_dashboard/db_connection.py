from sqlalchemy import create_engine
import os
import dotenv
import pandas as pd
import streamlit as st
dotenv.load_dotenv(".env")


@st.cache_resource
def get_engine():

    engine = create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    return engine

# LOAD TABLES INTO PANDAS
@st.cache_data
def load_tables():
    engine = get_engine()

    tables = ["category","competition","competitor",
              "complex","ranking","venue"]

    dfs = {
        t: pd.read_sql_query(f"SELECT * FROM tennis.{t}", engine)
        for t in tables
    }

    return dfs