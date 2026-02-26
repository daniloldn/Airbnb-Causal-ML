import numpy as np
import pandas as pd


def sm_treat_row(res, treat_name):
    """Return coef, se, CI for a statsmodels result object for treat_name."""
    b = float(res.params[treat_name])
    se = float(res.bse[treat_name])
    ci_low, ci_high = res.conf_int().loc[treat_name].astype(float).tolist()
    return b, se, ci_low, ci_high

def sm_extract(res, treat):
    b = float(res.params[treat])
    se = float(res.bse[treat])
    n = int(res.nobs)
    r2 = float(res.rsquared)
    return b, se, n, r2

def econml_ate_row(est, X=None):
    """Return ATE and CI for an econml estimator that supports ate/ate_interval."""
    ate = float(est.ate(X=X))
    ci_low, ci_high = est.ate_interval(X=X)
    return ate, np.nan, float(ci_low), float(ci_high)   



