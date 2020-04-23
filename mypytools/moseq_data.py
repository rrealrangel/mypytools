# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 22:13:46 2020

@author: rreal
"""
import pandas as _pd


def open_ts(filepath, percentile):
    sdi_name = filepath.stem.split('_')[2].replace('-', '_')
    series = _pd.read_csv(
        filepath_or_buffer=filepath,
        usecols=[0, 3],
        index_col=0,
        parse_dates=True,
        date_parser=(
            lambda x: _pd.to_datetime(arg=x,format='%Y%m') +
            _pd.tseries.offsets.MonthEnd(1)
            )
        )[percentile]
    series.name = sdi_name
    return(series)
