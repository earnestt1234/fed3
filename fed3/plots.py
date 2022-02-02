#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 18:06:53 2021

@author: earnestt1234
"""

import matplotlib.pyplot as plt
import pandas as pd

from fed3.fedfuncs import screen_mixed_alignment

from fed3.metrics import METRICS, METRICNAMES

from fed3.plothelpers import (plot_line_data,
                              plot_hist_data,
                              plot_scatter_data)

# ---- helper functions
def _create_metric_df(feds, metric):
    df = pd.DataFrame()
    for fed in feds:
        y = metric(fed)
        y.name = fed.name
        df = df.join(y, how='outer')

    return df

def _handle_feds(feds):
    if isinstance(feds, pd.DataFrame):
        feds = [feds]
    return feds

def _get_metric(y):
    if isinstance(y, str):

        key = y.lower()
        try:
            return METRICS[key]
        except KeyError:
            raise ValueError(f'y-value "{y}" is not recognized.')

    else:
        return y

def _get_metricname(y):

    if isinstance(y, str):

        key = y.lower()
        try:
            return METRICNAMES[key]
        except KeyError:
            raise ValueError(f'y-value "{y}" is not recognized.')

    else:
        return y.__name__

def _get_return_value(FIG, DATA, output):

    if output == 'plot':
        return FIG

    elif output in ['dataonly', 'data']:
        return DATA

    elif output == 'both':
        return FIG, DATA

    else:
        raise ValueError(f'output value "{output}" not recognized.')

# ---- generic plotting functions
def _simple_plot(feds, kind='line', y='pellets', mixed_align='raise', output='plot',
                 xaxis='auto', shadedark=True, ax=None, legend=True,
                 fed_styles=None, **kwargs):

    # determine general plotting function
    if kind == 'line':
        plotfunc = plot_line_data

    elif kind == 'scatter':
        plotfunc = plot_scatter_data

    else:
        raise ValueError(f'kind must be "line" or "scatter"; not {kind}')

    # set the outputs
    FIG = None
    DATA = pd.DataFrame()

    # handle arguments
    feds = _handle_feds(feds)
    alignment = screen_mixed_alignment(feds, option=mixed_align)

    # compute data
    metric = _get_metric(y)
    metricname = _get_metricname(y)
    DATA = _create_metric_df(feds=feds, metric=metric)

    # handle plot creation and returns
    if output in ['plot', 'data', 'both']:

        if ax is None:
            ax = plt.gca()

        if xaxis == 'auto':
            xaxis = alignment

        if xaxis == 'elapsed':
            shadedark = False

        FIG = plotfunc(ax=ax,
                       data=DATA,
                       shadedark=shadedark,
                       legend=legend,
                       xaxis=xaxis,
                       ylabel=metricname,
                       fed_styles=fed_styles,
                       **kwargs)

    return _get_return_value(FIG=FIG, DATA=DATA, output=output)


# ---- public plotting functions
def line_plot(feds, y='pellets', mixed_align='raise', output='plot',
              xaxis='auto', shadedark=True, ax=None, legend=True,
              fed_styles=None, **kwargs):

    return _simple_plot(kind='line',
                        feds=feds,
                        y=y,
                        mixed_align=mixed_align,
                        output=output,
                        xaxis=xaxis,
                        shadedark=shadedark,
                        ax=ax,
                        legend=legend,
                        fed_styles=fed_styles,
                        **kwargs)

def ipi_plot(feds, logx=True, kde=True, mixed_align='raise', output='plot',
             ax=None, legend=True, fed_styles=None, **kwargs):
    # set the outputs
    FIG = None
    DATA = pd.DataFrame()

    # handle arguments
    feds = _handle_feds(feds)
    screen_mixed_alignment(feds, option=mixed_align)

    # compute data
    y = 'ipi'
    metric = _get_metric(y)
    metricname = _get_metricname(y)
    DATA = _create_metric_df(feds=feds, metric=metric)

    # handle plot creation and returns
    if output in ['plot', 'data', 'both']:

        if ax is None:
            ax = plt.gca()

        FIG = plot_hist_data(ax=ax,
                             data=DATA,
                             logx=logx,
                             kde=kde,
                             xlabel=metricname,
                             fed_styles=fed_styles,
                             legend=legend,
                             **kwargs)


    return _get_return_value(FIG=FIG, DATA=DATA, output=output)


def scatter_plot(feds, y='pellets', mixed_align='raise', output='plot',
                 xaxis='auto', shadedark=True, ax=None, legend=True,
                 fed_styles=None, **kwargs):

    return _simple_plot(kind='scatter',
                        feds=feds,
                        y=y,
                        mixed_align=mixed_align,
                        output=output,
                        xaxis=xaxis,
                        shadedark=shadedark,
                        ax=ax,
                        legend=legend,
                        fed_styles=fed_styles,
                        **kwargs)
