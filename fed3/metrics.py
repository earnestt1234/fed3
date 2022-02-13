#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 18:27:07 2021

@author: earnestt1234
"""
from abc import ABCMeta, abstractmethod

import pandas as pd
import numpy as np

# ---- helper functions
def filterout(series, dropna=False, dropzero=False, deduplicate=False):
    if dropna:
        series = series.dropna()
    if dropzero:
        series = series[series != 0]
    if deduplicate:
        series = series[~series.duplicated()]
    return series

# # ---- Metric Class

class Metric(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def cumulative(fed, **kwargs):
        ...

    @classmethod
    @abstractmethod
    def noncumulative(fed, **kwargs):
        ...

    @classmethod
    @abstractmethod
    def binned(fed, bins, origin, **kwargs):
        ...

class Pellets(Metric):

    def cumulative(self, fed):
        return get_pellets(fed)

    def noncumulative(self, fed):
        return get_binary_pellets(fed)

    def binned(self, fed, bins, agg='sum', origin='start'):
        G = pd.Grouper(freq=bins, origin=origin)
        values = get_binary_pellets(fed).groupby(G).apply(agg)
        return values

    def __call__(self, fed):
        return self.cumulative(fed)

# ---- metric functions
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

# ---- module variables

# link keywords to their default function
METRICS = {'pellets': get_pellets,
           'bpellets': get_binary_pellets,
           'cpellets': get_pellets,
           'ipi': get_ipi}

# link keywords to names
METRICNAMES = {'pellets': 'Pellets',
               'bpellets': 'Pellets',
               'cpellets': 'Pellets',
               'ipi': 'Interpellet Intervals'}
