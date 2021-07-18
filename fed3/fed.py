#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 21:16:23 2021

@author: earnestt1234
"""

from collections.abc import Iterable
from copy import deepcopy
from difflib import SequenceMatcher
import os

import numpy as np
import pandas as pd

fixed_cols = ['Device_Number',
              'Battery_Voltage',
              'Motor_Turns',
              'Session_Type',
              'Event',
              'Active_Poke',
              'Left_Poke_Count',
              'Right_Poke_Count',
              'Pellet_Count',
              'Retrieval_Time',]

needed_cols = ['Pellet_Count',
               'Left_Poke_Count',
               'Right_Poke_Count',]

data_dict = {'pellets': 'Pellet_Count',
             'left_pokes': 'Left_Poke_Count',
             'right_pokes': 'Right_Poke_Count'}

zero_date = pd.Timestamp(year=1980, month=1, day=1)

class FED:

    def __init__(self, feddata, name, add_columns=True,
                 add_columns_errors='skip', check_column_names=True):

        # identity attributes; self.path set duing `fed3.fed.load()`
        self.name = name
        self.path = None

        # load the data
        self.data = feddata
        self.foreign_columns = []
        if check_column_names:
            for col in self.data.columns:
                for fix in fixed_cols:
                    likeness = SequenceMatcher(a=col, b=fix).ratio()
                    if likeness > 0.85:
                        self.data.rename(columns={col:fix}, inplace=True)
                        break
                    self.foreign_columns.append(col)
        self.missing_columns = [col for col in needed_cols if
                                col not in self.data.columns]

        # assign other attributes
        self.mode = self.determine_mode()

        self.events = None
        self.end_time = None
        self.start_time = None
        self.duration = None
        self._set_time_attributes()

        self._alignment = 'datetime'
        self._current_offset = pd.Timedelta(0)

        # add edit / columns
        if add_columns:
            e = add_columns_errors
            self._init_add_column('Binary_Pellets', self.binary_pellets, e)
            self._init_add_column('Interpellet_Intervals', self.interpellet_intervals, e)
            self._init_add_column('Correct_Pokes', self.correct_pokes, e)
        self._handle_retrieval_time()

    def _set_time_attributes(self):
        self.events = len(self.data)
        self.end_time = pd.Timestamp(self.data.index.values[-1])
        self.start_time = pd.Timestamp(self.data.index.values[0])
        self.duration = self.end_time-self.start_time

    def __repr__(self):
        x, y = self.data.shape
        return f'FED("{self.name}", [{x} x {y}])'

    def determine_mode(self):
        mode = 'Unknown'
        column = pd.Series(dtype=object)
        for col in ['FR','FR_Ratio',' FR_Ratio','Mode','Session_Type']:
            if col in self.data.columns:
                column = self.data[col]
        if not column.empty:
            if all(isinstance(i,int) for i in column):
                if len(set(column)) == 1:
                    mode = 'FR' + str(column[0])
                else:
                    mode = 'PR'
            elif 'PR' in column[0]:
                mode = 'PR'
            else:
                mode = str(column[0])
        return mode

    def copy(self):
        return deepcopy(self)

    def event_type(self, timestamp, poke_side=True):
        if 'Event' in self.data.columns:
            return self.data.loc[timestamp, 'Event']
        else:
            pellet = self.data.loc[timestamp, 'Pellet_Count'] == 0
            left = self.data.loc[timestamp, 'Left_Poke_Count'] == 0
            right = self.data.loc[timestamp, 'Right_Poke_Count'] == 0
            if sum((pellet, left, right)) == 2:
                if pellet:
                    return 'Pellet'
                if left:
                    return 'Left' if poke_side else 'Poke'
                if right:
                    return 'Right' if poke_side else 'Poke'
            else:
                raise Exception('Cannot determine event for timestamp with '
                                'no "Event" column and multiple non-zero '
                                'entries for pellets and pokes.')

    def binary_pellets(self):
        bp = self.data['Pellet_Count'].diff().copy()
        if not bp.empty:
            bp.iloc[0] = int(self.event_type(bp.index[0]) == 'Pellet')

        return bp

    def binary_pokes(self, side='both'):
        side = side.lower()
        if side not in ['left', 'right', 'both']:
            raise ValueError('`side` must be "left", "right", or "both", '
                             f'not {side}')
        if side == 'both':
            l = self._binary_poke_for_side('left')
            r = self._binary_poke_for_side('right')
            bp = ((l == 1) | (r==1)).astype(int)

        else:
            bp = self._binary_poke_for_side(side).astype(int)

        return bp

    def _binary_poke_for_side(self, side):
        col = {'left': 'Left_Poke_Count', 'right': 'Right_Poke_Count'}[side]
        bp = self.data[col].diff().copy()
        if not bp.empty:
            bp.iloc[0] = int(self.event_type(bp.index[0]).lower() == side)

        return bp

    def interpellet_intervals(self, check_concat=True, only_pellet_index=False):
        bp = self.binary_pellets()
        bp = bp[bp == 1]
        diff = bp.index.to_series().diff().dt.total_seconds() / 60

        interpellet = pd.Series(np.nan, index = self.data.index)
        interpellet.loc[diff.index] = diff

        if check_concat and 'Concat_#' in self.data.columns:
            #this can't do duplicate indexes
            if not any(self.data.index.duplicated()):
                #thanks to this answer https://stackoverflow.com/a/47115490/13386979
                dropped = interpellet.dropna()
                pos = dropped.index.to_series().groupby(self.data['Concat_#']).first()
                interpellet.loc[pos[1:]] = np.nan

        if only_pellet_index:
            interpellet = interpellet.loc[bp.index]

        return interpellet

    # add alias for interpellet_intervals
    ipi = interpellet_intervals

    def correct_pokes(self):
        l = self.binary_pokes('left')
        r = self.binary_pokes('right')
        active_l = self.data['Active_Poke'] == 'Left'
        active_r = self.data['Active_Poke'] == 'Right'
        correct = ((l * active_l).astype(int) | (r * active_r).astype(int))

        return correct

    def meals(self, pellet_minimum=1, intermeal_interval=1, only_pellet_index=False):
        ipi = self.interpellet_intervals(only_pellet_index=True)
        within_interval = ipi < intermeal_interval
        meals = ((~within_interval).cumsum() + 1)
        above_min = meals.value_counts().sort_index() >= pellet_minimum
        replacements = above_min[above_min].cumsum().reindex(above_min.index)
        meals = meals.map(replacements)
        if not only_pellet_index:
            meals = meals.reindex(self.data.index)
        return meals

    def _init_add_column(self, colname, func, add_columns_errors):
        if add_columns_errors == 'raise':
            self.data[colname] = func()
        else:
            try:
                self.data[colname] = func()
            except:
                if add_columns_errors == 'skip':
                    return
                elif add_columns_errors == 'nan':
                    self.data[colname] = np.nan

    def reassign_events(self, include_side=True):
        if include_side:
            events = pd.Series(np.nan, index=self.data.index)
            events.loc[self.binary_pellets().astype(bool)] = 'Pellet'
            events.loc[self.binary_pokes('left').astype(bool)] = 'Left'
            events.loc[self.binary_pokes('right').astype(bool)] = 'Right'
        else:
            events = np.where(self.binary_pellets(), 'Pellet', 'Poke')
        self.data['Event'] = events

    def _handle_retrieval_time(self):
        if 'Retrieval_Time' not in self.data.columns:
            return
        self.data['Retrieval_Time'] = pd.to_numeric(self.data['Retrieval_Time'], errors='coerce')

    def remove_init_columns(self):
        added = ['Binary_Pellets', 'Interpellet_Intervals', 'Correct_Pokes']
        self.data = self.data.loc[:, ~self.data.columns.isin(added)]

def align(fed, alignment, inplace=False):
    options = ['datetime', 'time', 'elapsed']

    if alignment not in options:
        raise ValueError(f'`alignment` must be one of {options}, '
                         f'not "{alignment}"')
    if alignment in ['none', 'datetime']:
        new_diff = fed._current_offset
    elif alignment == 'time':
        new_diff = fed.data.index[0].date() - zero_date.date()
    elif alignment == 'elapsed':
        new_diff = fed.data.index[0] - zero_date

    newfed = fed if inplace else fed.copy()
    newfed.data.index -= new_diff
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


def concat(feds, name, add_concat_number=True):

    if not can_concat(feds):
        raise ValueError('FED file dates overlap, cannot concat.')

    output=[]
    offsets = {}

    sorted_feds = sorted(feds, key=lambda x: x.start_time)

    for i, fed in enumerate(sorted_feds):
        df = fed.data.copy()
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

    output = pd.concat(output)
    newfed = FED(output, name=name, add_columns=False)

    return newfed

def load(path, index_col='MM:DD:YYYY hh:mm:ss', add_columns=True,
         add_columns_errors='skip', dropna=True):
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
    f = FED(feddata, name, add_columns=add_columns,
            add_columns_errors=add_columns_errors)

    return f

def split(fed, dates, reset_columns=('Pellet_Count', 'Left_Poke_Count', 'Right_Poke_Count'),
          return_empty=False):
    dates = _split_handle_dates(dates)
    output = []
    offsets = {col: 0 for col in reset_columns}
    for i in range(len(dates[:-1])):
        start = dates[i]
        end = dates[i+1]
        subset = fed.data[start:end].copy()
        if not return_empty and subset.empty:
            continue
        if offsets:
            for col in reset_columns:
                subset[col] -= offsets[col]
                offsets[col] = subset[col].max()

        newfed = FED(subset, f"{fed.name}_{i}", add_columns=False)
        output.append(newfed)
    return output


def _split_handle_dates(dates):
    if not isinstance(dates, Iterable) or isinstance(dates, str):
        dates = [None, pd.to_datetime(dates), None]
    else:
        dates = [pd.to_datetime(date) for date in dates]
        dates = [None] + dates + [None]

    return dates


