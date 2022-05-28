#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  9 15:26:30 2021

@author: earnestt1234
"""

from fed3.lightcycle import lightcycle_tuples

def shade_darkness(ax, min_date, max_date, lights_on, lights_off):
    """
    Shade the night periods of a matplotlib Axes with a datetime x-axis.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Plot Axes.
    min_date : datetime
        Earliest date to shade.
    max_date : datetime
        Latest date to shade.
    lights_on : int
        Integer between 0 and 23 representing when the light cycle begins.
    lights_off : int
        Integer between 0 and 23 representing when the light cycle ends.

    Returns
    -------
    None.
    """

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