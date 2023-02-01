#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. include:: ../../docs/plots_barchart.md
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
    '''Determine placement of bars from a dicionary of FEDs to be plotted.'''

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
    '''Create jitter in x for raw data being plotted in a bar chart.'''

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
    '''
    Create a vertical bar chart.

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
    stat : str or callable, optional
        Function used to collapse time series data to a point value.
        The default is 'max'.  With `y='pellets'`, the maximum of the pellet
        count is plotted.  Other common options would be 'mean' or
        'median'.
    normalize : str, optional
        Normalize the values plotted to a time window. The default is None,
        in which case no normalization is done.  For example, using '1H'
        would divide the metric being plotted by the number of hours of
        the FEDFrame.
    agg : str or callable, optional
        How to aggregate the point values being plotted from different FEDs
        when grouping data. The default is 'mean'.  Only relevant when
        grouped data are being plotted.
    var : str or callable, optional
        How to show the variation around the bar.  The default is 'std'.
    mixed_align : str, optional
        Protocol when encountering FEDFrames with mixed aligment being plotted.
        The default is 'raise'.  See `fed3.core.fedfuncs.screen_mixed_alignment()`
        for options.
    show_individual : bool, optional
        When grouping data, show each individual FED's data as a point floating
        around the bar. The default is False.
    spread : float, optional
        Parameter for controling the spread of points when using `show_individual`.
        The default is 0.3.
    positions : list of int, optional
        List of integers which can be used to determine the position & grouping
        of bars being plotted. The default is None.  Positions should have a length
        equal to the number of bars, and should only contain ascending integers.
        Bars with the same integer label will be grouped side by side.  For example,
        a group of 4 bars could be grouped into sets of 2 with
        `positions=[0, 0, 1, 1]`.  `positions=[0, 1, 2, 3]` would evenly
        space bars (this is the default behavior, set when `None` is passed.)
    position_labels : list of str, optional
        Labels for each position of bars being plotted. The default is None.
    legend : bool or None, optional
        Create a legend. The default is None, in which case follows
        `fed3.plot.OPTIONS['default_legend']`.
    ax : matplotlib Axes, optional
        Axes to direct the plotting to. The default is None, in which case
        `plt.gca()` is used.
    output : str, optional
        Specify function behavior and return value. The default is 'plot'.

        - **plot**: Plot is created and the matplotlib Figure is returned.
        - **data**: Plot is created, and underlying processed data are returned
        (as a pandas DataFrame).
        - **both**: Plot is created, and the return value is a 2-tuple with
        the first element being the Figure, and second element being the data.
        - **dataonly**: Plot is NOT created; only the processed data are returned.
        - anything else: a `ValueError` is raised.

    bar_kwargs : dict-like, optional
        Dictionary for providing kwargs to matplotlib, specifically `ax.bar()`.

        - If the dictionary key corresponds to the name of a FEDFrame being plotted,
        or the name of a group of FEDFrames being plotted, then the value
        should be another dictionary mapping keyword arguments for `ax.bar()`
        to their values.
        - Otherwise, the keys are assumed to be keywords arguments for `ax.bar()`,
        and values are the argument values.  In this case, the kwargs are applied
        to all lines being plotted.

    error_kwargs : dict-like, optional
        Dictionary for providing kwargs to matplotlib, specifically `ax.errorbar()`.

        - If the dictionary key corresponds to the name of a FEDFrame being plotted,
        or the name of a group of FEDFrames being plotted, then the value
        should be another dictionary mapping keyword arguments for `ax.errorbar()`
        to their values.
        - Otherwise, the keys are assumed to be keywords arguments for `ax.errorbar()`,
        and values are the argument values.  In this case, the kwargs are applied
        to all lines being plotted.

    scatter_kwargs : dict-like, optional
        Dictionary for providing kwargs to matplotlib, specifically `ax.scatter()`.

        - If the dictionary key corresponds to the name of a FEDFrame being plotted,
        or the name of a group of FEDFrames being plotted, then the value
        should be another dictionary mapping keyword arguments for `ax.scatter()`
        to their values.
        - Otherwise, the keys are assumed to be keywords arguments for `ax.scatter()`,
        and values are the argument values.  In this case, the kwargs are applied
        to all lines being plotted.
    **kwargs : dict-like
        Keyword arguments passed to `ax.bar()`.

    Returns
    -------
    variable
        Dependent on parameter `output`.

    '''

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
