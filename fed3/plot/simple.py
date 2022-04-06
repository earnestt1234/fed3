#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 18:06:53 2021

@author: earnestt1234
"""

import matplotlib.pyplot as plt
import pandas as pd

from fed3.fedframe.fedfuncs import screen_mixed_alignment

from fed3.lightcycle import LIGHTCYCLE

from fed3.metrics.tables import (_create_group_metric_df,  _create_metric_df,)

from fed3.metrics.core import (_get_metric, _get_metricname,)

from fed3.plot import COLORCYCLE
from fed3.plot.format_axis import FORMAT_XAXIS_OPTS
from fed3.plot.helpers import (_get_return_value, _handle_feds,)
from fed3.plot.shadedark import shade_darkness

# ---- low level plotting

def _plot_timeseries_line(ax, data, **kwargs):

    y = data.dropna()
    x = y.index
    ax.plot(x, y, **kwargs)

    return ax.get_figure()

def _plot_timeseries_scatter(ax, data, **kwargs):

    y = data.dropna()
    x = y.index
    ax.scatter(x, y, **kwargs)

    return ax.get_figure()

def _plot_timeseries_shade(ax, aggdata, vardata, **kwargs):
    x = aggdata.index
    y = aggdata
    ymin = y - vardata
    ymax = y + vardata
    ax.fill_between(x=x, y1=ymin, y2=ymax, **kwargs)

def _plot_timeseries_errorbars(ax, aggdata, vardata, **kwargs):
    x = aggdata.index
    y = aggdata
    yerr = vardata
    ax.errorbar(x=x, y=y, yerr=yerr, **kwargs)

# ---- common function for scatter / line
def _simple_plot(feds, kind='line', y='pellets', bins=None,
                 mixed_align='raise', output='plot',
                 xaxis='auto', shadedark=True, ax=None, legend=True,
                 line_kwargs=None, **kwargs):

    # determine general plotting function
    if kind == 'line':
        plotfunc = _plot_timeseries_line

    elif kind == 'scatter':
        plotfunc = _plot_timeseries_scatter

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
    DATA = _create_metric_df(feds=feds, metric=metric, bins=bins)

    # handle plot creation and returns
    if output in ['plot', 'data', 'both']:

        line_kwargs = {} if line_kwargs is None else line_kwargs

        if ax is None:
            ax = plt.gca()

        if xaxis == 'auto':
            xaxis = alignment

        if xaxis == 'elapsed':
            shadedark = False

        for i, col in enumerate(DATA.columns):

            # set keyword args passed
            plot_kwargs = kwargs.copy()
            plot_kwargs['color'] = (COLORCYCLE[i] if not plot_kwargs.get("color")
                                    else plot_kwargs.get("color"))
            plot_kwargs['label'] = col

            if line_kwargs.get(col):
                plot_kwargs.update(line_kwargs[col])

            # plot
            plotfunc(ax=ax, data=DATA[col], **plot_kwargs)

        # axis level formatting
        if shadedark:
            shade_darkness(ax, DATA.index.min(), DATA.index.max(),
                           lights_on=LIGHTCYCLE['on'],
                           lights_off=LIGHTCYCLE['off'])

        if legend:
            ax.legend()

        FORMAT_XAXIS_OPTS[xaxis](ax, DATA.index.min(), DATA.index.max())
        ax.set_ylabel(metricname)

        FIG = ax.get_figure()

    return _get_return_value(FIG=FIG, DATA=DATA, output=output)

def _simple_group_plot(feds, kind='line', y='pellets', bins='1H', agg='mean',
                       var='std', omit_na=False, mixed_align='raise', output='plot',
                       xaxis='auto', shadedark=True, ax=None, legend=True,
                       line_kwargs=None, **kwargs):

    # determine general plotting function
    if kind == 'line':
        plotfunc = _plot_timeseries_line
        errorfunc = _plot_timeseries_shade

    elif kind == 'scatter':
        plotfunc = _plot_timeseries_scatter
        errorfunc = _plot_timeseries_errorbars

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
                                               origin=origin,
                                               omit_na=omit_na)

    # create return data
    lsuffix = f"_{agg}" if isinstance(agg, str) else "_agg"
    rsuffix = f"_{var}" if isinstance(var, str) else "_var"
    DATA = AGGDATA.join(VARDATA, how='outer', lsuffix=lsuffix, rsuffix=rsuffix)

    # handle plot creation and returns
    if output in ['plot', 'data', 'both']:

        line_kwargs = {} if line_kwargs is None else line_kwargs

        if ax is None:
            ax = plt.gca()

        if xaxis == 'auto':
            xaxis = alignment

        if xaxis == 'elapsed':
            shadedark = False

        for i, col in enumerate(AGGDATA.columns):

            # set keyword args passed
            plot_kwargs = kwargs.copy()
            plot_kwargs['color'] = (COLORCYCLE[i] if not plot_kwargs.get("color")
                                    else plot_kwargs.get("color"))
            plot_kwargs['label'] = col

            if line_kwargs.get(col):
                plot_kwargs.update(line_kwargs[col])

            # plot
            plotfunc(ax=ax, data=AGGDATA[col], **plot_kwargs)

            # plot error
            aggdata = AGGDATA[col]
            vardata = VARDATA[col]
            errorfunc(ax=ax, aggdata=aggdata, vardata=vardata, alpha=0.3)

        # axis level formatting
        if shadedark:
            shade_darkness(ax, DATA.index.min(), DATA.index.max(),
                           lights_on=LIGHTCYCLE['on'],
                           lights_off=LIGHTCYCLE['off'])

        if legend:
            ax.legend()

        FORMAT_XAXIS_OPTS[xaxis](ax, DATA.index.min(), DATA.index.max())
        ax.set_ylabel(metricname)

    return _get_return_value(FIG=FIG, DATA=DATA, output=output)

# ---- public plotting functions
def line(feds, y='pellets', bins=None, agg='mean', var='std',
         omit_na=False, mixed_align='raise', output='plot',
         xaxis='auto', shadedark=True, ax=None, legend=True,
         line_kwargs=None, **kwargs):

    if isinstance(feds, dict):

        bins = '1H' if bins is None else bins

        return _simple_group_plot(kind='line',
                                  feds=feds,
                                  y=y,
                                  bins=bins,
                                  agg=agg,
                                  var=var,
                                  omit_na=omit_na,
                                  mixed_align=mixed_align,
                                  output=output,
                                  xaxis=xaxis,
                                  shadedark=shadedark,
                                  ax=ax,
                                  legend=legend,
                                  line_kwargs=line_kwargs,
                                  **kwargs)

    else:

        return _simple_plot(kind='line',
                            feds=feds,
                            y=y,
                            bins=bins,
                            mixed_align=mixed_align,
                            output=output,
                            xaxis=xaxis,
                            shadedark=shadedark,
                            ax=ax,
                            legend=legend,
                            line_kwargs=line_kwargs,
                            **kwargs)

def scatter(feds, y='pellets', bins=None, agg='mean', var='std',
            omit_na=False, mixed_align='raise', output='plot',
            xaxis='auto', shadedark=True, ax=None, legend=True,
            fed_styles=None, **kwargs):

    if isinstance(feds, dict):

        bins = '1H' if bins is None else bins

        return _simple_group_plot(kind='scatter',
                                  feds=feds,
                                  y=y,
                                  bins=bins,
                                  agg=agg,
                                  var=var,
                                  omit_na=omit_na,
                                  mixed_align=mixed_align,
                                  output=output,
                                  xaxis=xaxis,
                                  shadedark=shadedark,
                                  ax=ax,
                                  legend=legend,
                                  fed_styles=fed_styles,
                                  **kwargs)

    else:

        return _simple_plot(kind='scatter',
                            feds=feds,
                            y=y,
                            bins=bins,
                            mixed_align=mixed_align,
                            output=output,
                            xaxis=xaxis,
                            shadedark=shadedark,
                            ax=ax,
                            legend=legend,
                            fed_styles=fed_styles,
                            **kwargs)
