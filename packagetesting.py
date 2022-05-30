#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 11:02:24 2021

@author: earnestt1234
"""

import fed3
import fed3.plot as fplot

import numpy as np

# load FED data
# a = fed3.load(r"/Users/earnestt1234/Documents/fedviz/justin_data/FED7Cat.csv")
# b = fed3.load(r"/Users/earnestt1234/Documents/fedviz/justin_data/FED3Cat.csv")

a = fed3.load(r"C:\Users\earne\Documents\fedviz\justin_data\FED3Cat.csv")
b = fed3.load(r"C:\Users\earne\Documents\fedviz\justin_data\FED7Cat.csv")


from fed3.plot.helpers import _parse_feds
from fed3.core.fedfuncs import screen_mixed_alignment

from fed3.metrics.tables import (_create_group_metric_df,  _create_metric_df, _bar_metric_df)

from fed3.metrics.core import (_get_metric, _get_metricname,)

feds = {'a':[a, b], 'b':[a, b]}
y = 'pellets'
stat = 'max'
mixed_align = 'raise'

import matplotlib.pyplot as plt

# def bar(feds, stat, y='pellets'):

feds_dict = _parse_feds(feds)

# setup input arguments
feds_all = []
for l in feds_dict.values():
    feds_all += l

# screen issues alignment
alignment = screen_mixed_alignment(feds_all, option=mixed_align)

metric = _get_metric(y)
metricname = _get_metricname(y)
DATA = _bar_metric_df(feds_dict, metric, stat)
individual_data = DATA.iloc[:, :-2]
barvals = DATA.iloc[:, -2]
errors = DATA.iloc[:, -1]
idx = range(len(DATA))

fig, ax = plt.subplots()
ax.bar(idx, barvals, label=DATA.index)
ax.errorbar(x=idx, y=barvals, yerr=errors, color='grey', ls='none', capsize=5)