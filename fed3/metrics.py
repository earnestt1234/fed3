#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 18:27:07 2021

@author: earnestt1234
"""

from fed3.metrics_helpers import (_default_metric,
                                  get_binary_pellets,
                                  get_cumulative_pellets,
                                  get_ipi)

def binary_pellets(fed, bins=None, origin='start'):

    return _default_metric(fed,
                           nonbinned_func=get_binary_pellets,
                           binned_func=get_binary_pellets,
                           bins=bins,
                           origin=origin,
                           agg='sum')

def cumulative_pellets(fed, bins=None, origin='start'):

    return _default_metric(fed,
                           nonbinned_func=get_cumulative_pellets,
                           binned_func=get_cumulative_pellets,
                           bins=bins,
                           origin=origin,
                           agg='mean')

def pellets(fed, bins=None, origin='start'):

    return _default_metric(fed,
                           nonbinned_func=get_cumulative_pellets,
                           binned_func=get_binary_pellets,
                           bins=bins,
                           origin=origin,
                           agg='sum')

def ipi(fed, bins=None, origin='start'):

    return _default_metric(fed,
                           nonbinned_func=get_ipi,
                           binned_func=get_ipi,
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
