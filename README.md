# Airbnb-Causal-ML

Graduate-level project comparing traditional parametric estimators with modern causal machine learning for measuring how local competition affects Airbnb listing prices in London (Q4 2025 data).

The repository is structured as a lightweight Python package (`src/`) plus reproducible notebooks (`notebooks/`) and declarative data folders (`data/`). Running the full pipeline takes raw Inside Airbnb listings, cleans and engineers features, and re-estimates treatment effects with OLS, Post-Double Selection (PDS), Linear Double Machine Learning (DML), and Causal Forest DML.

---

## Repository layout

- `data/raw/` Untracked source CSV (`listings.csv`, ~150 MB). Obtain from [Inside Airbnb](http://insideairbnb.com/get-the-data/) → London → 2025-10 snapshot.
- `data/processed/` Outputs from cleaning (e.g., `processed_listings.csv`).
- `data/feature/` Final modeling matrix (`listings_features.csv`).
- `notebooks/eda.ipynb` Exploratory plots, column pruning, intuition building.
- `notebooks/model.ipynb` Implements OLS, cluster-robust OLS, PDS, Linear DML, and Causal Forest DML pipelines.
- `src/clean_data.py` Column filtering and type casting for raw listings.
- `src/feature_eng.py` Feature creation: borough fixed effects, spatial K-means, competition metrics, amenities, log-scaling, etc.
- `src/orchestrator.py` Minimal CLI that sequences cleaning then feature engineering.
- `pyproject.toml` Core python dependencies when installing as a package.

---

## Data requirements

1. Download the Inside Airbnb London listings CSV matching the course assignment (2025-10 or consistent snapshot).
2. Place it at `data/raw/listings.csv` without renaming columns.
3. The cleaning script removes sensitive columns and expects the standard schema (≈95 columns). If a newer snapshot adds/removes columns, update the `drop_cols` list inside [src/clean_data.py](src/clean_data.py).

---

## Environment setup

The project targets Python ≥ 3.10. At minimum you need: `numpy`, `pandas`, `scikit-learn`, `pyproj`, `statsmodels`, `scipy`, `plotly`, `econml`, `jupyter`, and `papermill` (for headless notebook execution).

### Option A – Conda (recommended for `econml`)

```powershell
conda create -n airbnb-causal-ml python=3.11 -y
conda activate airbnb-causal-ml
pip install -e .
pip install statsmodels plotly scipy econml jupyter papermill
```

### Option B – uv / pip

```bash
uv venv
uv pip install -e .
uv pip install statsmodels plotly scipy econml jupyter papermill
```

> 📝 `pip install -e .` reads `pyproject.toml` and installs the `src/` package so the notebooks can `import src.load_data` without editing `PYTHONPATH`.

---

## Reproducing the full pipeline

1. **Clone and install** using one of the environment options above.
2. **Place the raw CSV** at `data/raw/listings.csv`.
3. **Generate processed + feature data.** Either run the individual modules or trigger both via the orchestrator:
	```bash
	python -m src.orchestrator
	```
	- [src/clean_data.py](src/clean_data.py) drops unused columns, converts dates, normalizes prices, and saves `data/processed/processed_listings.csv`.
	- [src/feature_eng.py](src/feature_eng.py) adds host/amenity dummies, borough FE, spatial K-means clusters (K=100) with projected coordinates, local rival counts via a BallTree (500m radius), centered treatments, and amenities expansions. It outputs `data/feature/listings_features.csv`.
4. **Run exploratory analysis (optional but encouraged).**
	```bash
	jupyter lab notebooks/eda.ipynb
	```
	Validate that distributions (log price, competition) match lecture expectations.
5. **Estimate causal effects.** Execute the modeling notebook interactively or headlessly:
	```bash
	jupyter nbconvert --execute notebooks/model.ipynb --to notebook --output outputs/model-run.ipynb
	```
	This notebook:
	- Builds treatment (`log_rivals_500m`) and outcome (`log_price`).
	- Fits OLS with and without spatial fixed effects (`loc_fe`).
	- Performs Post-Double Selection per Belloni et al. using `ElasticNetCV` selectors.
	- Trains `LinearDML` and `CausalForestDML` with Random Forest nuisance models (5-fold cross-fitting, seeded for reproducibility).
	- Summarizes results into a comparison table using helpers in [src/results.py](src/results.py).
6. **Review outputs.** Expect to see:
	- Cluster-robust OLS tables showing a negative treatment coefficient.
	- DML and Causal Forest ATE estimates with 95% confidence intervals.
	- Optional treatment heterogeneity histogram for CATEs.

---

## Automation tips

- **Headless grading run:**
  ```bash
  python -m src.orchestrator && \
  papermill notebooks/model.ipynb outputs/model-graded.ipynb
  ```
- **Re-seeding:** Randomness is controlled via `random_state` in KMeans (42), DML (0), and Causal Forest (42). Modify these constants inside [src/feature_eng.py](src/feature_eng.py) and `notebooks/model.ipynb` if you need alternative draws.
- **Adding new controls:** Append engineered features to the dataframe before the drop/scale section of [src/feature_eng.py](src/feature_eng.py) so that downstream notebooks pick them up automatically.

---

## Troubleshooting

- `ModuleNotFoundError: src.load_data` → ensure you ran `pip install -e .` inside the active environment.
- `pyproj` / PROJ errors → run `conda install pyproj` (Windows) or ensure PROJ data files are accessible.
- `econml` build failures → prefer Conda-forge wheels (`conda install -c conda-forge econml`) or install Visual C++ Build Tools on Windows.
- Notebook memory errors → filter listings (e.g., subset boroughs) before running feature engineering, or increase RAM (>16 GB recommended).

---

## What to submit

For the course assignment, export:

1. `outputs/model-run.ipynb` (or HTML) showing the executed modeling pipeline.
2. A short write-up interpreting OLS vs DML/Causal Forest estimates (connect with competition theory).
3. Any additional plots created during EDA.

This README documents all steps necessary for graders to reproduce your numbers from scratch.
