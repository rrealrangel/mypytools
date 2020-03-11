# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 10:03:45 2020

@author: rreal
"""
from pathlib import Path
import pandas as pd


def read_database(path):
    inp_list = sorted(list(Path(path).glob(pattern='**/*.csv')))
    data_listed = [
        pd.read_csv(filepath_or_buffer=i, encoding='latin') for i in inp_list
        ]
    return(pd.concat(data_listed))


def subset(
        data, estado=None, ddr=None, cicloproductivo=None, modalidad=None,
        cultivo=None, clean=False, onlynom=False,
        ):
    sub = data.copy()

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
        sub.drop(
            labels=[f for f in sub.columns if sub[f].nunique() == 1],
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