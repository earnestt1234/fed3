#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 18:27:07 2021

@author: earnestt1234
"""

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

def _filterout(series, dropna=False, dropzero=False, deduplicate=False):

    if dropna:
        series = series.dropna()
    if dropzero:
        series = series[series != 0]
    if deduplicate:
        series = series[~series.duplicated()]

    return series

def binary_pellets(fed, bins=None, origin='start'):

    def _get_binary_pellets(fed):
        y = fed.binary_pellets()
        y = _filterout(y, dropzero=True)
        return y

    return _default_metric(fed,
                           nonbinned_func=_get_binary_pellets,
                           binned_func=_get_binary_pellets,
                           bins=bins,
                           origin=origin,
                           agg='sum')

def cumulative_pellets(fed, bins=None, origin='start'):

    def _get_cumulative_pellets(fed):
        y = fed['Pellet_Count']
        y = _filterout(y, deduplicate=True)
        return y

    return _default_metric(fed,
                           nonbinned_func=_get_cumulative_pellets,
                           binned_func=_get_cumulative_pellets,
                           bins=bins,
                           origin=origin,
                           agg='mean')

def pellets(fed, bins=None, origin='start'):

    func = cumulative_pellets if bins is None else binary_pellets

    return func(fed, bins=bins, origin=origin)

def ipi(fed, bins=None, origin='start'):

    def _get_ipi(fed):
        y = fed.ipi()
        y = _filterout(y, dropna=True)
        return y

    return _default_metric(fed,
                           nonbinned_func=_get_ipi,
                           binned_func=_get_ipi,
                           bins=bins,
                           origin=origin,
                           agg='mean')


# ---- module variables

# link keywords to their default function
METRICS = {'pellets': pellets,
           'bpellets': binary_pellets,
           'cpellets': cumulative_pellets,
           'ipi': ipi}

# # link keywords to names
METRICNAMES = {'pellets': 'Pellets',
                'bpellets': 'Pellets',
                'cpellets': 'Pellets',
                'ipi': 'Interpellet Intervals'}

def _get_metric(y, kind=None):

    key = y.lower()
    try:
        return METRICS[key]
    except KeyError:
        raise ValueError(f'y-value "{y}" is not recognized.')

def _get_metricname(y):

    key = y.lower()
    try:
        return METRICNAMES[key]
    except KeyError:
        raise ValueError(f'y-value "{y}" is not recognized.')
