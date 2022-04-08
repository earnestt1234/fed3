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
from fed3.metrics.tables import (_chronogram_df)

from fed3.plot import COLORCYCLE
from fed3.plot.helpers import (_get_return_value, _handle_feds,)

def _line_chronogram_single(feds, y='pellets', bins='1H',
                            mixed_align='raise', output='plot',
                            shadedark=True, ax=None, legend=True,
                            line_kwargs=None, **kwargs):

    FIG = None
    DATA = pd.DataFrame()

    # handle arguments
    feds = _handle_feds(feds)
    alignment = screen_mixed_alignment(feds, option=mixed_align)

    # compute data
    metric = _get_metric(y)
    metricname = _get_metricname(y)
    DATA = _chronogram_df(feds=feds, metric=metric, bins=bins,
                          origin_lightcycle=True, reorder_index=True,
                          relative_index=True)

    # handle plot creation and returns
    if output in ['plot', 'data', 'both']:

        line_kwargs = {} if line_kwargs is None else line_kwargs

        if ax is None:
            ax = plt.gca()

        for i, col in enumerate(DATA.columns):

            # set keyword args passed
            plot_kwargs = kwargs.copy()
            plot_kwargs['color'] = (COLORCYCLE[i] if not plot_kwargs.get("color")
                                    else plot_kwargs.get("color"))
            plot_kwargs['label'] = col

            if line_kwargs.get(col):
                plot_kwargs.update(line_kwargs[col])

            # plot
            y = DATA[col]
            x = DATA.index
            ax.plot(x, y, **plot_kwargs)

        # axis level formatting
        ax.set_ylabel(metricname)
        ax.set_xlabel("Hours (relative to light cycle)")

        if shadedark:
            on, off = LIGHTCYCLE['on'], LIGHTCYCLE['off']

        if legend:
            ax.legend()

        FIG = ax.get_figure()

    return _get_return_value(FIG=FIG, DATA=DATA, output=output)

def chronogram_line(feds, y='pellets', mixed_align='raise', output='plot',
                    xaxis='auto', shadedark=True, ax=None, legend=True,
                    line_kwargs=None, **kwargs):

    if isinstance(feds, dict):
        raise NotImplemented

    else:
        _line_chronogram_single(feds=feds, y=y, mixed_align=mixed_align,
                                output=output, shadedark=shadedark, ax=ax,
                                legend=legend, line_kwargs=line_kwargs, **kwargs)
