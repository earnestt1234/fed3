#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 12:31:45 2022

@author: earnestt1234
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from fed3.lightcycle import LIGHTCYCLE

from fed3.plot.format_axis import FORMAT_XAXIS_OPTS

from fed3.plot.shadedark import shade_darkness

prop_cycle = plt.rcParams['axes.prop_cycle']
COLORCYCLE = prop_cycle.by_key()['color']

def _apply_fed_styles(style_func, fedname, plot_kwargs):
    new_kwargs = style_func(fedname)
    if new_kwargs is None:
        pass
    else:
        plot_kwargs.update(new_kwargs)
    return plot_kwargs

def plot_hist_data(ax, data, logx, kde, xlabel, fed_styles=None, legend=True,
                   **kwargs):

    for i, col in enumerate(data.columns):

        plot_kwargs = kwargs.copy()
        plot_kwargs['color'] = COLORCYCLE[i]
        plot_kwargs['kde'] = kde
        plot_kwargs['label'] = col
        plot_kwargs['log_scale'] = logx
        if fed_styles is not None:
            _apply_fed_styles(fed_styles, fedname=col, plot_kwargs=plot_kwargs)

        y = data[col].dropna()
        sns.histplot(y, **plot_kwargs)

    ax.set_xlabel(xlabel)

    if legend:
        ax.legend()

    return ax.get_figure()

def plot_line_data(ax, data, xaxis='datetime', shadedark=True,
                   legend=True, drawstyle='steps', ylabel='',
                   fed_styles=None, **kwargs):

    for i, col in enumerate(data.columns):

        plot_kwargs = kwargs.copy()
        plot_kwargs['color'] = COLORCYCLE[i]
        plot_kwargs['drawstyle'] = drawstyle
        plot_kwargs['label'] = col
        if fed_styles is not None:
            _apply_fed_styles(fed_styles, fedname=col, plot_kwargs=plot_kwargs)

        y = data[col].dropna()
        x = y.index
        ax.plot(x, y, **plot_kwargs)

    if shadedark:
        shade_darkness(ax, x.min(), x.max(),
                       lights_on=LIGHTCYCLE['on'],
                       lights_off=LIGHTCYCLE['off'])

    if legend:
        ax.legend()

    FORMAT_XAXIS_OPTS[xaxis](ax, x.min(), x.max())
    ax.set_ylabel(ylabel)

    return ax.get_figure()

def plot_scatter_data(ax, data, xaxis='datetime', shadedark=True,
                      legend=True, drawstyle='steps', ylabel='',
                      fed_styles=None, **kwargs):

    for i, col in enumerate(data.columns):

        plot_kwargs = kwargs.copy()
        plot_kwargs['color'] = COLORCYCLE[i]
        plot_kwargs['label'] = col
        if fed_styles is not None:
            _apply_fed_styles(fed_styles, fedname=col, plot_kwargs=plot_kwargs)

        y = data[col].dropna()
        x = y.index
        ax.scatter(x, y, **plot_kwargs)

    if shadedark:
        shade_darkness(ax, x.min(), x.max(),
                       lights_on=LIGHTCYCLE['on'],
                       lights_off=LIGHTCYCLE['off'])

    if legend:
        ax.legend()

    FORMAT_XAXIS_OPTS[xaxis](ax, x.min(), x.max())
    ax.set_ylabel(ylabel)

    return ax.get_figure()