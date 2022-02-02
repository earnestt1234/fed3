#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 22:40:51 2022

@author: earnestt1234
"""

from collections.abc import Iterable
import os

import pandas as pd

from fed3.fedframe import FEDFrame

ZERO_DATE = pd.Timestamp(year=1980, month=1, day=1)

def align(fed, alignment, inplace=False):
    options = ['datetime', 'time', 'elapsed']

    if alignment not in options:
        raise ValueError(f'`alignment` must be one of {options}, '
                         f'not "{alignment}"')
    if alignment in ['none', 'datetime']:
        new_diff = fed._current_offset
    elif alignment == 'time':
        new_diff = fed.index[0].date() - ZERO_DATE.date()
    elif alignment == 'elapsed':
        new_diff = fed.index[0] - ZERO_DATE

    newfed = fed if inplace else fed.copy()
    newfed.index -= new_diff
    newfed._current_offset -= new_diff
    newfed._alignment = alignment

    return newfed

def can_concat(feds):
    """
    Determines whether or not FED3_Files can be concatenated, (based on whether
    their start and end times overlap).

    Parameters
    ----------
    feds : array
        an array of FED3_Files

    Returns
    -------
    bool

    """
    sorted_feds = sorted(feds, key=lambda x: x.start_time)
    for i, file in enumerate(sorted_feds[1:], start=1):
        if file.start_time <= sorted_feds[i-1].end_time:
            return False
    return True

def concat(feds, name=None, add_concat_number=True):

    if name is None:
        name = feds[0].name

    if not can_concat(feds):
        raise ValueError('FED file dates overlap, cannot concat.')

    output=[]
    offsets = {}

    sorted_feds = sorted(feds, key=lambda x: x.start_time)

    for i, fed in enumerate(sorted_feds):
        df = fed.copy()
        if add_concat_number:
            df['Concat_#'] = i

        if i==0:
            for col in['Pellet_Count', 'Left_Poke_Count','Right_Poke_Count']:
                if col in df.columns:
                    offsets[col] = df[col].max()

        else:
            for col, offset in offsets.items():
                df[col] += offset
                offsets[col] = df[col].max()

        output.append(df)

    newfed = pd.concat(output)
    newfed._load_init(name=name)

    return newfed

def determine_alignment(feds):
    alignments = set(f._alignment for f in feds)
    return 'mixed' if len(alignments) > 1 else list(alignments)[0]

def load(path, index_col='MM:DD:YYYY hh:mm:ss', dropna=True):
    # read the path
    name, ext = os.path.splitext(path)
    ext = ext.lower()

    read_opts = {'.csv':pd.read_csv, '.xlsx':pd.read_excel}
    func = read_opts[ext]
    feddata = func(path,
                   parse_dates=True,
                   index_col=index_col)
    if dropna:
        feddata = feddata.dropna(how='all')

    name = os.path.basename(name)
    f = FEDFrame(feddata)
    f._load_init(name=name, path=path)

    return f

def screen_mixed_alignment(feds, option='raise'):
    alignment = determine_alignment(feds)
    if alignment != 'mixed':
        return True
    if option == 'raise':
        raise ValueError('The passed feds have mixed alignment; '
                         'you can either align them with the `align` argument '
                         'or force plotting by setting the `mixed_align` argument.')
    elif option == 'warn':
        print("PLACE A REAL WARNING HERE")
    elif option != 'ignore':
        raise ValueError('Mixed alignment option must be "ignore", "warn", or "raise"')

def split(fed, dates, reset_columns=('Pellet_Count', 'Left_Poke_Count', 'Right_Poke_Count'),
          return_empty=False):
    dates = _split_handle_dates(dates)
    output = []
    offsets = {col: 0 for col in reset_columns}
    for i in range(len(dates[:-1])):
        start = dates[i]
        end = dates[i+1]
        subset = fed[(fed.index >= start) &
                     (fed.index < end)].copy()
        if not return_empty and subset.empty:
            continue
        if offsets:
            for col in reset_columns:
                subset[col] -= offsets[col]
                offsets[col] = subset[col].max()
        output.append(subset)
    return output


def _split_handle_dates(dates):
    old = pd.Timestamp('01-01-1970')
    future = pd.Timestamp('12-31-2200')
    if not isinstance(dates, Iterable) or isinstance(dates, str):
        dates = [old, pd.to_datetime(dates), future]
    else:
        dates = [pd.to_datetime(date) for date in dates]
        dates = [old] + dates + [future]

    return dates