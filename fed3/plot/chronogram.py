#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 17:40:10 2022

@author: earnestt1234
"""

import matplotlib.pyplot as plt
import pandas as pd

from fed3.fedframe.fedfuncs import screen_mixed_alignment

from fed3.lightcycle import LIGHTCYCLE

from fed3.metrics.core import (_get_metric, _get_metricname,)
from fed3.metrics.tables import (_create_chronogram_df, _create_group_chronogram_df)

from fed3.plot import COLORCYCLE
from fed3.plot.helpers import (_get_return_value, _handle_feds, _parse_feds)

def chronogram_line(feds, y='pellets', bins='1H', agg='mean', var='std',
                    mixed_align='raise', output='plot',
                    shadedark=True, ax=None, legend=True,
                    line_kwargs=None, **kwargs):

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
    metric = _get_metric(y)
    metricname = _get_metricname(y)
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

    # handle plot creation and returns
    if output in ['plot', 'data', 'both']:

        line_kwargs = {} if line_kwargs is None else line_kwargs

        if ax is None:
            ax = plt.gca()

        # plot group level data
        for i, col in enumerate(AGGDATA.columns):

            # set keyword args passed
            plot_kwargs = kwargs.copy()
            color = (COLORCYCLE[i] if not plot_kwargs.get("color") else plot_kwargs.get("color"))
            plot_kwargs['color'] = color
            plot_kwargs['label'] = col

            if line_kwargs.get(col):
                plot_kwargs.update(line_kwargs[col])

            # plot
            y = AGGDATA[col]
            x = AGGDATA.index
            ax.plot(x, y, **plot_kwargs)

            # plot error
            if not VARDATA.empty:
                y = AGGDATA[col]
                x = y.index
                v = VARDATA[col]
                ax.fill_between(x, y-v, y+v, color=color, alpha=.3)

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
                    ax.plot(x, y, alpha=.3, label='', color=color)

        # axis level formatting
        ax.set_ylabel(metricname)
        ax.set_xlabel("Hour of Light Cycle")

        ax.set_xticks([0, 6, 12, 18, 24])

        if shadedark:
            on, off = LIGHTCYCLE['on'], LIGHTCYCLE['off']
            off += (on > off) * 24
            start = off - on
            ax.axvspan(start, 24, color='gray', alpha=.2, zorder=0, label='lights off')

        if legend:
            ax.legend()

    return _get_return_value(FIG=FIG, DATA=DATA, output=output)
