#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 22:13:44 2022

@author: earnestt1234
"""

import numpy as np
import pandas as pd

from fed3.lightcycle import LIGHTCYCLE, time_to_float

def _bar_metric_df(feds_dict, metric, stat, normalize=None, agg='mean', var='std', dropna=True):

    agg_key = f"total.{agg}"
    var_key = f"total.{var}"

    normalize = pd.to_timedelta(normalize) if normalize is not None else None

    rows = []

    for group, feds in feds_dict.items():

        row = {}
        aggregate = None
        variation = None

        tbl = _create_metric_df(feds, metric)

        for col in tbl.columns:
            vals = tbl[col]
            if dropna:
                vals = vals.dropna()

            v = vals.agg(stat)
            if normalize is not None:
                factor = (vals.index.max() - vals.index.min()) / normalize
                v /= factor

            row[col] = v


        as_series = pd.Series(row)
        aggregate = as_series.agg(agg)
        variation = as_series.agg(var) if var is not None else np.nan
        row[agg_key] = aggregate
        row[var_key] = variation

        rows.append(row)

    last2 = [agg_key, var_key]
    out = pd.DataFrame(rows, index=feds_dict.keys())
    out = out.loc[:, [c for c in out.columns if c not in last2] + last2]

    return out

def _create_chronogram_df(feds_list, metric, bins='1H', origin_lightcycle=True,
                          reorder_index=True, relative_index=True):

    on = LIGHTCYCLE['on']
    on_f = time_to_float(on)
    t = pd.to_timedelta(bins)
    n = pd.to_timedelta('24H') / t
    rem = n % 1

    if rem != 0:
        raise ValueError("bins must evenly divide 24 hours.")

    if origin_lightcycle:
        origin = pd.Timestamp(year=1970, month=1, day=1, hour=on.hour, minute=on.minute)
    else:
        origin = 'start_day'

    metric_df = _create_metric_df(feds_list, metric=metric, bins=bins, origin=origin)
    bytime = metric_df.groupby(metric_df.index.time).mean()

    # handle reindexing things
    float_index = np.array([x.hour + x.minute / 60 for x in bytime.index.values])

    # orders so that the start of the light cycle is first
    if reorder_index:
        idx = (float_index < on_f).argsort(kind='stable')
        bytime = bytime.iloc[idx]
        float_index = float_index[idx]

    # replaces times with hours since lights on
    if relative_index:
        post_lights_on = np.where(float_index < on_f, float_index + 24, float_index)
        post_lights_on -= on_f
        bytime.index = post_lights_on.round(4)

    return bytime

def _create_group_chronogram_df(feds_dict, metric, agg='mean', var='std', bins='1H',
                                omit_na=False, origin_lightcycle=True,
                                reorder_index=True, relative_index=True):
    all_agg = pd.DataFrame()
    all_var = pd.DataFrame()
    for group, fedlist in feds_dict.items():
        metric_df = _create_chronogram_df(fedlist, metric=metric, bins=bins,
                                          origin_lightcycle=origin_lightcycle,
                                          reorder_index=reorder_index,
                                          relative_index=relative_index)
        if omit_na:
            metric_df = metric_df.dropna()

        group_agg = metric_df.agg(agg, axis=1)
        group_agg.name = group

        if var is None or var == 'raw':
            group_var = pd.Series(dtype='float64')
        else:
            group_var = metric_df.agg(var, axis=1)
        group_var.name = group

        all_agg = all_agg.join(group_agg, how='outer')
        all_var = all_var.join(group_var, how='outer')

    return all_agg, all_var


def _create_group_metric_df(feds_dict, metric, agg='mean', var='std', bins='1H',
                            origin='start', omit_na=False):
    all_agg = pd.DataFrame()
    all_var = pd.DataFrame()
    for group, fedlist in feds_dict.items():
        metric_df = _create_metric_df(fedlist, metric=metric, bins=bins, origin=origin)
        if omit_na:
            metric_df = metric_df.dropna()

        group_agg = metric_df.agg(agg, axis=1)
        group_agg.name = group

        if var is None or var == 'raw':
            group_var = pd.Series(dtype='float64')
        else:
            group_var = metric_df.agg(var, axis=1)
        group_var.name = group

        all_agg = all_agg.join(group_agg, how='outer')
        all_var = all_var.join(group_var, how='outer')

    return all_agg, all_var

def _create_metric_df(feds_list, metric, bins=None, origin='start'):
    df = pd.DataFrame()
    for fed in feds_list:
        y = metric(fed, bins=bins, origin=origin)
        y.name = getattr(fed, '_plot_name', fed.name)
        df = df.join(y, how='outer')

    return df

def _stack_group_values(metric_df, feds_dict):

    series = []

    for group, feds in feds_dict.items():

        group_vals = []

        for fed in feds:

            name = getattr(fed, '_plot_name', fed.name)
            vals = metric_df[name].dropna().to_list()
            group_vals += vals

        series.append(pd.Series(group_vals, name=group))

    output = pd.concat(series, axis=1)

    return output

