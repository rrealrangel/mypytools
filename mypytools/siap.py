# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 17:20:26 2020

@author: rreal

Rutinas para manejar los conjuntos de datos de producción agropecuaria
del Sistema de Información Agroalimentaria y Pesquera (SIAP;
https://www.gob.mx/siap) de la Secretaría de Agricultura y Desarrollo
Rural (SADER) de México.
"""
import datetime as _dt
import pandas as _pd


# =============================================================================
# Cierres de ciclo
# =============================================================================
def cierres_open_dataset(filename):
    """Abre un archivo de cierres agrícolas del SIAP.

    Parameters
    ----------
    filename : str
        Ruta completa del archivo de entrada.

    Returns
    -------
    pandas.DataFrame.

    """
    return(_pd.read_csv(
        filepath_or_buffer=filename,
        encoding='latin',
        low_memory=False
        ))


def cierres_open_mfdataset(paths):
    return(_pd.concat([
        cierres_open_dataset(filename)
        for filename in paths
        ]))


def cierres_subset(
        data, estado=None, ddr=None, cicloproductivo=None, modalidad=None,
        cultivo=None, clean=False, onlynom=False,
        ):
    sub = data.copy()

    if estado:
        if isinstance(estado, str):
            sub = sub[sub['Nomestado'].str.lower() == estado.lower()]

        elif isinstance(estado, (int, float)):
            sub = sub[sub['Idestado'] == estado]

    if ddr:
        if isinstance(ddr, str):
            sub = sub[sub['Nomddr'].str.lower() == ddr.lower()]

        elif isinstance(ddr, (int, float)):
            sub = sub[sub['Idddr'] == ddr]

    if cicloproductivo:
        if isinstance(cicloproductivo, str):
            sub = sub[sub['Nomcicloproductivo'].str.lower() ==
                      cicloproductivo.lower()]

        elif isinstance(cicloproductivo, (int, float)):
            sub = sub[sub['Idciclo'] == cicloproductivo]

    if modalidad:
        if isinstance(modalidad, str):
            sub = sub[sub['Nommodalidad'].str.lower() == modalidad.lower()]

        elif isinstance(modalidad, (int, float)):
            sub = sub[sub['Idmodalidad'] == modalidad]

    if cultivo:
        if isinstance(cultivo, str):
            sub = sub[sub['Nomcultivo'].str.lower() == cultivo.lower()]

        elif isinstance(cultivo, (int, float)):
            sub = sub[sub['Idcultivo'] == cultivo]

    if clean:
        sub.drop(
            labels=sub.columns[(sub.nunique() == 1).values],
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


# =============================================================================
# Avances mensuales (2006-presente)
# =============================================================================
def avances_open_dataset(filename):
    def str2DatetimeIndex(date_str):
        keys = (
            'ENERO FEBRERO MARZO ABRIL MAYO JUNIO JULIO AGOSTO SEPTIEMBRE '
            'OCTUBRE NOVIEMBRE DICIEMBRE'.split()
            )
        vals = [i for i in list(range(1, 13))]
        month_str2int = {k: v for k, v in zip(keys, vals)}
        date_str = date_str.split()
        return(_dt.date(
            int(date_str[6]),
            month_str2int[date_str[4]],
            int(date_str[2])
            ))

    output = []
    tables = [
        df.copy()
        for df in _pd.read_html(io=str(filename))
        if df.shape[1] == 7
        ]

    with open(file=str(filename), mode='r') as html_file:
        html_script = html_file.read().splitlines()

    table_metadata = [
        i
        for i in html_script
        if "textoTablaTitulo" in i
        ]

    for t, table in enumerate(tables):
        # Parse the data.
        table = table[[
            'TOTAL' not in i.split()
            for i in table['Distrito']['Distrito']
            ]]
        table.columns = (
            'ESTADO DISTRITO SEMBRADO_HA COSECHADO_HA SINIESTRADO_HA '
            'OBTENIDO_TON RBC_TON/HA'.split()
            )
        table['ESTADO'] = table['ESTADO'].fillna(method='ffill')

        # Parse the metadata.
        titles = [
            i for i in table_metadata[t].split("textoTabla")
            if "titulo" in i.lower()
            ][-2:]
        metadata = [
            i for i in [
                i.split(">")[-1].strip()
                for i in titles[0].split("<") + titles[1].split("<")
                ]
            if i
            ]
        table['CICLO'] = metadata[0]
        table['ANO'] = int(metadata[1])
        table['MOD'] = metadata[2]
        table['CORTE'] = str2DatetimeIndex(date_str=metadata[3])
        table['CULTIVO'] = metadata[5]
        output.append(
            table.loc[
                :,
                'ANO CORTE ESTADO DISTRITO CULTIVO CICLO MOD SEMBRADO_HA '
                'COSECHADO_HA SINIESTRADO_HA OBTENIDO_TON'.split()
                ]
            )

    output = _pd.concat(output)
    output.set_index(
        keys='CORTE',
        inplace=True
        )

    return(output)


def avances_open_mfdataset(paths):
    return(_pd.concat([
        avances_open_dataset(filename) for filename in paths
        ]))


def avances_subset(
        data, estado=None, ddr=None, cicloproductivo=None, modalidad=None,
        cultivo=None, clean=False):
    sub = data.copy()

    if estado:
        sub = sub[sub['ESTADO'].str.lower() == estado.lower()]

    if ddr:
        sub = sub[sub['DISTRITO'].str.lower() == ddr.lower()]

    if cicloproductivo:
        sub = sub[sub['CICLO'].str.lower() == cicloproductivo.lower()]

    if modalidad:
        sub = sub[sub['MOD'].str.lower() == modalidad.lower()]

    if cultivo:
        sub = sub[sub['CULTIVO'].str.lower() == cultivo.lower()]

    if clean:
        sub.drop(
            labels=sub.columns[(sub.nunique() == 1).values],
            axis=1,
            inplace=True
            )

    return(sub)


def avances_fillna(data):
    data_filled = data.copy()
    data_filled[data_filled.isna()] = 0
    data_filled = data_filled.reindex(
        index=_pd.date_range(
            start=data_filled.index[0],
            end=data_filled.index[-1],
            freq='M'
            )
        )
    data_filled.loc[
        (data_filled['ANO'].isna()) & (data_filled.index.month >= 4), 'ANO'
        ] = data_filled.loc[
            (data_filled['ANO'].isna()) & (data_filled.index.month >= 4)
            ].index.year.values
    data_filled.loc[
        (data_filled['ANO'].isna()) & (data_filled.index.month <= 3), 'ANO'
        ] = data_filled.loc[
            (data_filled['ANO'].isna()) & (data_filled.index.month <= 3)
            ].index.year.values - 1
    data_filled = data_filled.groupby(by='ANO').apply(
        lambda group: group.interpolate()
        )
    return(data_filled)


def avances_monthly_weight(data):
    mean_progress = data.groupby(level='ANO').apply(
        lambda table: table / table.iloc[-1]
        ).groupby(by=data.index.get_level_values('CORTE').month).mean()
    mean_progress.clip(lower=0, upper=1, inplace=True)
    exposure = mean_progress['SEMBRADO_HA'] - mean_progress['COSECHADO_HA']
    return(exposure / exposure.sum())
