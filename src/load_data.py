import pandas as pd


def load_data() -> pd.DataFrame:
    return pd.read_csv('../data/raw/listings.csv')

def load_processed() -> pd.DataFrame:
    return pd.read_csv("../data/processed/clean_listings.csv")