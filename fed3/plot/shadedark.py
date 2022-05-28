#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  9 15:26:30 2021

@author: earnestt1234
"""

# from fed3.lightcycle import (hours_between, night_intervals)

def is_at_night(datetime, lights_on, lights_off):

    ashour = datetime.hour + (1/60) * datetime.minute
    if lights_on > lights_off:
        return (lights_off <= ashour < lights_on)
    else:
        return (ashour < lights_on or ashour >= lights_off)

def nighttime_intervals(start_date, end_date, lights_on, lights_off):

    result = []
    pair = []

    if is_at_night(start_date):
        pair.append(start_date)
    else:
        first_night = start_date.replace(hour=lights_on)
        first_night += pd.Timedelta('24H') * (first_night < start_date)
        pair.append(first_night)


def shade_darkness(ax, min_date, max_date, lights_on, lights_off,
                   convert=True):
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
    convert : bool, optional
        Whether to convert the start/end arguments from numpy datetime to
        standard datetime. The default is True.

    Returns
    -------
    None.
    """
    hours_list = hours_between(min_date, max_date,convert=convert)
    nights = night_intervals(hours_list, lights_on=lights_on,
                             lights_off=lights_off)
    if nights:
        for i, interval in enumerate(nights):
            start = interval[0]
            end = interval[1]
            if start != end:
                ax.axvspan(start,
                           end,
                           color='gray',
                           alpha=.2,
                           label='_'*i + 'lights off',
                           zorder=0)