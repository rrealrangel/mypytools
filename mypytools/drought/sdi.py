# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 23:46:26 2019

@author: r.realrangel
"""

def compute_npsdi(
        data, temp_scale, index, variable, output_res, nodata=-32768,
        trim_vmap=None
        ):
    """Compute non-parametric standardized drought indices (SDI).

    References:
    Edwards, D. C., & McKee, T. B. (1997). Characteristics of 20th
        Century drought in the United States at multiple time scales.
        Atmospheric Science Paper No. 634, May 1–30, 174–174. Retrieved
        from http://oai.dtic.mil/oai/oai?verb=getRecord&metadataPrefix=
        html&identifier=ADA325595
    Hao, Z., & AghaKouchak, A. (2013). Multivariate Standardized
        Drought Index: A parametric multi-index model. Advances in
        Water Resources, 57, 12–18. https://doi.org/10.1016
        /j.advwatres.2013.03.009
    Hao, Z., & AghaKouchak, A. (2014). A Nonparametric Multivariate
        Multi-Index Drought Monitoring Framework. Journal of
        Hydrometeorology, 15(1), 89–101. https://doi.org/10.1175/JHM-D-
        12-0160.1
    McKee, T. B., Doesken, N. J., & Kleist, J. (1993). The relationship
        of drought frequency and duration to time scales. Eighth
        Conference on Applied Climatology, 179–184. American
        Meteorological Society.
    Shukla, S., & Wood, A. W. (2008). Use of a Standardized Runoff
        Index for Characterizing Hydrologic Drought. Geophysical
        Research Letters, 35(2), 1–7. https://doi.org/10.1029
        /2007GL032487

    Parameters
    ----------
    data : xarray.Dataset
        The input datasets of MERRA-2 merged into one data cube (time,
        lat, lon).
    temp_scale : int
        The temporal scale to which the input data is aggregated to
        compute the standardized drought index.
    index : str
        The name of the index to be computed. Valid options are:
            'SPI', to compute the Standardized Precipitation Index
                (McKee et al., 1993, Edwards & McKee, 1997);
            'SRI', to compute the Standardized Runoff Index (Shukla &
                 Wood, 2008);
            'SSI', to compute the Standardized Soil Moisture Index (Hao
                & AghaKouchak, 2013);
            'MSDI-PRERUN', to compute the Multivariate Standardized
                Drought Index for precipitation and runoff (Hao &
                AghaKouchak, 2013; 2014);
            'MSDI-PRESMO', to compute the Multivariate Standardized
                Drought Index for precipitation and soil moisture (Hao
                & AghaKouchak, 2013; 2014); and
            'MSDI-PRESMORUN', to compute the Multivariate Standardized
                Drought Index for precipitation and soil moisture and
                runoff (Hao & AghaKouchak, 2013; 2014).
    variable : sequence
        A list of the MERRA-2's variable(s) name(s) used to compute the
        index. Valid options are:
            [['PRECTOTLAND']], to compute the SPI;
            [['BASEFLOW', 'RUNOFF']], to compute the SRI;
            [['RZMC']], to compute the SSI;
            [['PRECTOTLAND'], ['BASEFLOW', 'RUNOFF']], to compute the
                MSDI-PRERUN;
            [['PRECTOTLAND'], ['RZMC']], to compute the MSDI-PRESMO;
                and
            [['PRECTOTLAND'], ['RZMC'], ['BASEFLOW', 'RUNOFF']], to
                compute the MSDI-PRESMORUN.
    output_res : float
        The spatial resolution used in the output SDI dataset.
    nodata : int, optional
        Value to set in empty cells. Default is -32768.
    trim_vmap : str, optional
        Full path of a shapefile that contains the vector map used to
            trim the output dataset.

    Returns
    -------
    xarray.Dataset
        Dataset of the SDI computed.
    """
    # TODO: Remove the parameter 'variable' from the arguments and
    # define the variables names from the index to compute.

    # Merge mergeable variables.
    if sum([len(i) > 1 for i in variable]) > 0:
        vars_to_merge = variable[
            [
                j
                for j in range(len(variable))
                if [len(i) > 1 for i in variable][j] is True][0]
            ]
        data = dmgr.merge_arrays(
            data=data,
            vars_to_merge=[vars_to_merge]
            )

    data_clean = dmgr.drop_array(
        data=data,
        keeplst=variable
        )

    data_scaled = dmgr.accumulate_time(
        data=data_clean,
        t_acc=temp_scale
        )

    inp_shape = list(
        np.shape(data_scaled[data_scaled.var().keys()[0]].values)
        )
    intensity_aux = np.ndarray(inp_shape, dtype='float32') * np.nan

    for month in range(1, 13):
        t_index = data_scaled.time.dt.month == month
        time_series = get_time_series(
            data=data_scaled,
            month=month
            )

        for v, var in enumerate(time_series.var().iterkeys()):
            var_data = np.expand_dims(time_series[var].values, axis=3)

            if v == 0:
                rec_arranged = var_data.copy()

            else:
                rec_arranged = np.concatenate(
                    (rec_arranged, var_data.copy()),
                    axis=3
                    )

        P = empirical_probability(rec_arranged)
        SDI = norm.ppf(P)
        SDI[np.isnan(SDI)] = 0   # To fill near sore sea cells.
        intensity_aux[t_index] = SDI
        dmgr.progress_message(
            current=month,
            total=12,
            message=(
                "- Computing the {} index for a {}-month time scale".format(
                    index.upper(), temp_scale
                    )
                ),
            units='months'
            )

    intensity = xr.DataArray(
        data=intensity_aux,
        coords={
            'time': data_scaled.time.values,
            'lat': data_scaled.lat.values,
            'lon': data_scaled.lon.values
            },
        dims=['time', 'lat', 'lon']
        )
    intensity = intensity.reindex({'time': sorted(intensity.time.values)})

    if output_res > 0:
        x_min = intensity.lon.min()
        x_max = intensity.lon.max()
        y_min = intensity.lat.min()
        y_max = intensity.lat.max()
        out_lon = np.arange(x_min, x_max + output_res, output_res)
#        out_lat = np.arange(y_min, y_max + output_res, output_res)
        out_lat = np.arange(y_min, y_max + output_res, output_res) + (output_res / 2)
        intensity_interp = intensity.interp(lat=out_lat, lon=out_lon)

    # Trim the intensity_interp dataset.
    if trim_vmap is not None:
        intensity_interp_trimmed = span.trim_data(
            data=intensity_interp,
            vmap=trim_vmap,
            res=output_res,
            nodata=nodata
            )

    # Define global attributes
    global_attrs = OrderedDict()
    global_attrs['DroughtFeature'] = 'Drought_intensity'
    global_attrs['DroughtIndex'] = index
    global_attrs['TemporalScale'] = str(temp_scale) + ' month(s)'
    global_attrs['Units'] = 'None'
    global_attrs['Description'] = 'Nonparametric Standardized Drought Index'
    intensity_interp_trimmed.attrs = global_attrs

    # Define coordinates attributes
    lat_attrs = OrderedDict()
    lat_attrs['long_name'] = "latitude"
    lat_attrs['units'] = "degrees_north"
    lat_attrs['standard_name'] = "latitude"
    intensity_interp_trimmed.lat.attrs = lat_attrs
    lon_attrs = OrderedDict()
    lon_attrs['long_name'] = "longitude"
    lon_attrs['units'] = "degrees_east"
    lon_attrs['standard_name'] = "longitude"
    intensity_interp_trimmed.lon.attrs = lon_attrs

    return(intensity_interp_trimmed)