# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 14:59:20 2020

@author: rreal
"""
import pandas as _pd


class SDISeries():
    def __init__(self, filepath, percentile):
        self._filepath = filepath
        self.Series = _pd.read_csv(
            filepath_or_buffer=self._filepath,
            usecols=[0, 3],
            index_col=0,
            parse_dates=True,
            date_parser=lambda x: _pd.to_datetime(
                arg=x,
                format='%Y%m'
                ) + _pd.tseries.offsets.MonthEnd(1)
            )[percentile]

    def get_monthly_ts(self, month):
        return(self.Series[self.Series.index.month == month])
