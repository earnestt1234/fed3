#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 18:06:53 2021

@author: earnestt1234
"""

__all__ = ['line', 'scatter']

import matplotlib.pyplot as plt
import pandas as pd

from fed3.core.fedfuncs import screen_mixed_alignment

from fed3.lightcycle import LIGHTCYCLE

from fed3.metrics.tables import (_create_group_metric_df,  _create_metric_df,)

from fed3.metrics.core import get_metric

from fed3.plot import OPTIONS
from fed3.plot.format_axis import FORMAT_XAXIS_OPTS
from fed3.plot.helpers import (_get_most_recent_color,
                               _get_return_value,
                               _parse_feds,
                               _process_plot_kwargs)
from fed3.plot.shadedark import shade_darkness

# ---- low level plotting

def _plot_timeseries_line(ax, data, **kwargs):
    '''Plot a pandas Series with a datetime index on a given
    matplotlib Axes, as a line.'''

    y = data.dropna()
    x = y.index
    ax.plot(x, y, **kwargs)

    return ax.get_figure()

def _plot_timeseries_scatter(ax, data, **kwargs):
    '''Plot a pandas Series with a datetime index on a given
    matplotlib Axes, as a scatter.'''

    y = data.dropna()
    x = y.index
    ax.scatter(x, y, **kwargs)

    return ax.get_figure()

def _plot_timeseries_shade(ax, aggdata, vardata, **kwargs):
    '''Plot the shaded error bar around a line.'''
    x = aggdata.index
    y = aggdata
    ymin = y - vardata
    ymax = y + vardata
    ax.fill_between(x=x, y1=ymin, y2=ymax, **kwargs)

def _plot_timeseries_errorbars(ax, aggdata, vardata, **kwargs):
    '''Plot vertical error bars around timeseries points.'''
    x = aggdata.index
    y = aggdata
    yerr = vardata
    ax.errorbar(x=x, y=y, yerr=yerr, ls='none', **kwargs)

# ---- common function for scatter / line

def _simple_plot(feds_dict, kind='line', y='pellets', bins='1H', agg='mean',
                 var='std', omit_na=False, mixed_align='raise', output='plot',
                 xaxis='auto', shadedark=None, ax=None, legend=None,
                 plot_kwargs=None, error_kwargs=None, **kwargs):
    '''Underlying method used by `line()` and `scatter()`.  Both
    these methods involve identical data processing - the only
    major difference is how they are represented.  The parameter `kind`
    handles the small differences needed.  Users should not need to
    use this function.'''

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
    feds_all = []
    for l in feds_dict.values():
        feds_all += l

    # screen issues alignment
    alignment = screen_mixed_alignment(feds_all, option=mixed_align)

    # get resample time
    origin = min(f.start_time.floor('1H') for f in feds_all)

    # compute data
    metric_obj = get_metric(y)
    metric = metric_obj.func
    metricname = metric_obj.nicename
    AGGDATA, VARDATA = _create_group_metric_df(feds_dict=feds_dict,
                                               metric=metric,
                                               agg=agg,
                                               var=var,
                                               bins=bins,
                                               origin=origin,
                                               omit_na=omit_na)

    # create return data
    if var is None or var == 'raw':
        DATA = AGGDATA
    else:
        lsuffix = f"_{agg}" if isinstance(agg, str) else "_agg"
        rsuffix = f"_{var}" if isinstance(var, str) else "_var"
        DATA = AGGDATA.join(VARDATA, how='outer', lsuffix=lsuffix, rsuffix=rsuffix)

    # update the kwargs to handle individual & general options
    plot_kwargs = {} if plot_kwargs is None else plot_kwargs
    plot_kwargs.update(kwargs) # general kwargs default to plot
    plot_kwargs = _process_plot_kwargs(plot_kwargs, feds_dict.keys())

    error_kwargs = {} if error_kwargs is None else error_kwargs
    error_kwargs = _process_plot_kwargs(error_kwargs, feds_dict.keys())

    # handle plot creation and returns
    if output in ['plot', 'data', 'both']:

        if ax is None:
            ax = plt.gca()

        if xaxis == 'auto':
            xaxis = alignment

        if xaxis == 'elapsed':
            shadedark = False

        FIG = ax.get_figure()

        # plot group level data
        for i, col in enumerate(AGGDATA.columns):

            # set kwargs for main curve plot
            this_kwargs = {}
            this_kwargs['label'] = col
            this_kwargs.update(plot_kwargs[col])

            # plot
            plotfunc(ax=ax, data=AGGDATA[col], **this_kwargs)

            # update error_kwargs, grabbing most recent color
            this_error_kwargs = {}
            this_error_kwargs['color'] = _get_most_recent_color(ax=ax, kind=kind)
            this_error_kwargs['alpha'] = 0.3 if kind == 'line' else 1
            this_error_kwargs.update(error_kwargs[col])


            # plot error - errorbar / shade
            if not VARDATA.empty:
                aggdata = AGGDATA[col]
                vardata = VARDATA[col]
                errorfunc(ax=ax, aggdata=aggdata, vardata=vardata, **this_error_kwargs)

            # plot individual lines
            if var == 'raw':

                group_feds = feds_dict[col]
                metric_df = _create_metric_df(feds_list=group_feds,
                                              metric=metric,
                                              bins=bins,
                                              origin=origin)

                for col in metric_df.columns:
                    plotfunc(ax=ax, data=metric_df[col], **this_error_kwargs)

        # axis level formatting
        shadedark = OPTIONS['default_shadedark'] if shadedark is None else shadedark
        if shadedark:
            shade_darkness(ax, DATA.index.min(), DATA.index.max(),
                           lights_on=LIGHTCYCLE['on'],
                           lights_off=LIGHTCYCLE['off'])

        legend = OPTIONS['default_legend'] if legend is None else legend
        if legend:
            ax.legend()

        FORMAT_XAXIS_OPTS[xaxis](ax, DATA.index.min(), DATA.index.max())
        ax.set_ylabel(metricname)

    return _get_return_value(FIG=FIG, DATA=DATA, output=output)

# ---- public plotting functions

def line(feds, y='pellets', bins=None, agg='mean', var='std',
         omit_na=False, mixed_align='raise', output='plot',
         xaxis='auto', shadedark=None, ax=None, legend=None,
         line_kwargs=None, error_kwargs=None, **kwargs):
    '''
    Create a line plot, with time on the x-axis and a variable
    of interest on the y-axis.

    Parameters
    ----------
    feds : FEDFrame, list-like, or dict
        FED3 data to be plotted.
        - **FEDFrame**: A single line is plotted for this object
        - **list-like**: If a collection of FEDFrames is passed,
        an individual line is plotted for every FEDFrame within `feds`
        - **dict**: If a `dict` is passed, the data are treated as being
        grouped, and average lines are plotted.  The dict should have
        group labels as keys, and FEDFrame objects as values.  Note that
        the values can be either single FEDFrame objects or list-like collections
        of them.  Though if all the values of the `dict` are single FEDFrame
        objects, the data will be treated as if there are no groups.
    y : str, optional
        Metric to plot on y-axis. See `fed3.metrics` or `fed3.metrics.list_metrics()`
        for available options.  The default is 'pellets'.
    bins : pandas time offset string, optional
        Frequency string denoting how data should be binned when plotting.
        The default is None, in which case there is no binnings.  Examples
        are '1H' for 1 hour or '15T' for 15 minutes.  When group data are passed
        (see `feds`) and `bins` is not specified, defaults to `1H`.
    agg : str or callable, optional
        Function to aggregate data from multiple FEDFrames in a group (for each
        temporal bin).  The default is 'mean'.  Only relevant when grouped
        data are being plotted.
    var : str or callable, optional
        Function to measure variation of data from multiple FEDFrames in a group
        (for each temporal bin).  The default is 'std'.  The output of this
        callable is represented as a shaded error bar around the line.
        Only relevant when grouped data are being plotted. The default is 'std'.
    omit_na : bool, optional
        When True, omits bins in a group where at least one FEDFrame has
        missing data. Only relevant when grouped data are being plotted.
        The default is False.
    mixed_align : str, optional
        Protocol when encountering FEDFrames with mixed aligment being plotted.
        The default is 'raise'.  See `fed3.core.fedfuncs.screen_mixed_alignment()`
        for options.
    output : str, optional
        Specify function behavior and return value. The default is 'plot'.
        - **plot**: Plot is created and the matplotlib Figure is returned.
        - **data**: Plot is created, and underlying processed data are returned
        (as a pandas DataFrame).
        - **both**: Plot is created, and the return value is a 2-tuple with
        the first element being the Figure, and second element being the data.
        - **dataonly**: Plot is NOT created; only the processed data are returned.
        - anything else: a `ValueError` is raised.
    xaxis : str, optional
        X-axis type to used for plotting. This is usually determined by the
        alignment of the FEDFrames, and should be handled by 'auto' (default).
        Other options are 'datetime', 'time', and 'elapsed'.
    shadedark : bool or None, optional
        When applicable based on the FEDFrame alignment, create shaded
        boxes indicating when the lights were off. The default is None,
        in which case follows `fed3.plot.OPTIONS['default_shadedark']`.
    ax : matplotlib Axes, optional
        Axes to direct the plotting to. The default is None, in which case
        `plt.gca()` is used.
    legend : bool or None, optional
        Create a legend. The default is None, in which case follows
        `fed3.plot.OPTIONS['default_legend']`.
    line_kwargs : dict-like, optional
        Dictionary for providing kwargs to matplotlib, specifically `ax.plot()`.
        - If the dictionary key corresponds to the name of a FEDFrame being plotted,
        or the name of a group of FEDFrames being plotted, then the value
        should be another dictionary mapping keyword arguments for `ax.plot()`
        to their values.
        - Otherwise, the keys are assumed to be keywords arguments for `ax.plot()`,
        and values are the argument values.  In this case, the kwargs are applied
        to all lines being plotted.
    error_kwargs : dict-like, optional
        Dictionary for providing kwargs to matplotlib, specifically `ax.fill_between()`.
        - If the dictionary key corresponds to the name of a FEDFrame being plotted,
        or the name of a group of FEDFrames being plotted, then the value
        should be another dictionary mapping keyword arguments for `ax.fill_between()`
        to their values.
        - Otherwise, the keys are assumed to be keywords arguments for `ax.fill_between()`,
        and values are the argument values.  In this case, the kwargs are applied
        to all lines being plotted.
    **kwargs : dict-like
        Passed to updated `line_kwargs`.

    Returns
    -------
    variable
        Dependent on parameter `output`.

    '''

    feds_dict = _parse_feds(feds)
    is_group = any(len(v) > 1 for v in feds_dict.values())
    bins = '1H' if is_group and bins is None else bins
    var = var if is_group else None

    return _simple_plot(kind='line',
                        feds_dict=feds_dict,
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
                        plot_kwargs=line_kwargs,
                        error_kwargs=error_kwargs,
                        **kwargs)

def scatter(feds, y='pellets', bins=None, agg='mean', var='std',
            omit_na=False, mixed_align='raise', output='plot',
            xaxis='auto', shadedark=None, ax=None, legend=None,
            point_kwargs=None, error_kwargs=None, **kwargs):

    feds_dict = _parse_feds(feds)
    is_group = any(len(v) > 1 for v in feds_dict.values())
    bins = '1H' if is_group and bins is None else bins
    var = var if is_group else None

    return _simple_plot(kind='scatter',
                        feds_dict=feds_dict,
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
                        plot_kwargs=point_kwargs,
                        error_kwargs=error_kwargs,
                        **kwargs)



