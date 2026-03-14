from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
import os

def get_credentials():
    try:
        # Try Streamlit Cloud secrets first
        return {
            "user"    : st.secrets["DB_USER"],
            "password": st.secrets["DB_PASSWORD"],
            "host"    : st.secrets["DB_HOST"],
            "port"    : st.secrets["DB_PORT"],
            "name"    : st.secrets["DB_NAME"],
        }
    except:
        # Fall back to .env for local
        import dotenv
        dotenv.load_dotenv()
        return {
            "user"    : os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host"    : os.getenv("DB_HOST"),
            "port"    : os.getenv("DB_PORT"),
            "name"    : os.getenv("DB_NAME"),
        }

@st.cache_resource
def get_engine():
    creds = get_credentials()
    engine = create_engine(
        f"postgresql+psycopg2://{creds['user']}:{creds['password']}"
        f"@{creds['host']}:{creds['port']}/{creds['name']}"
    )
    return engine

@st.cache_data
def load_tables():
    engine = get_engine()
    tables = ["category", "competition", "competitor", "complex", "ranking", "venue"]
    dfs = {
        t: pd.read_sql_query(f"SELECT * FROM tennis.{t}", engine)
        for t in tables
    }
    return dfs