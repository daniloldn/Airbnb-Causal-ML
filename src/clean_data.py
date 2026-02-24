import pandas as pd
import numpy as np
from pathlib import Path
from load_data import load_data, PROCESSED

def clean_data() -> pd.DataFrame:

    df = load_data()

    #dropping columns that are not relevant for our analysis
    drop_cols = ["listing_url", "name",
                  "source","picture_url", "host_url", "host_id",
                "host_thumbnail_url", "host_picture_url", "estimated_occupancy_l365d", "estimated_revenue_l365d",
                  "host_location" ,"host_name", "neighbourhood_group_cleansed", "neighbourhood",
                  "availability_30", "availability_60", "availability_90", "availability_365", "availability_eoy",
                   "minimum_minimum_nights", "maximum_minimum_nights", "minimum_maximum_nights", "maximum_maximum_nights",
                   "minimum_nights_avg_ntm", "maximum_nights_avg_ntm", "calendar_updated", "calendar_last_scraped",
                   "has_availability","host_neighbourhood", "bathrooms_text",
                   "number_of_reviews_ltm", "number_of_reviews_l30d", "number_of_reviews_ly","reviews_per_month",
                   "license"]
    
    df.drop(columns=drop_cols, inplace=True)

    # converting data types to correct types
    df["last_scraped"] = pd.to_datetime(df["last_scraped"])
    df["host_since"] = pd.to_datetime(df["host_since"])
    df["host_response_rate"] = df["host_response_rate"].str.rstrip("%").astype("float") / 100
    df["price"] = df["price"].str.replace("$", "").str.replace(",", "").astype("float")
    df["first_review"] = pd.to_datetime(df["first_review"])
    df["last_review"] = pd.to_datetime(df["last_review"])
    df["instant_bookable"] = df["instant_bookable"].map({"t": 1, "f": 0}).astype("int8")
    df["host_verifications"] = df["host_verifications"].apply(lambda x: len(x.strip("[]").split(", ")) if pd.notnull(x) else 0).astype("int8")
    df["host_acceptance_rate"] = df["host_acceptance_rate"].str.rstrip("%").astype("float") / 100


    Path(PROCESSED).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED, index=False)

    return None