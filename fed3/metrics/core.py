#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 18:27:07 2021

@author: earnestt1234
"""

from fed3.metrics.helpers import (_default_metric,
                                  _get_binary_pellets,
                                  _get_cumulative_pellets,
                                  _get_ipi)

def binary_pellets(fed, bins=None, origin='start'):

    return _default_metric(fed,
                           nonbinned_func=_get_binary_pellets,
                           binned_func=_get_binary_pellets,
                           bins=bins,
                           origin=origin,
                           agg='sum')

def cumulative_pellets(fed, bins=None, origin='start'):

    return _default_metric(fed,
                           nonbinned_func=_get_cumulative_pellets,
                           binned_func=_get_cumulative_pellets,
                           bins=bins,
                           origin=origin,
                           agg='mean')

def pellets(fed, bins=None, origin='start'):

    return _default_metric(fed,
                           nonbinned_func=_get_cumulative_pellets,
                           binned_func=_get_binary_pellets,
                           bins=bins,
                           origin=origin,
                           agg='sum')

def ipi(fed, bins=None, origin='start'):

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
