#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 17:40:10 2022

@author: earnestt1234
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from fed3.core.fedfuncs import screen_mixed_alignment

from fed3.lightcycle import LIGHTCYCLE, time_to_float

from fed3.metrics.core import get_metric
from fed3.metrics.tables import (_create_chronogram_df, _create_group_chronogram_df)

from fed3.plot import COLORCYCLE
from fed3.plot.helpers import (_get_return_value,
                               _parse_feds,
                               _raise_name_clash,
                               _process_plot_kwargs)

def chronogram_circle(feds, y='pellets', bins='1H', agg='mean', var='std',
                      mixed_align='raise', output='plot',
                      shadedark=True, ax=None, legend=True,
                      line_kwargs=None, error_kwargs=None, **kwargs):

    # parse input
    feds_dict = _parse_feds(feds)
    is_group = any(len(v) > 1 for v in feds_dict.values())
    var = var if is_group else None

    # set the outputs
    FIG = None
    DATA = pd.DataFrame()

    # setup input arguments
    feds_all = []
    for l in feds_dict.values():
        feds_all += l

    # screen issues alignment
    alignment = screen_mixed_alignment(feds_all, option=mixed_align)

    # compute data
    metric_obj = get_metric(y)
    metric = metric_obj.func
    metricname = metric_obj.nicename
    AGGDATA, VARDATA = _create_group_chronogram_df(feds=feds_dict, metric=metric, bins=bins,
                                                   agg=agg, var=var, origin_lightcycle=True,
                                                   reorder_index=True, relative_index=True)

    # create return data
    if var is None:
        DATA = AGGDATA
    else:
        lsuffix = f"_{agg}" if isinstance(agg, str) else "_agg"
        rsuffix = f"_{var}" if isinstance(var, str) else "_var"
        DATA = AGGDATA.join(VARDATA, how='outer', lsuffix=lsuffix, rsuffix=rsuffix)

    # update the kwargs to handle individual & general options
    line_kwargs = {} if line_kwargs is None else line_kwargs
    line_kwargs.update(kwargs) # general kwargs default to updatine line
    line_kwargs = _process_plot_kwargs(line_kwargs, feds_dict.keys())

    error_kwargs = {} if error_kwargs is None else error_kwargs
    error_kwargs = _process_plot_kwargs(error_kwargs, feds_dict.keys())

    # handle plot creation and returns
    if output in ['plot', 'data', 'both']:

        if ax is None:
            fig, ax = plt.subplots(subplot_kw=dict(polar=True))
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)

        FIG = ax.get_figure()

        # plot group level data
        for i, col in enumerate(AGGDATA.columns):

            # set keyword args passed
            this_kwargs = {}
            this_kwargs['color'] = COLORCYCLE[i]
            this_kwargs['label'] = col
            this_kwargs.update(line_kwargs[col])

            this_error_kwargs = {}
            this_error_kwargs['color'] = COLORCYCLE[i]
            this_error_kwargs['alpha'] = 0.3
            this_error_kwargs.update(error_kwargs[col])

            # plot
            y = AGGDATA[col]
            y = np.append(y, y[0])
            x = np.linspace(0, 2*np.pi, len(y))
            ax.plot(x, y, **this_kwargs)

            # plot error
            if not VARDATA.empty:

                y = AGGDATA[col]
                y = np.append(y, y[0])
                v = VARDATA[col]
                v = np.append(v, v[0])
                x = np.linspace(0, 2*np.pi, len(y))

                ax.fill_between(x, y-v, y+v, **this_error_kwargs)

            # plot individual lines
            if var == 'raw':

                group_feds = feds_dict[col]
                metric_df = _create_chronogram_df(feds=group_feds,
                                                  metric=metric,
                                                  bins=bins,
                                                  origin_lightcycle=True,
                                                  reorder_index=True,
                                                  relative_index=True)
                for col in metric_df.columns:
                    y = metric_df[col]
                    y = np.append(y, y[0])
                    x = np.linspace(0, 2*np.pi, len(y))
                    ax.plot(x, y, **this_error_kwargs)

        # axis level formatting
        ax.set_xlabel("Hour of Light Cycle")
        ax.set_xticks(np.linspace(0, 2*np.pi, 5))
        ax.set_xticklabels([0, 6, 12, 18, None])
        ax.set_title(metricname, pad=10)

        if shadedark:
            on, off = LIGHTCYCLE['on'], LIGHTCYCLE['off']
            on = time_to_float(on)
            off = time_to_float(off)
            off += (on > off) * 24
            start = off - on
            theta = (start / 24) * 2 * np.pi
            ax.fill_between(np.linspace(theta, 2*np.pi, 100), 0, ax.get_rmax(),
                            color='gray',alpha=.2,zorder=0,label='lights off')

        if legend:
            ax.legend()

    return _get_return_value(FIG=FIG, DATA=DATA, output=output)

