import pandas as pd
import numpy as np
from src.load_data import load_processed
from pathlib import Path


def feature_eng() -> pd.DataFrame:

    df = load_processed()


    #host features
    df["experience"] = df["last_scraped"].dt.year - df["host_since"].dt.year
    df["desc_dummy"] = df["description"].apply(lambda x: 0 if pd.isnull(x) else 1)
    df["about_dummy"] = df["host_about"].apply(lambda x: 0 if pd.isnull(x) else 1)
    df["overveiw_dummy"] = df["neighborhood_overview"].apply(lambda x: 0 if pd.isnull(x) else 1)
    df["cat_response_time"] = df["host_response_time"].apply(
    lambda x: 1 if x == "within an hour" 
    else 2 if x == "within a few hours" 
    else 3 if x == "within a day"
    else 4
)


    #converting categorical variables
    df["host_is_superhost"] = df["host_is_superhost"].map({"t": 1, "f": 0}).astype("int8")
    df["host_identity_verified"] = df["host_identity_verified"].map({"t": 1, "f": 0}).astype("int8")
    df["host_has_profile_pic"] = df["host_has_profile_pic"].map({"t": 1, "f": 0}).astype("int8")
    
    
    #property dummies
    df["shared"] = df["property_type"].apply(lambda x: 1 if "Shared" in x else 0)
    df["entire"] = df["property_type"].apply(lambda x: 1 if "Entire" in x else 0)
    df["private"] = df["property_type"].apply(lambda x: 1 if "Private" in x else 0)

    #dropping rows with missing values
    df.dropna(inplace=True)

    #dropping columns no longer needed
    df.drop(columns=["last_scraped", "host_since", "description", "host_about",
                      "neighborhood_overview", "host_response_time", "property_type"], inplace=True)

    return None