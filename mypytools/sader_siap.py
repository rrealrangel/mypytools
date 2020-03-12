# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 10:03:45 2020

@author: rreal
"""
import pandas as _pd


class SiapDatabase():
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
            sub = sub[(sub['Nomestado'] == estado)]

        if ddr:
            sub = sub[(sub['Nomddr'] == ddr)]

        if cicloproductivo:
            sub = sub[(sub['Nomcicloproductivo'] == cicloproductivo)]

        if modalidad:
            sub = sub[(sub['Nommodalidad'] == modalidad)]

        if cultivo:
            sub = sub[(sub['Nomcultivo'] == cultivo)]

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