def chronogram_line(feds, y='pellets', bins='15T', agg='mean', var='std',
                    mixed_align='raise', output='plot',
                    shadedark=True, ax=None, legend=True,
                    line_kwargs=None, error_kwargs=None, **kwargs):

    # parse input
    feds_dict = _parse_feds(feds)
    is_group = any(len(v) > 1 for v in feds_dict.values())
    var = var if is_group else None

    # set the outputs
    FIG = None
    DATA = pd.DataFrame()

    # setup input arguments
    feds_all = []
    for l in feds_dict.values():
        feds_all += l

    # screen issues alignment
    alignment = screen_mixed_alignment(feds_all, option=mixed_align)

    # compute data
    metric_obj = get_metric(y)
    metric = metric_obj.func
    metricname = metric_obj.nicename
    AGGDATA, VARDATA = _create_group_chronogram_df(feds=feds_dict, metric=metric, bins=bins,
                                                   agg=agg, var=var, origin_lightcycle=True,
                                                   reorder_index=True, relative_index=True)

    # create return data
    if var is None:
        DATA = AGGDATA
    else:
        lsuffix = f"_{agg}" if isinstance(agg, str) else "_agg"
        rsuffix = f"_{var}" if isinstance(var, str) else "_var"
        DATA = AGGDATA.join(VARDATA, how='outer', lsuffix=lsuffix, rsuffix=rsuffix)

    # update the kwargs to handle individual & general options
    line_kwargs = {} if line_kwargs is None else line_kwargs
    line_kwargs.update(kwargs) # general kwargs default to updatine line
    line_kwargs = _process_plot_kwargs(line_kwargs, feds_dict.keys())

    error_kwargs = {} if error_kwargs is None else error_kwargs
    error_kwargs = _process_plot_kwargs(error_kwargs, feds_dict.keys())

    # handle plot creation and returns
    if output in ['plot', 'data', 'both']:

        if ax is None:
            ax = plt.gca()

        FIG = ax.get_figure()

        # plot group level data
        for i, col in enumerate(AGGDATA.columns):

            # set keyword args passed
            this_kwargs = {}
            this_kwargs['color'] = COLORCYCLE[i]
            this_kwargs['label'] = col
            this_kwargs.update(line_kwargs[col])

            this_error_kwargs = {}
            this_error_kwargs['color'] = COLORCYCLE[i]
            this_error_kwargs['alpha'] = 0.3
            this_error_kwargs.update(error_kwargs[col])

            # plot
            y = AGGDATA[col]
            x = AGGDATA.index
            ax.plot(x, y, **this_kwargs)

            # plot error
            if not VARDATA.empty:
                y = AGGDATA[col]
                x = y.index
                v = VARDATA[col]
                ax.fill_between(x, y-v, y+v, **this_error_kwargs)

            # plot individual lines
            if var == 'raw':

                group_feds = feds_dict[col]
                metric_df = _create_chronogram_df(feds=group_feds,
                                                  metric=metric,
                                                  bins=bins,
                                                  origin_lightcycle=True,
                                                  reorder_index=True,
                                                  relative_index=True)
                for col in metric_df.columns:
                    y = metric_df[col]
                    x = y.index
                    ax.plot(x, y, **this_error_kwargs)

        # axis level formatting
        ax.set_ylabel(metricname)
        ax.set_xlabel("Hour of Light Cycle")

        ax.set_xticks([0, 6, 12, 18, 24])

        if shadedark:
            on, off = LIGHTCYCLE['on'], LIGHTCYCLE['off']
            on = time_to_float(on)
            off = time_to_float(off)
            off += (on > off) * 24
            start = off - on
            ax.axvspan(start, 24, color='gray', alpha=.2, zorder=0, label='lights off')

        if legend:
            ax.legend(bbox_to_anchor=(1,1), loc='upper left')

    return _get_return_value(FIG=FIG, DATA=DATA, output=output)

