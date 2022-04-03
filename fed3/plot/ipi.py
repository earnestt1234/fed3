#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 12:38:40 2022

@author: earnestt1234
"""

import matplotlib.pyplot as plt
import pandas as pd

from fed3.fedframe.fedfuncs import screen_mixed_alignment

from fed3.plot.generic import (plot_hist_data)

from fed3.metrics.tables import (_create_metric_df)

from fed3.metrics.core import (_get_metric, _get_metricname,)

from fed3.plot.helpers import (_get_return_value,
                               _handle_feds,)

def ipi(feds, logx=True, kde=True, mixed_align='raise', output='plot',
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