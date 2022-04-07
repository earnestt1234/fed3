#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 11:02:24 2021

@author: earnestt1234
"""

import fed3
import fed3.plot as fplot

import numpy as np

import matplotlib as mpl
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=["r", "k", "c"])

# load FED data
a = fed3.load('/Users/earnestt1234/Documents/fedviz/onemoretweak/FED001_012921_02.CSV')
# b = fed3.load('/Users/earnestt1234/Documents/fedviz/justin_data/FED3Cat.csv')
# c = fed3.load('/Users/earnestt1234/Documents/fedviz/justin_data/FED2Cat.csv')

metric = fed3.metrics.core.METRICS['pellets']
r = fed3.metrics.tables._chronogram_df([a], metric, bins='1T', relative_index=True,
                                       reorder_index=True)

fplot.line(a)