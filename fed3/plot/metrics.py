#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 18:27:07 2021

@author: earnestt1234
"""

import pandas as pd
import numpy as np

# helper function
def filterout(series, dropna=False, dropzero=False, deduplicate=False):
    if dropna:
        series = series.dropna()
    if dropzero:
        series = series[series != 0]
    if deduplicate:
        series = series[~series.duplicated()]
    return series

# metric functions
def get_pellets(fed):
    y = fed['Pellet_Count']
    y = filterout(y, deduplicate=True)
    return y

def get_binary_pellets(fed):
    y = fed.binary_pellets()
    y = filterout(y, dropzero=True)
    return y

def get_ipi(fed):
    y = fed.ipi()
    y = filterout(y, dropna=True)
    return y

def get_log_ipi(fed):
    y = fed.ipi()
    y = filterout(y, dropna=True)
    return np.log10(y)

METRICS = {'pellets': get_pellets,
           'bpellets': get_binary_pellets,
           'cpellets': get_pellets,
           'ipi': get_ipi}

METRICNAMES = {'pellets': 'Pellets',
               'bpellets': 'Pellets',
               'cpellets': 'Pellets',
               'ipi': 'Interpellet Intervals'}

def _create_metric_df(feds, metric):
    df = pd.DataFrame()
    for fed in feds:
        y = metric(fed)
        y.name = fed.name
        df = df.join(y, how='outer')

    return df

def _get_metric(y):
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
