import pandas as pd
import numpy as np


def clean_data(df: pd.DataFrame) -> pd.DataFrame:

    drop_cols = ["listing_url", "scrape_id", "last_scraped", "name",
              "neighborhood_overview","description","source","picture_url", "host_url", "host_id",
                "host_thumbnail_url", "host_picture_url", "estimated_occupancy_l365d", "estimated_revenue_l365d",
                 "host_about", "host_location" ,"host_name", "neighbourhood_cleansed", "neighbourhood",
                  "availability_30", "availability_60", "availability_90", "availability_365", "availability_eoy",
                   "minimum_minimum_nights", "maximum_minimum_nights", "minimum_maximum_nights", "maximum_maximum_nights",
                   "minimum_nights_avg_ntm", "maximum_nights_avg_ntm", "calendar_updated", "calendar_last_scraped",
                   "has_availability","host_neighbourhood", "bathrooms_text",
                   "number_of_reviews_ltm", "number_of_reviews_l30d", "number_of_reviews_ly","reviews_per_month",
                   "license"]
    
    df.drop(columns=drop_cols, inplace=True)
    return df