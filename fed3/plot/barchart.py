#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 29 20:31:41 2022

@author: earnestt1234
"""

__all__ = ['bar']

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from fed3.core.fedfuncs import screen_mixed_alignment

from fed3.metrics.core import get_metric
from fed3.metrics.tables import _bar_metric_df

from fed3.plot import OPTIONS
from fed3.plot.helpers import (_get_most_recent_color,
                               _get_return_value,
                               _parse_feds,
                               _process_plot_kwargs)

def _assign_bar_positions_widths(feds_dict, positions_arg=None, position_width=0.75):

    if positions_arg is None:
        positions_arg = np.arange(len(feds_dict))

    if len(positions_arg) != len(feds_dict):
        raise ValueError('positions argument must equal the length of the input')

    positions = np.array(positions_arg, dtype='int')

    if any(np.diff(positions) > 1):
        raise ValueError("positions must be only integers with none skipped.")

    centers, counts = np.unique(positions, return_counts=True)
    bw = position_width / max(counts)

    positions = []
    bar_widths = []
    for x, c in zip(centers, counts):
        start = x - (.5 * c * bw)
        end  = x + (.5 * c * bw)
        positions += list(np.arange(start + bw/2, end, bw))
        bar_widths += [bw] * c

    return centers, positions, bar_widths

def _jitter_ys(ys, xcenter, spread):

    xs = np.random.uniform(0, spread/2, size=len(ys))
    half = int(len(ys)/2)
    xs[np.arange(len(xs)) < half] *= -1
    np.random.shuffle(xs)
    xs += xcenter
    return xs

def bar(feds, y='pellets', stat='max', normalize=None, agg='mean', var='std',
        mixed_align='raise', show_individual=False, spread=0.3, positions=None,
        position_labels=None, legend=None, ax=None, output='plot', bar_kwargs=None,
        error_kwargs=None, scatter_kwargs=None, **kwargs):

    # parse inputs
    feds_dict = _parse_feds(feds)
    not_group = all(len(f) == 1 for f in feds_dict.values())
    if not_group:
        var = None

    # set the outputs
    FIG = None
    DATA = pd.DataFrame()

    # setup input arguments
    feds_all = []
    for l in feds_dict.values():
        feds_all += l

    # screen issues alignment
    alignment = screen_mixed_alignment(feds_all, option=mixed_align)

    # compute plot data
    metric_obj = get_metric(y)
    metric = metric_obj.func
    metricname = metric_obj.nicename
    if normalize is not None:
        metricname += f' ({normalize})'
    DATA = _bar_metric_df(feds_dict, metric=metric, stat=stat,
                          normalize=normalize, agg=agg, var=var)
    individual_data = DATA.iloc[:, :-2]
    barvals = DATA.iloc[:, -2]
    errors = DATA.iloc[:, -1]

    # determine plotting order
    if position_labels is None and positions is None:
        position_labels = feds_dict.keys()
    position_width = 0.75
    centers, positions, bar_widths = _assign_bar_positions_widths(feds,
                                                                  positions,
                                                                  position_width=position_width)

    # update the kwargs to handle individual & general options
    bar_kwargs = {} if bar_kwargs is None else bar_kwargs
    bar_kwargs.update(kwargs) # general kwargs default to bar
    bar_kwargs = _process_plot_kwargs(bar_kwargs, feds_dict.keys())

    error_kwargs = {} if error_kwargs is None else error_kwargs
    error_kwargs = _process_plot_kwargs(error_kwargs, feds_dict.keys())

    scatter_kwargs = {} if scatter_kwargs is None else scatter_kwargs
    scatter_kwargs = _process_plot_kwargs(scatter_kwargs, feds_dict.keys())

    # handle plot creation and returns
    if output in ['plot', 'data', 'both']:

        if ax is None:
            ax = plt.gca()

        FIG = ax.get_figure()

        for i, label in enumerate(DATA.index):

            # set keyword args for main bar (first plotted)
            this_bar_kwargs = {'label':label,
                               'zorder':0,
                               'width': bar_widths[i]}
            this_bar_kwargs.update(bar_kwargs[label])

            # plot the bars
            x = positions[i]
            y = barvals[i]
            ax.bar(x, y, **this_bar_kwargs)

            # now set keyword args for error, grabbing most recent color
            this_error_kwargs = {'color':'grey',
                                 'ls':'none',
                                 'capsize':5,
                                 'zorder':2}
            this_error_kwargs.update(error_kwargs[label])

            this_scatter_kwargs = {'color':_get_most_recent_color(ax=ax, kind='bar'),
                                   'zorder':1,
                                   'edgecolor':'k'}
            this_scatter_kwargs.update(scatter_kwargs[label])



            # error bars
            if var is not None:
                err = errors[i]
                ax.errorbar(x=x, y=y, yerr=err, **this_error_kwargs)

            if show_individual:
                w = bar_widths[i] * spread
                ys = individual_data.iloc[i, :].dropna()
                xs = _jitter_ys(ys, x, w)
                ax.scatter(xs, ys, **this_scatter_kwargs)

        # format the axes
        ax.set_ylabel(metricname)
        ax.set_xticks(centers)
        if position_labels is not None:
            ax.set_xticklabels(position_labels)

        legend = OPTIONS['default_legend'] if legend is None else legend
        if legend:
            ax.legend()

    # output was weird for lists without this step -
    # treated each single FED as group, and created
    # a DF with lots of unhelpful info
    if not_group:
        DATA = DATA.drop(DATA.index, axis=1)
        DATA = DATA.iloc[:, :-1]

    return _get_return_value(FIG=FIG, DATA=DATA, output=output)
