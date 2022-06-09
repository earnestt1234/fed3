#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 18:27:07 2021

@author: earnestt1234
"""

from collections import namedtuple
import warnings

import pandas as pd

# ---- General helpers

def _default_metric(fed, func, bins=None, origin='start',
                    agg='sum'):

    if bins is None:
        out = func(fed)
    else:
        vals = func(fed)
        G = pd.Grouper(freq=bins, origin=origin)
        out = vals.groupby(G).agg(agg)

    return out

def _get_metric(y, kind=None):

    key = y.lower()
    try:
        return METRICS[key]
    except KeyError:
        metrics = str(list(METRICS.keys()))[1:-1]
        raise ValueError(f'Metric key "{y}" is not recognized. Possible metrics are: '
                         f'{metrics}.')

def _filterout(series, dropna=False, dropzero=False, deduplicate=False):

    if dropna:
        series = series.dropna()
    if dropzero:
        series = series[series != 0]
    if deduplicate:
        series = series[~series.duplicated()]

    return series

# ---- Helpers for computing metrics

def _cumulative_poke_percentage_side(fed, side):

    l = cumulative_left_pokes(fed)
    r = cumulative_right_pokes(fed)
    idx = l.index.union(r.index)

    try:
        l = l.reindex(idx)
        r = r.reindex(idx)
    except ValueError:
        warnings.warn("Unable to reindex left and right pokes, likely "
                      "due to duplicate index.  Using pandas `duplicated()` "
                      "to remove duplicate indices.",
                      RuntimeWarning)

        l = l.loc[~ l.index.duplicated()]
        r = r.loc[~ r.index.duplicated()]
        l = l.reindex(idx)
        r = r.reindex(idx)

    l = l.ffill().fillna(0)
    r = r.ffill().fillna(0)
    total = l + r
    opts = {'left': (l / total) * 100, 'right': (r / total) * 100}

    return opts[side]

# ---- Pellets

def binary_pellets(fed, bins=None, origin='start'):
    func = lambda f: f.pellets(cumulative=False, condense=True)
    agg = 'sum'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

def cumulative_pellets(fed, bins=None, origin='start'):
    func = lambda f: f.pellets(cumulative=True, condense=True)
    agg = 'max'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

def pellets(fed, bins=None, origin='start'):
    func = cumulative_pellets if bins is None else binary_pellets
    return func(fed, bins=bins, origin=origin)

# ---- Any sided pokes

# ---- L/R pokes

def binary_left_pokes(fed, bins=None, origin='start'):
    func = lambda f: f.pokes(kind='left', cumulative=False, condense=True)
    agg = 'sum'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

def binary_right_pokes(fed, bins=None, origin='start'):
    func = lambda f: f.pokes(kind='right', cumulative=False, condense=True)
    agg = 'sum'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

def cumulative_left_pokes(fed, bins=None, origin='start'):
    func = lambda f: f.pokes(kind='left', cumulative=True, condense=True)
    agg = 'max'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

def cumulative_right_pokes(fed, bins=None, origin='start'):
    func = lambda f: f.pokes(kind='right', cumulative=True, condense=True)
    agg = 'max'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

def cumulative_left_percentage(fed, bins=None, origin='start'):
    func = lambda f: _cumulative_poke_percentage_side(f, 'left')
    agg = 'last'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

def cumulative_right_percentage(fed, bins=None, origin='start'):
    func = lambda f: _cumulative_poke_percentage_side(f, 'right')
    agg = 'last'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

def left_pokes(fed, bins=None, origin='start'):
    func = cumulative_left_pokes if bins is None else binary_left_pokes
    return func(fed, bins=bins, origin=origin)

def right_pokes(fed, bins=None, origin='start'):
    func = cumulative_right_pokes if bins is None else binary_right_pokes
    return func(fed, bins=bins, origin=origin)

# ---- Other

def battery(fed, bins=None, origin='start'):
    func = lambda f: f['Battery_Voltage']
    agg = 'mean'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

def ipi(fed, bins=None, origin='start'):
    func = lambda f: f.ipi(condense=True)
    agg = 'mean'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

def motor_turns(fed, bins=None, origin='start'):
    def func(fed):
        pellets = fed.binary_pellets().astype(bool)
        y = fed.loc[pellets, 'Motor_Turns']
        return y
    agg = 'mean'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

def retrival_time(fed, bins=None, origin='start'):
    def func(fed):
        y = fed['Retrieval_Time']
        y = _filterout(y, dropna=True)
        return y
    agg = 'mean'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

# ---- Dicts for metric access

# link keywords to their default function
Metric = namedtuple("Metric", ['func', 'nicename'])

METRICS = {'battery'           : Metric(battery, "Battery Life (V)"),
           'binary_pellets'    : Metric(binary_pellets, "Pellets"),
           'cumulative_pellets': Metric(cumulative_pellets, "Pellets"),
           'ipi'               : Metric(ipi, "Interpellet Intervals"),
           'motor'             : Metric(motor_turns, "Motor Turns"),
           'pellets'           : Metric(pellets, "Pellets"),
           'rt'                : Metric(retrival_time, "Retrieval Time (s)")}
