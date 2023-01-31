#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  9 15:26:30 2021

@author: earnestt1234
"""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from fed3.lightcycle import lightcycle_tuples, LIGHTCYCLE

def shade_darkness(ax=None, min_date=None, max_date=None, lights_on=None, lights_off=None):
    '''
    Shade the night time periods with vertical bars on a datetime x-axis.

    Parameters
    ----------
    ax : matplotlib.axes.Axes, optional
        Axes to shade. The default is None, in which case uses `plt.gca()`.
    min_date : datetime, optional
        Earliest date to shade. The default is None, in which case is inferred
        from axis.
    max_date : TYPE, optional
        Latest date to shade. The default is None, in which case is inferred
        from axis.
    lights_on : datetime.time, optional
        Time indicating beginning of light cycle. The default is None, in
        which case `fed3.lightcycle.LIGHTCYCLE` is used.
    lights_off : datetime.time, optional
        Time indicating beginning of light cycle. The default is None, in
        which case `fed3.lightcycle.LIGHTCYCLE` is used.

    Returns
    -------
    None.

    '''

    if ax is None:
        ax = plt.gca()

    if min_date is None:
        min_date, _ = mdates.num2date(ax.get_xlim())

    if max_date is None:
        _, max_date = mdates.num2date(ax.get_xlim())

    if lights_on is None:
        lights_on = LIGHTCYCLE['on']

    if lights_off is None:
        lights_off = LIGHTCYCLE['off']

    nights = lightcycle_tuples(start_date=min_date,
                               end_date=max_date,
                               lights_on=lights_on,
                               lights_off=lights_off,
                               kind='nights')

    for i, (start, end) in enumerate(nights):
        ax.axvspan(start,
                   end,
                   color='gray',
                   alpha=.2,
                   label='_'*i + 'lights off',
                   zorder=0)
