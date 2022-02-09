#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 12:34:52 2022

@author: earnestt1234
"""

import pandas as pd

from fed3.metrics import METRICS, METRICNAMES

def _create_metric_df(feds, metric):
    df = pd.DataFrame()
    for fed in feds:
        y = metric(fed)
        y.name = fed.name
        df = df.join(y, how='outer')

    return df

def _get_metric(y):
    if isinstance(y, str):

        key = y.lower()
        try:
            return METRICS[key]
        except KeyError:
            raise ValueError(f'y-value "{y}" is not recognized.')

    else:
        return y

def _get_metricname(y):

    if isinstance(y, str):

        key = y.lower()
        try:
            return METRICNAMES[key]
        except KeyError:
            raise ValueError(f'y-value "{y}" is not recognized.')

    else:
        return y.__name__

def _get_return_value(FIG, DATA, output):

    if output == 'plot':
        return FIG

    elif output in ['dataonly', 'data']:
        return DATA

    elif output == 'both':
        return FIG, DATA

    else:
        raise ValueError(f'output value "{output}" not recognized.')

def _handle_feds(feds):
    if isinstance(feds, pd.DataFrame):
        feds = [feds]
    return feds