#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 18:06:53 2021

@author: earnestt1234
"""

import matplotlib.pyplot as plt
import pandas as pd

from fed3.fedframe.fedfuncs import screen_mixed_alignment

from fed3.plot.generic import (plot_line_data,
                               plot_line_error,
                               plot_scatter_data)

from fed3.plot.helpers import (_create_group_metric_df,
                               _create_metric_df,
                               _get_metric,
                               _get_metricname,
                               _get_return_value,
                               _handle_feds,)

# ---- low level plotting
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

def _simple_group_plot(feds, y='pellets', bins='1H', agg='mean', var='std',
                       mixed_align='raise', output='plot',
                       xaxis='auto', shadedark=True, ax=None, legend=True,
                       fed_styles=None, **kwargs):

    # set the outputs
    FIG = None
    DATA = pd.DataFrame()

    # setup input arguments
    feds_dict = {k:_handle_feds(v) for k, v in feds.items()}
    feds_all = []
    for l in feds.values():
        feds_all += l

    # screen issues alignment
    alignment = screen_mixed_alignment(feds_all, option=mixed_align)

    # get resample time
    origin = min(f.start_time.floor('1H') for f in feds_all)

    # compute data
    metric = _get_metric(y)
    metricname = _get_metricname(y)
    AGGDATA, VARDATA = _create_group_metric_df(feds=feds_dict,
                                               metric=metric,
                                               agg=agg,
                                               var=var,
                                               bins=bins,
                                               origin=origin)

    # create return data
    DATA = AGGDATA

    # handle plot creation and returns
    if output in ['plot', 'data', 'both']:

        if ax is None:
            ax = plt.gca()

        if xaxis == 'auto':
            xaxis = alignment

        if xaxis == 'elapsed':
            shadedark = False

        FIG = plot_line_data(ax=ax,
                             data=AGGDATA,
                             shadedark=shadedark,
                             legend=legend,
                             xaxis=xaxis,
                             ylabel=metricname,
                             fed_styles=fed_styles,
                             drawstyle='default',
                             **kwargs)

        plot_line_error(ax=ax, aggdata=AGGDATA, vardata=VARDATA)

    return _get_return_value(FIG=FIG, DATA=DATA, output=output)

# ---- public plotting functions
def line(feds, y='pellets', mixed_align='raise', output='plot',
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

def scatter(feds, y='pellets', mixed_align='raise', output='plot',
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
