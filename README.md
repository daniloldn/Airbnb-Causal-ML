# Airbnb-Causal-ML

This repo shows how nearby competition affects Airbnb prices in London. We:
- clean the public Inside Airbnb dataset,
- add intuitive features (amenities, spatial clusters, rival counts),
- compare standard econometrics (OLS, Post-Double Selection) with causal ML (Double Machine Learning, Causal Forest).

The goal of this README is to let anyone reproduce the assignment without guessing hidden steps.

---

## 1. What you need

1. **Raw data:** Download the latest London CSV from [Inside Airbnb](http://insideairbnb.com/get-the-data/) and place it at `data/raw/listings.csv`.
2. **Python tools:** Install Anaconda or Miniconda (recommended). Everything else comes from the provided environment file.
3. **Git:** Clone this repo so you have the same folder layout.

---

## 2. Set up the environment (5 minutes)

```powershell
conda env create -f environment.yml
conda activate airbnb-causal-ml
pip install -e .
```

Why both Conda and pip?
- Conda installs heavy packages such as `numpy`, `scikit-learn`, `pyproj`, `statsmodels`, `plotly`, `jupyter`, and `econml` (through the pip section).
- `pip install -e .` registers the `src/` folder as a package so notebooks can run `from src.load_data import load_feature` without hacks.

If Conda is not an option, create a Python 3.11 virtual environment and install the packages listed in [environment.yml](environment.yml) manually.

---

## 3. Know the folders

| Folder | Why it matters |
| ------ | -------------- |
| `data/raw/` | Put the downloaded `listings.csv` here (git ignores this). |
| `data/processed/` | Appears after cleaning; contains `processed_listings.csv`. |
| `data/feature/` | Holds `listings_features.csv`, the modeling-ready table. |
| `notebooks/eda.ipynb` | Quick exploratory analysis, column sanity checks. |
| `notebooks/model.ipynb` | All estimation steps (OLS, PDS, DML, Causal Forest). |
| `src/clean_data.py` | Drops unused columns, parses dates, fixes prices. |
| `src/feature_eng.py` | Creates engineered variables and saves the feature set. |
| `src/orchestrator.py` | Runs cleaning + feature engineering with one command. |

---

## 4. Reproduce the pipeline

1. **Download data** → `data/raw/listings.csv`.
2. **Activate env** → `conda activate airbnb-causal-ml`.
3. **Build processed datasets**
   ```powershell
   python -m src.orchestrator
   ```
   - Step 1 (`clean_data`) keeps relevant variables, standardizes formats, and writes `data/processed/processed_listings.csv`.
   - Step 2 (`feature_eng`) adds:
     - host experience dummies,
     - borough fixed effects and 100 spatial K-means clusters (built after projecting lat/long to meters),
     - rival counts within 500 meters using a `BallTree`,
     - amenities flags for the 30 most common amenities,
     - log/centered versions of key variables.
     - Output: `data/feature/listings_features.csv`.
4. **Run notebooks**
   - EDA (optional but encouraged): `jupyter lab notebooks/eda.ipynb`.
   - Modeling (required):
     ```powershell
     jupyter nbconvert --execute notebooks/model.ipynb --to notebook --output outputs/model-run.ipynb
     ```
     or open the notebook and click “Run All”.
5. **Interpret results**
   - Compare OLS vs OLS + spatial FE vs Post-Double Selection.
   - Review the Linear DML and Causal Forest ATEs and their confidence intervals.
   - Inspect treatment heterogeneity plots in the notebook.

Following these five steps recreates every table and figure that appears in the original assignment submission.

---

## 5. Troubleshooting tips

- **`ModuleNotFoundError: src.load_data`** → rerun `pip install -e .` inside the active environment.
- **`pyproj` errors** → ensure the Conda env is active; on Windows, run `conda install pyproj` if needed.
- **`econml` installation fails** → the Conda environment already pulls compatible builds; if you still have trouble, install Visual C++ Build Tools and retry.
- **Long runtimes / memory issues** → subset the dataset (e.g., filter to a few boroughs) before running `feature_eng`.

---

## 6. What to hand in

1. Executed modeling notebook (`outputs/model-run.ipynb` or its HTML export).
2. Short explanation of the treatment effect estimates (compare OLS vs DML/Causal Forest and relate to competition theory).
3. Optional EDA visuals to motivate your modeling choices.

That’s it. Stick to the “Reproduce the pipeline” checklist and you will match the original results.
