# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 14:30:22 2020

@author: rreal
"""
from sklearn.metrics import mean_squared_error as _mse
from sklearn.model_selection import KFold as _KFold
from statsmodels.nonparametric.smoothers_lowess import _lowess
import numpy as _np


def optimal_lowess(x, y, fracs=11, xval_folds=3, random_seeds=range(3)):
    """
    """
    xmid = x[1:-1]
    ymid = y[1:-1]
    f_tries = _np.linspace(
        start=0,
        stop=1,
        num=fracs
        )[1:]
    crossval = {}
    best_seed_f = []

    for seed in random_seeds:
        kf = _KFold(
            n_splits=xval_folds,
            shuffle=True,
            random_state=seed
            )

        for f in f_tries:
            rmse = []

            for trn_fold, tst_fold in kf.split(ymid):
                x_trn = _np.concatenate([[x[0]], xmid[trn_fold], [x[-1]]])
                y_trn = _np.concatenate([[y[0]], ymid[trn_fold], [y[-1]]])
                x_tst = xmid[tst_fold]
                y_tst = ymid[tst_fold]
                y_trn_model = _lowess(endog=y_trn, exog=x_trn, frac=f)[:, 1]
                y_tst_model = _np.interp(
                    x=x_tst,
                    xp=x_trn,
                    fp=y_trn_model,
                    left=_np.nan,
                    right=_np.nan
                    )
                rmse.append(_np.sqrt(_mse(y_true=y_tst, y_pred=y_tst_model)))

            crossval[f] = _np.mean(rmse)

        best_seed_f.append(
            min(crossval.keys(), key=(lambda k: crossval[k]))
            )

    optimal_f = _np.mean(best_seed_f)
    return(_lowess(endog=y, exog=x, frac=optimal_f))


def power_law(x, alpha, beta):
    """
    """
    return alpha * (x**beta)


def logistic(x, k, x0):
    """
    Logistic function

    Source: wikipedia.org (https://bit.ly/2Wuxn34).

    Parameters:
        k : float
            Logistic growth rate or steepness of the curve.
        x0 : float
            x-value of the sigmoid's midpoint.
    """
    return(1 / (1 + _np.exp(-k * (x - x0))))