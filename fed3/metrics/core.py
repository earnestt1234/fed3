#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This modules defines functions which are called on individual FEDFrame
objects to extract temporal variables of interest.  It also provides
a small API for accessing them.

For a current list of available metrics, call:

```python
>>> fed3.list_metrics()
['binary_pellets',
 'cumulative_pellets',
 'pellets',
 'binary_pokes',
 'cumulative_pokes',
 'pokes',
 'binary_left_pokes',
 'binary_right_pokes',
 'cumulative_left_pokes',
 'cumulative_right_pokes',
 'cumulative_left_percent',
 'cumulative_right_percent',
 'left_pokes',
 'right_pokes',
 'binary_correct_pokes',
 'binary_error_pokes',
 'cumulative_correct_pokes',
 'cumulative_error_pokes',
 'cumulative_correct_percent',
 'cumulative_error_percent',
 'correct_pokes',
 'error_pokes',
 'battery',
 'ipi',
 'motor',
 'rt']

```

Note that for now, the individual metric functions are not included
in the default fed3 namespace, and are undocumented.  They can still
be access with `get_metric`.
"""

__all__ = ['get_metric', 'list_metrics']

from collections import namedtuple
import warnings

import pandas as pd

# ---- General helpers

def _default_metric(fed, func, bins=None, origin='start',
                    agg='sum'):
    '''Call a function of a FEDFrame in the "default manner".  It is
    so-called "default" in that most metrics can be constructed using
    this function.'''
    if bins is None:
        out = func(fed)
    else:
        vals = func(fed)
        G = pd.Grouper(freq=bins, origin=origin)
        out = vals.groupby(G).agg(agg)

    return out

def _filterout(series, dropna=False, dropzero=False, deduplicate=False):
    '''Helper for cleaning up some metrics.'''

    if dropna:
        series = series.dropna()
    if dropzero:
        series = series[series != 0]
    if deduplicate:
        series = series[~series.duplicated()]

    return series

# ---- Helpers for computing metrics

def _cumulative_poke_percentage_general(fed, kind):
    '''General function which is used to compute either the cumulative
    left, right, correct, or error poke percentage.'''

    kinds = ['left', 'right', 'correct', 'error']
    if kind not in kinds:
        raise ValueError(f'`kind` must be one of {kinds}')

    if kind == 'left':
        a = cumulative_left_pokes(fed)
        b = cumulative_right_pokes(fed)
    elif kind == 'right':
        a = cumulative_right_pokes(fed)
        b = cumulative_left_pokes(fed)
    elif kind == 'correct':
        a = cumulative_correct_pokes(fed)
        b = cumulative_error_pokes(fed)
    elif kind == 'error':
        a = cumulative_error_pokes(fed)
        b = cumulative_correct_pokes(fed)

    idx = a.index.union(b.index)

    try:
        a = a.reindex(idx)
        b = b.reindex(idx)
    except ValueError:
        warnings.warn("Unable to reindex two poke arrays, likely "
                      "due to duplicate index.  Using pandas `duplicated()` "
                      "to remove duplicate indices.",
                      RuntimeWarning)

        a = a.loc[~ a.index.duplicated()]
        b = b.loc[~ b.index.duplicated()]
        a = a.reindex(idx)
        b = b.reindex(idx)

    a = a.ffill().fillna(0)
    b = b.ffill().fillna(0)
    total = a + b

    return (a / total) * 100

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

def binary_pokes(fed, bins=None, origin='start'):
    func = lambda f: f.pokes(kind='any', cumulative=False, condense=True)
    agg = 'sum'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

def cumulative_pokes(fed, bins=None, origin='start'):
    func = lambda f: f.pokes(kind='any', cumulative=True, condense=True)
    agg = 'max'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

def pokes(fed, bins=None, origin='start'):
    func = cumulative_pokes if bins is None else binary_pokes
    return func(fed, bins=bins, origin=origin)

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

def cumulative_left_percent(fed, bins=None, origin='start'):
    func = lambda f: _cumulative_poke_percentage_general(f, 'left')
    agg = 'last'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

def cumulative_right_percent(fed, bins=None, origin='start'):
    func = lambda f: _cumulative_poke_percentage_general(f, 'right')
    agg = 'last'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

def left_pokes(fed, bins=None, origin='start'):
    func = cumulative_left_pokes if bins is None else binary_left_pokes
    return func(fed, bins=bins, origin=origin)

def right_pokes(fed, bins=None, origin='start'):
    func = cumulative_right_pokes if bins is None else binary_right_pokes
    return func(fed, bins=bins, origin=origin)

# ---- Correct / Error pokes

# you can do a find and replace on the left/right ...

def binary_correct_pokes(fed, bins=None, origin='start'):
    func = lambda f: f.pokes(kind='correct', cumulative=False, condense=True)
    agg = 'sum'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

def binary_error_pokes(fed, bins=None, origin='start'):
    func = lambda f: f.pokes(kind='error', cumulative=False, condense=True)
    agg = 'sum'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

def cumulative_correct_pokes(fed, bins=None, origin='start'):
    func = lambda f: f.pokes(kind='correct', cumulative=True, condense=True)
    agg = 'max'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

def cumulative_error_pokes(fed, bins=None, origin='start'):
    func = lambda f: f.pokes(kind='error', cumulative=True, condense=True)
    agg = 'max'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

def cumulative_correct_percent(fed, bins=None, origin='start'):
    func = lambda f: _cumulative_poke_percentage_general(f, 'correct')
    agg = 'last'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

def cumulative_error_percent(fed, bins=None, origin='start'):
    func = lambda f: _cumulative_poke_percentage_general(f, 'error')
    agg = 'last'
    return _default_metric(fed=fed, func=func, bins=bins, origin=origin, agg=agg)

def correct_pokes(fed, bins=None, origin='start'):
    func = cumulative_correct_pokes if bins is None else binary_correct_pokes
    return func(fed, bins=bins, origin=origin)

def error_pokes(fed, bins=None, origin='start'):
    func = cumulative_error_pokes if bins is None else binary_error_pokes
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

# ---- Metric access

def get_metric(y):
    '''
    Return a metric function from its key.

    Parameters
    ----------
    y : str
        Key for metric.

    Raises
    ------
    KeyError
        Metric key not recognized.

    Returns
    -------
    namedtuple
        Named tuple with a `func` and `nicename` attribute.  The `func`
        is the actual metric function, which can be called on FEDFrames.
        The `nicename` is a nicer version of the key, used for axis labels.

    '''

    key = y.lower()
    try:
        return METRICS[key]
    except KeyError:
        metrics = str(list(METRICS.keys()))[1:-1]
        raise KeyError(f'Metric key "{y}" is not recognized. Possible metrics are: '
                       f'{metrics}.')

def list_metrics():
    '''
    List all available metric keys.

    Returns
    -------
    list

    '''
    return list(METRICS.keys())

# link keywords to their default function
Metric = namedtuple("Metric", ['func', 'nicename'])
"""Lightweight class for metric functions and their representation names."""

METRICS = {'binary_pellets'             : Metric(binary_pellets, "Pellets"),
           'cumulative_pellets'         : Metric(cumulative_pellets, "Pellets"),
           'pellets'                    : Metric(pellets, "Pellets"),
           'binary_pokes'               : Metric(binary_pokes, "Pokes"),
           'cumulative_pokes'           : Metric(cumulative_pokes, "Pokes"),
           'pokes'                      : Metric(pokes, "Pokes"),
           'binary_left_pokes'          : Metric(binary_left_pokes, "Left Pokes"),
           'binary_right_pokes'         : Metric(binary_right_pokes, "Right Pokes"),
           'cumulative_left_pokes'      : Metric(cumulative_left_pokes, "Left Pokes"),
           'cumulative_right_pokes'     : Metric(cumulative_right_pokes, "Right Pokes"),
           'cumulative_left_percent'    : Metric(cumulative_left_percent, "Left Pokes (%)"),
           'cumulative_right_percent'   : Metric(cumulative_right_percent, "Right Pokes (%)"),
           'left_pokes'                 : Metric(left_pokes, "Left Pokes"),
           'right_pokes'                : Metric(right_pokes, "Right Pokes"),
           'binary_correct_pokes'       : Metric(binary_correct_pokes, "correct Pokes"),
           'binary_error_pokes'         : Metric(binary_error_pokes, "Right Pokes"),
           'cumulative_correct_pokes'   : Metric(cumulative_correct_pokes, "Left Pokes"),
           'cumulative_error_pokes'     : Metric(cumulative_error_pokes, "Right Pokes"),
           'cumulative_correct_percent' : Metric(cumulative_correct_percent, "Left Pokes (%)"),
           'cumulative_error_percent'   : Metric(cumulative_error_percent, "Right Pokes (%)"),
           'correct_pokes'              : Metric(correct_pokes, "Left Pokes"),
           'error_pokes'                : Metric(error_pokes, "Right Pokes"),
           'battery'                    : Metric(battery, "Battery Life (V)"),
           'ipi'                        : Metric(ipi, "Interpellet Intervals"),
           'motor'                      : Metric(motor_turns, "Motor Turns"),
           'rt'                         : Metric(retrival_time, "Retrieval Time (s)")}
'''Dictionary for storing all metrics.'''
