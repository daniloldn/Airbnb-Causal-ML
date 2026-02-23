import pandas as pd
import numpy as np
from src.load_data import load_processed
from pathlib import Path


def feature_eng() -> pd.DataFrame:

    df = load_processed()

    return None