def _parse_feds_spiny_chronogram(feds, raise_name_clash=True):

    if isinstance(feds, pd.DataFrame):
        feds = [feds]

    if not isinstance(feds, dict):

        _raise_name_clash(feds) if raise_name_clash else None
        feds = {'group' : feds}

    if raise_name_clash:
        for l in feds.values():
            _raise_name_clash(l)

    if len(feds) > 1:
        raise ValueError("Spiny chronograms only plot the average values "
                         "for one group; `feds` cannot be a dict with "
                         "more than one entry.")

    return feds

def _spine_data_trick(x, y):
    newx = np.repeat(x, 3)
    newy = np.zeros(len(newx))
    newy[1::3] = y
    return newx, newy

def chronogram_spiny(feds, y='pellets', bins='15T', agg='mean',
                     mixed_align='raise', output='plot',
                     shadedark=True, ax=None, legend=True,
                     plot_quick=True, **kwargs):

    # handle parsing here, to only accept single groups
    feds_dict = _parse_feds_spiny_chronogram(feds)

    # set the outputs
    FIG = None
    DATA = pd.DataFrame()

    # setup input arguments
    feds_all = []
    for l in feds_dict.values():
        feds_all += l

    # screen issues alignment
    alignment = screen_mixed_alignment(feds_all, option=mixed_align)

    # compute data
    metric_obj = get_metric(y)
    metric = metric_obj.func
    metricname = metric_obj.nicename
    DATA, _ = _create_group_chronogram_df(feds=feds_dict, metric=metric, bins=bins,
                                          agg=agg, var=None, origin_lightcycle=True,
                                          reorder_index=True, relative_index=True)

    # handle plot creation and returns
    if output in ['plot', 'data', 'both']:

        if ax is None:
            FIG, ax = plt.subplots(subplot_kw=dict(polar=True))
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)

        FIG = ax.get_figure()

        # set keyword args passed
        kwargs['color'] = 'crimson' if not kwargs.get('color') else kwargs.get('color')

        # plot
        if plot_quick:
            y = list(DATA.iloc[:, 0]) + [0]
            x = np.linspace(0, 2*np.pi, len(y))
            x, y = _spine_data_trick(x, y)
            ax.plot(x, y, **kwargs)
        else:
            y = DATA.iloc[:, 0]
            x = np.linspace(0, 2*np.pi, len(y)+1)
            for n, val in enumerate(y):
                label = n * '_' + DATA.columns[0]
                ax.plot([0, x[n]], [0, val], label=label, **kwargs)

        # axis level formatting
        ax.set_xlabel("Hour of Light Cycle")
        ax.set_xticks(np.linspace(0, 2*np.pi, 5))
        ax.set_xticklabels([0, 6, 12, 18, None])
        ax.set_title(metricname, pad=10)

        if shadedark:
            on, off = LIGHTCYCLE['on'], LIGHTCYCLE['off']
            on = time_to_float(on)
            off = time_to_float(off)
            off += (on > off) * 24
            start = off - on
            theta = (start / 24) * 2 * np.pi
            ax.fill_between(np.linspace(theta, 2*np.pi, 100), 0, ax.get_rmax(),
                            color='gray',alpha=.2,zorder=0,label='lights off')

        if legend:
            ax.legend(bbox_to_anchor=(1,1), loc='upper left')

    return _get_return_value(FIG=FIG, DATA=DATA, output=output)