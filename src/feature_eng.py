import pandas as pd
import numpy as np
from src.load_data import load_processed
from pathlib import Path
from sklearn.cluster import KMeans
from pyproj import Transformer
from sklearn.neighbors import BallTree


def feature_eng() -> pd.DataFrame:

    df = load_processed()


    #host features
    df["experience"] = df["last_scraped"].dt.year - df["host_since"].dt.year
    df["desc_dummy"] = df["description"].apply(lambda x: 0 if pd.isnull(x) else 1)
    df["about_dummy"] = df["host_about"].apply(lambda x: 0 if pd.isnull(x) else 1)
    df["overveiw_dummy"] = df["neighborhood_overview"].apply(lambda x: 0 if pd.isnull(x) else 1)
    df["host_response_time"] = pd.Categorical(
    df["host_response_time"],
    categories=["within an hour", "within a few hours", "within a day", "a few days or more"],
    ordered=True)

  
    #log price
    df["log_price"] = np.log(df["price"])


    #converting categorical variables
    df["host_is_superhost"] = df["host_is_superhost"].map({"t": 1, "f": 0}).astype("int8")
    df["host_identity_verified"] = df["host_identity_verified"].map({"t": 1, "f": 0}).astype("int8")
    df["host_has_profile_pic"] = df["host_has_profile_pic"].map({"t": 1, "f": 0}).astype("int8")
    
    
    #property dummies
    df["shared"] = df["property_type"].apply(lambda x: 1 if "Shared" in x else 0)
    df["entire"] = df["property_type"].apply(lambda x: 1 if "Entire" in x else 0)
    df["private"] = df["property_type"].apply(lambda x: 1 if "Private" in x else 0)

    #borough FE
    dummies = pd.get_dummies(df["neighbourhood_cleansed"], prefix="borough", drop_first=True)
    df = pd.concat([df, dummies], axis=1)
 
    #fixed effects
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:27700", always_xy=True)
    x, y = transformer.transform(df["longitude"].values,
                             df["latitude"].values)
    df["x"] = x
    df["y"] = y
    K = 100  
    kmeans = KMeans(n_clusters=K, random_state=42, n_init=10)
    df["loc_fe"] = kmeans.fit_predict(df[["x", "y"]])

    #treatment variable
    coords = df[["x", "y"]].values
    tree = BallTree(coords, metric="euclidean")
    radius = 500
    # query neighbors within radius
    indices = tree.query_radius(coords, r=radius)
    df["rivals_500m"] = [len(i) - 1 for i in indices]
    #log treatment
    df["log_rivals_500m"] = np.log1p(df["rivals_500m"])
    
    #dropping columns no longer needed
    df.drop(columns=["last_scraped", "host_since", "description", "host_about",
                      "neighborhood_overview", "host_response_time", "property_type", 
                      "price", "latitude", "longitude", "neighbourhood_cleansed",
                      "x", "y", "rivals_500m"
                      ], inplace=True)
    
    #dropping rows with missing values
    df.dropna(inplace=True)
    
    #saving the data
    Path("../data/feature").mkdir(parents=True, exist_ok=True)
    df.to_csv("../data/feature/listings_features.csv", index=False)

    return None