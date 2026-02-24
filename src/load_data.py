import pandas as pd
from pathlib import Path


RAW = Path(__file__).parent.parent/"data"/"raw"/"listings.csv"
PROCESSED = Path(__file__).parent.parent/"data"/"processed"/"processed_listings.csv"
FEATURE = Path(__file__).parent.parent/"data"/"feature"/"listings_features.csv"


def load_data() -> pd.DataFrame:
    return pd.read_csv(RAW)

def load_processed() -> pd.DataFrame:
    return pd.read_csv(PROCESSED,  parse_dates=["last_scraped", "host_since", "first_review", "last_review"])

def load_feature() -> pd.DataFrame:
    return pd.read_csv(FEATURE)