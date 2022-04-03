#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 22:13:44 2022

@author: earnestt1234
"""

import pandas as pd

def _create_metric_df(feds, metric, bins=None, origin='start'):
    df = pd.DataFrame()
    for fed in feds:
        y = metric(fed, bins=bins, origin=origin)
        y.name = fed.name
        df = df.join(y, how='outer')

    return df

def _create_group_metric_df(feds, metric, agg='mean', var='std', bins='1H',
                            origin='start', omit_na=False):
    all_agg = pd.DataFrame()
    all_var = pd.DataFrame()
    for group, fedlist in feds.items():
        fed_values = pd.DataFrame()
        for fed in fedlist:
            y = metric(fed, bins=bins, origin=origin)
            y.name = fed.name
            fed_values = fed_values.join(y, how='outer')
        if omit_na:
            fed_values = fed_values.dropna()
        group_agg = fed_values.agg(agg, axis=1)
        group_var = fed_values.agg(var, axis=1)
        group_agg.name = group
        group_var.name = group
        all_agg = all_agg.join(group_agg, how='outer')
        all_var = all_var.join(group_var, how='outer')

    return all_agg, all_var