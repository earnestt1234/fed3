#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 22:13:44 2022

@author: earnestt1234
"""

import numpy as np
import pandas as pd

def _default_metric(fed, nonbinned_func, binned_func, bins=None, origin='start',
                    agg='sum'):

    if bins is None:
        out = nonbinned_func(fed)
    else:
        vals = binned_func(fed)
        G = pd.Grouper(freq=bins, origin=origin)
        out = vals.groupby(G).agg(agg)

    return out

def filterout(series, dropna=False, dropzero=False, deduplicate=False):
    if dropna:
        series = series.dropna()
    if dropzero:
        series = series[series != 0]
    if deduplicate:
        series = series[~series.duplicated()]
    return series

def get_cumulative_pellets(fed):
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