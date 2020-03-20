# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 22:13:46 2020

@author: rreal
"""
import pandas as _pd


class IiSdi():
    """
    """
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


class SiapAgProd():
    """
    filepaths puede ser hecho con
    inp_list = sorted(list(_Path(dir_padre).glob(pattern='**/*.extension')))
    """
    def __init__(self, filepaths):
        self._filepaths = filepaths
        self.DataFrame = _pd.concat([
            _pd.read_csv(
                filepath_or_buffer=i,
                encoding='latin'
                ) for i in self._filepaths
            ])

    def subset(
            self, estado=None, ddr=None, cicloproductivo=None,
            modalidad=None, cultivo=None, clean=False, onlynom=False,
            ):
        sub = self.DataFrame.copy()

        if estado:
            if isinstance(estado, str):
                sub = sub[(sub['Nomestado'] == estado)]

            elif isinstance(estado, (int, float)):
                sub = sub[(sub['Idestado'] == estado)]

        if ddr:
            if isinstance(ddr, str):
                sub = sub[(sub['Nomddr'] == ddr)]

            elif isinstance(ddr, (int, float)):
                sub = sub[(sub['Idddr'] == ddr)]

        if cicloproductivo:
            if isinstance(cicloproductivo, str):
                sub = sub[(sub['Nomcicloproductivo'] == cicloproductivo)]

            elif isinstance(cicloproductivo, (int, float)):
                sub = sub[(sub['Idciclo'] == cicloproductivo)]

        if modalidad:
            if isinstance(modalidad, str):
                sub = sub[(sub['Nommodalidad'] == modalidad)]

            elif isinstance(modalidad, (int, float)):
                sub = sub[(sub['Idmodalidad'] == modalidad)]

        if cultivo:
            if isinstance(cultivo, str):
                sub = sub[(sub['Nomcultivo'] == cultivo)]

            elif isinstance(cultivo, (int, float)):
                sub = sub[(sub['Idcultivo'] == cultivo)]

        if clean:
            labels = [
                f for f in sub.columns
                if sub[f].nunique() == 1
                ] + ['Unnamed: 18']
            sub.drop(
                labels=labels,
                axis=1,
                inplace=True
                )

        if onlynom:
            sub.drop(
                labels=[f for f in sub.columns if f.startswith('Id')],
                axis=1,
                inplace=True
                )

        return(sub)
