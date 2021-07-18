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

class FED(pd.DataFrame):
    _metadata = ('name', 'path', 'foreign_columns', 'missing_columns',
                 '_alignment', '_current_offset')

    @property
    def _constructor(self):
        return FED

    @property
    def mode(self):
        return self.determine_mode()

    @property
    def events(self):
        return len(self.data)

    @property
    def start_time(self):
        return pd.Timestamp(self.index.values[0])

    @property
    def end_time(self):
        return pd.Timestamp(self.index.values[-1])

    @property
    def duration(self):
        return self.end_time-self.start_time

    def _load_init(self, name=None, path=None):
        self.name = name
        self.path = path
        self.fix_column_names()
        self._handle_retrieval_time()
        self._alignment = 'datetime'
        self._current_offset = pd.Timedelta(0)

    def fix_column_names(self):
        self.foreign_columns = []
        for col in self.columns:
            for fix in fixed_cols:
                likeness = SequenceMatcher(a=col, b=fix).ratio()
                if likeness > 0.85:
                    self.rename(columns={col:fix}, inplace=True)
                    break
                self.foreign_columns.append(col)
        self.missing_columns = [col for col in needed_cols if
                                col not in self.columns]

    def determine_mode(self):
        mode = 'Unknown'
        column = pd.Series(dtype=object)
        for col in ['FR','FR_Ratio',' FR_Ratio','Mode','Session_Type']:
            if col in self.columns:
                column = self[col]
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

    def event_type(self, timestamp, poke_side=True):
        if 'Event' in self.columns:
            return self.loc[timestamp, 'Event']
        else:
            pellet = self.loc[timestamp, 'Pellet_Count'] == 0
            left = self.loc[timestamp, 'Left_Poke_Count'] == 0
            right = self.loc[timestamp, 'Right_Poke_Count'] == 0
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
        bp = self['Pellet_Count'].diff().copy()
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
        bp = self[col].diff().copy()
        if not bp.empty:
            bp.iloc[0] = int(self.event_type(bp.index[0]).lower() == side)

        return bp

    def interpellet_intervals(self, check_concat=True, only_pellet_index=False):
        bp = self.binary_pellets()
        bp = bp[bp == 1]
        diff = bp.index.to_series().diff().dt.total_seconds() / 60

        interpellet = pd.Series(np.nan, index = self.index)
        interpellet.loc[diff.index] = diff

        if check_concat and 'Concat_#' in self.columns:
            #this can't do duplicate indexes
            if not any(self.index.duplicated()):
                #thanks to this answer https://stackoverflow.com/a/47115490/13386979
                dropped = interpellet.dropna()
                pos = dropped.index.to_series().groupby(self['Concat_#']).first()
                interpellet.loc[pos[1:]] = np.nan

        if only_pellet_index:
            interpellet = interpellet.loc[bp.index]

        return interpellet

    # add alias for interpellet_intervals
    ipi = interpellet_intervals

    def correct_pokes(self):
        l = self.binary_pokes('left')
        r = self.binary_pokes('right')
        active_l = self['Active_Poke'] == 'Left'
        active_r = self['Active_Poke'] == 'Right'
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
            meals = meals.reindex(self.index)
        return meals

    def reassign_events(self, include_side=True):
        if include_side:
            events = pd.Series(np.nan, index=self.index)
            events.loc[self.binary_pellets().astype(bool)] = 'Pellet'
            events.loc[self.binary_pokes('left').astype(bool)] = 'Left'
            events.loc[self.binary_pokes('right').astype(bool)] = 'Right'
        else:
            events = np.where(self.binary_pellets(), 'Pellet', 'Poke')
        self['Event'] = events

    def _handle_retrieval_time(self):
        if 'Retrieval_Time' not in self.columns:
            return
        self['Retrieval_Time'] = pd.to_numeric(self['Retrieval_Time'], errors='coerce')

def align(fed, alignment, inplace=False):
    options = ['datetime', 'time', 'elapsed']

    if alignment not in options:
        raise ValueError(f'`alignment` must be one of {options}, '
                         f'not "{alignment}"')
    if alignment in ['none', 'datetime']:
        new_diff = fed._current_offset
    elif alignment == 'time':
        new_diff = fed.index[0].date() - zero_date.date()
    elif alignment == 'elapsed':
        new_diff = fed.index[0] - zero_date

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
    f = FED(feddata)
    f._load_init(name=name, path=path)

    return f

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


