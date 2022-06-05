#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 18:27:07 2021

@author: earnestt1234
"""

from collections import namedtuple
import warnings

import pandas as pd

# ---- Helpers

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

# ---- Pellets

def binary_pellets(fed, bins=None, origin='start'):

    def _get_binary_pellets(fed):
        y = fed.binary_pellets()
        y = _filterout(y, dropzero=True)
        return y

    return _default_metric(fed,
                           func=_get_binary_pellets,
                           bins=bins,
                           origin=origin,
                           agg='sum')

def cumulative_pellets(fed, bins=None, origin='start'):

    def _get_cumulative_pellets(fed):
        y = fed['Pellet_Count']
        y = _filterout(y, deduplicate=True, dropzero=True)
        return y

    return _default_metric(fed,
                           func=_get_cumulative_pellets,
                           bins=bins,
                           origin=origin,
                           agg='max')

def pellets(fed, bins=None, origin='start'):

    func = cumulative_pellets if bins is None else binary_pellets

    return func(fed, bins=bins, origin=origin)

# ---- Any sided pokes

# ---- L/R pokes

def binary_left_pokes(fed, bins=None, origin='start'):

    def _get_binary_left(fed):
        y = fed.binary_pokes(side='left')
        y = _filterout(y, dropzero=True)
        return y

    return _default_metric(fed,
                           func=_get_binary_left,
                           bins=bins,
                           origin=origin,
                           agg='sum')

def binary_right_pokes(fed, bins=None, origin='start'):

    def _get_binary_right(fed):
        y = fed.binary_pokes(side='right')
        y = _filterout(y, dropzero=True)
        return y

    return _default_metric(fed,
                           func=_get_binary_right,
                           bins=bins,
                           origin=origin,
                           agg='sum')

def cumulative_left_pokes(fed, bins=None, origin='start'):

    def _get_cumulative_left(fed):
        y = fed['Left_Poke_Count']
        y = _filterout(y, deduplicate=True, dropzero=True)
        return y

    return _default_metric(fed,
                           func=_get_cumulative_left,
                           bins=bins,
                           origin=origin,
                           agg='max')

def cumulative_right_pokes(fed, bins=None, origin='start'):

    def _get_cumulative_right(fed):
        y = fed['Right_Poke_Count']
        y = _filterout(y, deduplicate=True, dropzero=True)
        return y

    return _default_metric(fed,
                           func=_get_cumulative_right,
                           bins=bins,
                           origin=origin,
                           agg='max')

def cumulative_left_percentage(fed, bins=None, origin='start'):

    def _get_crp(fed):

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
        p = (l / total) * 100

        return p

    return _get_crp(fed)


# ---- Other

def battery(fed, bins=None, origin='start'):

    def _get_battery(fed):
        return fed['Battery_Voltage']

    return _default_metric(fed,
                           func=_get_battery,
                           bins=bins,
                           origin=origin,
                           agg='mean')

def ipi(fed, bins=None, origin='start'):

    def _get_ipi(fed):
        y = fed.ipi()
        y = _filterout(y, dropna=True)
        return y

    return _default_metric(fed,
                           func=_get_ipi,
                           bins=bins,
                           origin=origin,
                           agg='mean')

def motor_turns(fed, bins=None, origin='start'):

    def _get_mt(fed):
        pellets = fed.binary_pellets().astype(bool)
        y = fed.loc[pellets, 'Motor_Turns']
        return y

    return _default_metric(fed,
                           func=_get_mt,
                           bins=bins,
                           origin=origin,
                           agg='mean')

def retrival_time(fed, bins=None, origin='start'):

    def _get_rt(fed):
        y = fed['Retrieval_Time']
        y = _filterout(y, dropna=True)
        return y

    return _default_metric(fed,
                           func=_get_rt,
                           bins=bins,
                           origin=origin,
                           agg='mean')

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
