#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 17:40:10 2022

@author: earnestt1234
"""

import pandas as pd

from fed3.fedframe.fedfuncs import screen_mixed_alignment

from fed3.metrics.core import (_get_metric, _get_metricname,)
from fed3.metrics.tables import (_create_group_metric_df,  _create_metric_df,)

from fed3.plot.helpers import (_get_return_value, _handle_feds,)

# def _chronogram_singles(feds, kind='line', y='pellets', bins=None,
#                         mixed_align='raise', output='plot',
#                         xaxis='auto', shadedark=True, ax=None, legend=True,
#                         line_kwargs=None, **kwargs):

#     FIG = None
#     DATA = pd.DataFrame()

#     # handle arguments
#     feds = _handle_feds(feds)
#     alignment = screen_mixed_alignment(feds, option=mixed_align)

#     # compute data
#     metric = _get_metric(y)
#     metricname = _get_metricname(y)
#     DATA = _create_metric_df(feds=feds, metric=metric, bins=bins)

# def chronogram_line(feds, kind='line', y='pellets', bins=None,
#                     mixed_align='raise', output='plot',
#                     xaxis='auto', shadedark=True, ax=None, legend=True,
#                     line_kwargs=None, **kwargs):
