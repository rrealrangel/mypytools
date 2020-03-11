# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 14:30:22 2020

@author: rreal
"""
from sklearn.metrics import mean_squared_error as _mse
from sklearn.model_selection import KFold as _KFold
from statsmodels.nonparametric.smoothers_lowess import _lowess
import numpy as _np


def optimal_lowess(x, y, tries=10, xval_folds=3):
    xmid = x[1:-1]
    ymid = y[1:-1]
    kf = _KFold(
        n_splits=xval_folds,
        shuffle=True,
        random_state=1
        )
    f_tries = _np.linspace(
        start=0,
        stop=1,
        num=tries
        )[1:]
    crossval = {}

    for f in f_tries:
        rmse = []

        for trn_fold, tst_fold in kf.split(ymid):
            x_trn = _np.concatenate([[x[0]], xmid[trn_fold], [x[-1]]])
            y_trn = _np.concatenate([[y[0]], ymid[trn_fold], [y[-1]]])
            x_tst = xmid[tst_fold]
            y_tst = ymid[tst_fold]
            k_model = _lowess(endog=y_trn, exog=x_trn, frac=f)
            y_trn_model = k_model[:, 1]
            y_tst_model = _np.interp(
                x=x_tst,
                xp=x_trn,
                fp=y_trn_model,
                left=_np.nan,
                right=_np.nan
                )
            rmse.append(_np.sqrt(_mse(y_true=y_tst, y_pred=y_tst_model)))

        crossval[f] = _np.mean(rmse)

    optimal_f = min(crossval.keys(), key=(lambda k: crossval[k]))
    return(_lowess(endog=y, exog=x, frac=optimal_f))
