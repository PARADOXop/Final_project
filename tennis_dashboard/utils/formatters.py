import pandas as pd


# --------------------------------------------------
# STRIP WHITESPACE FROM STRING COLUMNS
# --------------------------------------------------

def strip_whitespace(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    for col in cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    return df


# --------------------------------------------------
# RANK TIER BUCKETING
# --------------------------------------------------

def add_rank_tier(df: pd.DataFrame, rank_col: str = "rank_position") -> pd.DataFrame:
    bins = [0, 10, 50, 100, float("inf")]
    labels = ["Top 10", "11–50", "51–100", "100+"]
    df["rank_tier"] = pd.cut(df[rank_col], bins=bins, labels=labels, right=True)
    return df


# --------------------------------------------------
# MOVEMENT CATEGORY
# --------------------------------------------------

def add_movement_category(df: pd.DataFrame, movement_col: str = "movement") -> pd.DataFrame:
    def categorize(val):
        if val > 0:
            return "Gained"
        elif val < 0:
            return "Lost"
        else:
            return "No Change"
    df["movement_category"] = df[movement_col].apply(categorize)
    return df


# --------------------------------------------------
# MERGE COMPETITOR NAMES INTO RANKING
# --------------------------------------------------

def merge_competitor_names(ranking_df: pd.DataFrame, competitor_df: pd.DataFrame) -> pd.DataFrame:
    competitor_clean = strip_whitespace(competitor_df.copy(), ["country_code", "country"])
    merged = ranking_df.merge(
        competitor_clean[["competitor_id", "name", "country", "country_code"]],
        on="competitor_id",
        how="left"
    )
    return merged


# --------------------------------------------------
# FORMAT LARGE NUMBERS
# --------------------------------------------------

def format_number(val: int) -> str:
    if val >= 1000:
        return f"{val / 1000:.1f}K"
    return str(val)