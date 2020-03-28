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
import unicodedata as _unicodedata


def _remove_accents(input_str):
    """Source: https://stackoverflow.com/a/517974."""
    nfkd_form = _unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not _unicodedata.combining(c)])


# =============================================================================
# Cierres de ciclo
# =============================================================================
def cierres_open_dataset(filename, level=4):
    """Abre un archivo de cierres agrícolas del SIAP.

    Parameters
    ----------
    filename : str
        Ruta completa del archivo de entrada.

    Returns
    -------
    pandas.DataFrame.

    """
    df = _pd.read_csv(
        filepath_or_buffer=filename,
        encoding='latin',
        low_memory=False
        )
    df.drop(
        columns=[i for i in df.columns if i.startswith('Id')],
        inplace=True
        )
    df.dropna(
        axis=0,
        how='all',
        inplace=True
        )
    df.columns = df.columns.str.upper()

    for col in [i for i in df.columns.tolist() if i.startswith('NOM')]:
        df.loc[:, col] = df.loc[:, col].apply(_remove_accents).str.upper()

    df.loc[df['NOMESTADO'] == 'CIUDAD DE MEXICO / DF', 'NOMESTADO'] = (
        'CIUDAD DE MEXICO'
        )

    df.set_index(
        keys=(
            ['ANIO'] + [i for i in df.columns.tolist() if i.startswith('NOM')]
            ),
        inplace=True
        )
    df.dropna(
        axis=1,
        how='all',
        inplace=True
        )

    if level == 1:  # País
        df = df.groupby(level=[
            'ANIO', 'NOMCICLOPRODUCTIVO', 'NOMMODALIDAD', 'NOMUNIDAD',
            'NOMCULTIVO'
            ]).sum()

    elif level == 2:  # Estado
        df = df.groupby(level=[
            'ANIO', 'NOMESTADO', 'NOMCICLOPRODUCTIVO', 'NOMMODALIDAD',
            'NOMUNIDAD', 'NOMCULTIVO'
            ]).sum()

    elif level == 3:  # Distrito de desarrollo rural
        try:
            df = df.groupby(level=[
                'ANIO', 'NOMESTADO', 'NOMDDR', 'NOMCICLOPRODUCTIVO',
                'NOMMODALIDAD', 'NOMUNIDAD', 'NOMCULTIVO'
                ]).sum()

        except AssertionError:
            pass

    elif level == 4:  # Municipio
        pass

    return(df)


def cierres_open_mfdataset(paths, level=4):
    dfs = [cierres_open_dataset(filename, level) for filename in paths]
    # levels = set([j for j in list(i.index.names) for i in dfs])
    df = _pd.concat(
        objs=[i.reset_index() for i in dfs],
        ignore_index=True
        )
    df.set_index(
        keys=(
            ['ANIO'] + [i for i in df.columns.tolist() if i.startswith('NOM')]
            ),
        inplace=True
        )
    return(df)


def cierres_subset(
        data, estado=None, ddr=None, cicloproductivo=None, modalidad=None,
        cultivo=None, clean=False, onlynom=False,
        ):
    par = {
        'NOMESTADO': estado,
        'NOMDDR': ddr,
        'NOMCICLOPRODUCTIVO': cicloproductivo,
        'NOMMODALIDAD': modalidad,
        'NOMCULTIVO': cultivo
        }
    par = {
        key: _remove_accents(level.upper())
        for key, level in par.items()
        if level
        }
    return(data.xs(key=par.values(), level=list(par.keys())))


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
        table = table.reindex(columns=(
            'ANO CORTE CULTIVO CICLO MOD ESTADO DISTRITO SEMBRADO_HA '
            'COSECHADO_HA SINIESTRADO_HA OBTENIDO_TON'.split()))
        table.loc[:, 'DISTRITO'] = (
            table.loc[:, 'DISTRITO'].str.upper().apply(_remove_accents)
            )
        table.loc[:, 'ESTADO'].fillna(method='ffill', inplace=True)

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
        table.loc[:, 'CICLO'] = _remove_accents(metadata[0].upper())
        table.loc[:, 'ANO'] = int(metadata[1])
        table.loc[:, 'MOD'] = _remove_accents(metadata[2].upper())
        table.loc[:, 'CORTE'] = str2DatetimeIndex(date_str=metadata[3])
        table.loc[:, 'CULTIVO'] = _remove_accents(metadata[5].upper())
        output.append(table)

    output = _pd.concat(output)
    output.set_index(
        keys=['ANO', 'CORTE', 'CULTIVO', 'CICLO', 'MOD', 'ESTADO', 'DISTRITO'],
        inplace=True
        )
    return(output)


def avances_open_mfdataset(paths):
    return(_pd.concat([
        avances_open_dataset(filename) for filename in paths
        ]))


def avances_subset(
        data, estado=None, ddr=None, cicloproductivo=None, modalidad=None,
        cultivo=None):
    par = {
        'ESTADO': estado,
        'DISTRITO': ddr,
        'CICLO': cicloproductivo,
        'MOD': modalidad,
        'CULTIVO': cultivo
        }
    par = {
        key: _remove_accents(level.upper())
        for key, level in par.items()
        if level
        }
    return(data.xs(key=par.values(), level=list(par.keys())))


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
