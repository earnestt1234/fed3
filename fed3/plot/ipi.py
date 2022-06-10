#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 12:38:40 2022

@author: earnestt1234
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from fed3.core.fedfuncs import screen_mixed_alignment

from fed3.metrics.core import get_metric
from fed3.metrics.tables import (_create_metric_df,
                                 _stack_group_values)

from fed3.plot.helpers import (_get_return_value, _parse_feds)

def _plot_hist_data(ax, data, logx, kde, legend=True, **kwargs):

    data = pd.melt(data,
                   value_vars=data.columns,
                   var_name="FED",
                   value_name='ipi').dropna()

    sns.histplot(data=data, x='ipi', hue='FED', log_scale=logx, kde=kde,
                 legend=legend, **kwargs)

    return ax.get_figure()

def ipi(feds, logx=True, kde=True, mixed_align='raise', output='plot',
        ax=None, legend=True, **kwargs):

    # set the outputs
    FIG = None
    DATA = pd.DataFrame()

    # setup input arguments
    feds_dict = _parse_feds(feds)
    is_group = any(len(v) > 1 for v in feds_dict.values())
    feds_all = []
    for l in feds_dict.values():
        feds_all += l

    # screen issues alignment
    alignment = screen_mixed_alignment(feds_all, option=mixed_align)

    # compute data for individual feds
    y = 'ipi'
    metric_obj = get_metric(y)
    metric = metric_obj.func
    metricname = metric_obj.nicename
    DATA = _create_metric_df(feds=feds_all, metric=metric)
    if is_group:
        DATA = _stack_group_values(DATA, feds_dict)

    # handle plot creation and returns
    if output in ['plot', 'data', 'both']:

        if ax is None:
            ax = plt.gca()

        FIG = _plot_hist_data(ax=ax,
                              data=DATA,
                              logx=logx,
                              kde=kde,
                              legend=legend,
                              **kwargs)

        ax.set_xlabel(metricname)

    return _get_return_value(FIG=FIG, DATA=DATA, output=output)

