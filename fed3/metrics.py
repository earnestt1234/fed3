#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 18:27:07 2021

@author: earnestt1234
"""

class Metric:
    def __init__(self, key, nicename, defaultagg='mean',
                 cumulative=None, noncumulative=None,):
        self.key = key
        self.nicename = nicename
        self.cumulative = cumulative
        self.noncumulative = noncumulative
        self.defaultagg = defaultagg

    def __call__(self, fed, cumulative=True, use_other=True):
        options = {True: self.cumulative, False: self.noncumulative}
        func = options[cumulative]
        if func is None and use_other:
            func = options[not cumulative]
        return func(fed)

def filterout(series, dropna=False, dropzero=False, deduplicate=False):
    if dropna:
        series = series.dropna()
    if dropzero:
        series = series[series != 0]
    if deduplicate:
        series = series[~series.duplicated()]
    return series

def get_pellets(fed):
    y = fed.data['Pellet_Count']
    y = filterout(y, deduplicate=True)
    return y

def get_binary_pellets(fed):
    y = fed.binary_pellets()
    y = filterout(y, dropzero=True)
    return y

def get_ipi(fed):
    y = fed.interpellet_intervals()
    y = filterout(y, dropna=True)
    return y

pellets = Metric('pellets', 'Pellets', 'mean',
                 get_pellets, get_binary_pellets)
ipi = Metric('ipi', 'Interpellet Intervals', 'mean',
             cumulative=None, noncumulative=get_ipi)

metricsdict = {'pellets': pellets,
               'ipi': ipi}