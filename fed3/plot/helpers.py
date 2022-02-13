#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 12:34:52 2022

@author: earnestt1234
"""

import pandas as pd

from fed3.metrics import METRICS, METRICNAMES

def _create_metric_df(feds, metric):
    df = pd.DataFrame()
    for fed in feds:
        y = metric(fed)
        y.name = fed.name
        df = df.join(y, how='outer')

    return df

def _create_group_metric_df(feds, metric, agg='sum', var='std', freq='1H',
                            origin='start'):
    all_agg = pd.DataFrame()
    all_var = pd.DataFrame()
    G = pd.Grouper(freq=freq, origin=origin)
    for group, fedlist in feds.items():
        fed_values = pd.DataFrame()
        for fed in fedlist:
            y = metric(fed)
            y.name = fed.name
            values = y.groupby(G).agg(agg)
            fed_values = fed_values.join(values, how='outer')
        group_agg = fed_values.apply(agg, axis=1)
        group_var = fed_values.apply(var, axis=1)
        group_agg.name = group
        group_var.name = group
        all_agg = all_agg.join(group_agg, how='outer')
        all_var = all_var.join(group_var, how='outer')

    return all_agg, all_var

def _get_metric(y, kind=None):
    if isinstance(y, str):

        key = y.lower()
        try:
            return METRICS[key]
        except KeyError:
            raise ValueError(f'y-value "{y}" is not recognized.')

    else:
        return y

def _get_metricname(y):

    if isinstance(y, str):

        key = y.lower()
        try:
            return METRICNAMES[key]
        except KeyError:
            raise ValueError(f'y-value "{y}" is not recognized.')

    else:
        return y.__name__

def _get_return_value(FIG, DATA, output):

    if output == 'plot':
        return FIG

    elif output in ['dataonly', 'data']:
        return DATA

    elif output == 'both':
        return FIG, DATA

    else:
        raise ValueError(f'output value "{output}" not recognized.')

def _handle_feds(feds):
    if isinstance(feds, pd.DataFrame):
        feds = [feds]
    return feds