#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 21:16:23 2021

@author: earnestt1234
"""

from difflib import SequenceMatcher

import numpy as np
import pandas as pd

FIXED_COLS = ['Device_Number',
              'Battery_Voltage',
              'Motor_Turns',
              'Session_Type',
              'Event',
              'Active_Poke',
              'Left_Poke_Count',
              'Right_Poke_Count',
              'Pellet_Count',
              'Retrieval_Time',]

NEEDED_COLS = ['Pellet_Count',
               'Left_Poke_Count',
               'Right_Poke_Count',]

def _filterout(series, dropna=False, dropzero=False, deduplicate=False):

    """Helper func for condensing series returned from FEDFrame methods."""

    if dropna:
        series = series.dropna()
    if dropzero:
        series = series[series != 0]
    if deduplicate:
        series = series[~series.duplicated()]

    return series

class FEDFrame(pd.DataFrame):
    _metadata = ['name', 'path', 'foreign_columns', 'missing_columns',
                 '_alignment', '_current_offset']

    # ---- Properties

    @property
    def _constructor(self):
        return FEDFrame

    @property
    def duration(self):
        return self.end_time-self.start_time

    @property
    def end_time(self):
        return pd.Timestamp(self.index.values[-1])

    @property
    def events(self):
        return len(self.data)

    @property
    def mode(self):
        return self.determine_mode()

    @property
    def start_time(self):
        return pd.Timestamp(self.index.values[0])

    # ---- "Private"

    def _binary_correct_pokes(self):
        l = self._binary_pokes('left')
        r = self._binary_pokes('right')
        active_l = self['Active_Poke'] == 'Left'
        active_r = self['Active_Poke'] == 'Right'
        correct = ((l * active_l).astype(int) | (r * active_r).astype(int))

        return correct

    def _binary_error_pokes(self):
        l = self._binary_pokes('left')
        r = self._binary_pokes('right')
        active_l = self['Active_Poke'] == 'Left'
        active_r = self['Active_Poke'] == 'Right'
        error = ((l * active_r).astype(int) | (r * active_l).astype(int))

        return error

    def _binary_pellets(self):
        bp = self['Pellet_Count'].diff().copy()
        if not bp.empty:
            bp.iloc[0] = int(self.event_type(bp.index[0]) == 'Pellet')

        return bp

    def _binary_poke_for_side(self, side):
        col = {'left': 'Left_Poke_Count', 'right': 'Right_Poke_Count'}[side]
        bp = self[col].diff().copy()
        if not bp.empty:
            bp.iloc[0] = int(self.event_type(bp.index[0]).lower() == side)

        return bp

    def _binary_pokes(self, kind='any'):
        kind = kind.lower()
        kinds = ['left', 'right', 'any', 'correct', 'error']
        if kind not in kinds:
            raise ValueError(f'`kind` must be one of  {kinds}, not {kind}')

        if kind == 'any':
            l = self._binary_poke_for_side('left')
            r = self._binary_poke_for_side('right')
            bp = ((l == 1) | (r==1)).astype(int)

        elif kind in ['left', 'right']:
            bp = self._binary_poke_for_side(kind).astype(int)

        elif kind in ['correct', 'error']:
            bp = self._binary_correct_pokes() if kind == 'correct' else self._binary_error_pokes()

        return bp

    def _cumulative_poke_for_side(self, side):
        col = {'left': 'Left_Poke_Count', 'right': 'Right_Poke_Count'}[side]
        cp = self[col]

        return cp

    def _cumulative_pokes(self, kind='any'):
        kind = kind.lower()
        kinds = ['left', 'right', 'any', 'correct', 'error']
        if kind not in kinds:
            raise ValueError(f'`kind` must be one of  {kinds}, not {kind}')

        if kind == 'any':
            l = self._cumulative_poke_for_side('left')
            r = self._cumulative_poke_for_side('right')
            cp = (l + r).astype(int)

        elif kind in ['left', 'right']:
            cp = self._cumulative_poke_for_side(kind).astype(int)

        elif kind in ['correct', 'error']:
            bp = self._binary_correct_pokes() if kind == 'correct' else self._binary_error_pokes()
            cp = bp.cumsum()

        return cp

    def _handle_retrieval_time(self):
        if 'Retrieval_Time' not in self.columns:
            return
        self['Retrieval_Time'] = pd.to_numeric(self['Retrieval_Time'], errors='coerce')


    def _load_init(self, name=None, path=None):
        self.name = name
        self.path = path
        self.fix_column_names()
        self._handle_retrieval_time()
        self._alignment = 'datetime'
        self._current_offset = pd.Timedelta(0)

    # ---- Public

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

    def fix_column_names(self):
        self.foreign_columns = []
        for col in self.columns:
            for fix in FIXED_COLS:
                likeness = SequenceMatcher(a=col, b=fix).ratio()
                if likeness > 0.85:
                    self.rename(columns={col:fix}, inplace=True)
                    break
                self.foreign_columns.append(col)
        self.missing_columns = [col for col in NEEDED_COLS if
                                col not in self.columns]

    def interpellet_intervals(self, check_concat=True, condense=False):
        bp = self._binary_pellets()
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

        if condense:
            interpellet = interpellet.loc[bp.index]
            interpellet = _filterout(interpellet, dropna=True)

        return interpellet

    def meals(self, pellet_minimum=1, intermeal_interval=1, condense=False):
        ipi = self.interpellet_intervals(condense=True)
        within_interval = ipi < intermeal_interval
        meals = ((~within_interval).cumsum() + 1)
        above_min = meals.value_counts().sort_index() >= pellet_minimum
        replacements = above_min[above_min].cumsum().reindex(above_min.index)
        meals = meals.map(replacements)
        if not condense:
            meals = meals.reindex(self.index)
        return meals

    def pellets(self, cumulative=True, condense=False):

        if cumulative:
            y = self['Pellet_Count']
            if condense:
                y = _filterout(y, deduplicate=True, dropzero=True)

        else:
            y = self._binary_pellets()
            if condense:
                y = _filterout(y, dropzero=True)

        return y

    def pokes(self, kind='any', cumulative=True, condense=False):

        kind = kind.lower()
        kinds = ['left', 'right', 'any', 'correct', 'error']
        if kind not in kinds:
            raise ValueError(f'`kind` must be one of  {kinds}, not {kind}')

        if cumulative:
            y = self._cumulative_pokes(kind)
            if condense:
                y = _filterout(y, deduplicate=True, dropzero=True)

        else:
            y = self._binary_pokes(kind)
            if condense:
                y = _filterout(y, dropzero=True)

        return y

    def reassign_events(self, include_side=True):
        if include_side:
            events = pd.Series(np.nan, index=self.index)
            events.loc[self._binary_pellets().astype(bool)] = 'Pellet'
            events.loc[self._binary_pokes('left').astype(bool)] = 'Left'
            events.loc[self._binary_pokes('right').astype(bool)] = 'Right'
        else:
            events = np.where(self._binary_pellets(), 'Pellet', 'Poke')
        self['Event'] = events

    # ---- Aliases
    ipi = interpellet_intervals

