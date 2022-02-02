#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  9 12:42:13 2021

@author: earnestt1234
"""

import matplotlib.pyplot as plt
import seaborn as sns

from fed3.format_axis import (FORMAT_XAXIS_OPTS,)

from fed3.lightcycle import (LIGHTCYCLE,
                             shade_darkness)

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

def plot_line_data(ax, data, xaxis='datetime', shadedark=True,
                   legend=True, drawstyle='steps', ylabel='', **kwargs):
    for col in data.columns:
        y = data[col].dropna()
        x = y.index
        ax.plot(x, y, label=col, drawstyle=drawstyle)

    if shadedark:
        shade_darkness(ax, x.min(), x.max(),
                       lights_on=LIGHTCYCLE['on'],
                       lights_off=LIGHTCYCLE['off'])

    if legend:
        ax.legend()

    FORMAT_XAXIS_OPTS[xaxis](ax, x.min(), x.max())
    ax.set_ylabel(ylabel)

def plot_hist_data(ax, data, logx, kde, xlabel, **kwargs):
    for i, col in enumerate(data.columns):
        y = data[col].dropna()
        sns.histplot(y, kde=kde, log_scale=logx, color=colors[i])
    ax.set_xlabel(xlabel)