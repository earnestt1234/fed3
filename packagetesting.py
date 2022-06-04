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

c = fed3.split(a, dates = a.index[[1000, 2000, 3000, 4000, 5000]])
d = fed3.split(b, dates = b.index[[1000, 2000, 3000, 4000, 5000]])

# from fed3.plot.helpers import _parse_feds
# from fed3.core.fedfuncs import screen_mixed_alignment

# from fed3.metrics.tables import (_create_group_metric_df,  _create_metric_df, _bar_metric_df)

# from fed3.metrics.core import (_get_metric, _get_metricname,)

# from fed3.plot import COLORCYCLE

# def assign_bar_positions_widths(feds_dict, positions_arg=None, position_width=0.75):

#     if positions_arg is None:
#         positions_arg = np.arange(len(feds_dict))

#     if len(positions_arg) != len(feds_dict):
#         raise ValueError('positions argument must equal the length of the input')

#     positions = np.array(positions_arg, dtype='int')

#     if any(np.diff(positions) > 1):
#         raise ValueError("positions must be only integers with none skipped.")

#     centers, counts = np.unique(positions, return_counts=True)
#     bw = position_width / max(counts)

#     positions = []
#     bar_widths = []
#     for x, c in zip(centers, counts):
#         start = x - (.5 * c * bw)
#         end  = x + (.5 * c * bw)
#         positions += list(np.arange(start + bw/2, end, bw))
#         bar_widths += [bw] * c

#     return centers, positions, bar_widths

# def jitter_ys(ys, xcenter, spread):

#     xs = np.random.uniform(0, spread/2, size=len(ys))
#     half = int(len(ys)/2)
#     xs[np.arange(len(xs)) < half] *= -1
#     np.random.shuffle(xs)
#     xs += xcenter
#     return xs

# feds = {'C':c, 'D':d}
# y = 'pellets'
# stat = 'max'
# mixed_align = 'raise'
# positions = [0, 1]
# position_labels = ['C', 'D']
# bar_kwargs = None
# error_kwargs = None
# scatter_kwargs = None

# import matplotlib.pyplot as plt

# # def bar(feds, stat, y='pellets'):

# feds_dict = _parse_feds(feds)

# # setup input arguments
# feds_all = []
# for l in feds_dict.values():
#     feds_all += l

# # screen issues alignment
# alignment = screen_mixed_alignment(feds_all, option=mixed_align)

# metric = _get_metric(y)
# metricname = _get_metricname(y)
# DATA = _bar_metric_df(feds_dict, metric, stat)
# individual_data = DATA.iloc[:, :-2]
# barvals = DATA.iloc[:, -2]
# errors = DATA.iloc[:, -1]
# show_individual = True

# position_width = 0.75
# centers, positions, bar_widths = assign_bar_positions_widths(feds,
#                                                              positions,
#                                                              position_width=position_width)

# fig, ax = plt.subplots()

# for i, x in enumerate(positions):
#     y = barvals[i]
#     w = bar_widths[i]
#     label = DATA.index[i]
#     err = errors[i]
#     color = COLORCYCLE[i]

#     ax.bar(x, y, width=w, label=label, color=color, zorder=0)
#     ax.errorbar(x=x, y=y, yerr=err, color='grey', ls='none', capsize=5, zorder=2)
#     if show_individual:
#         spread = w * .3
#         ys = individual_data.iloc[i, :].dropna()
#         xs = jitter_ys(ys, x, spread)
#         ax.scatter(xs, ys, zorder=1, color=color, edgecolor='k')

# ax.set_xticks(centers)
# if position_labels is not None:
#     ax.set_xticklabels(position_labels)