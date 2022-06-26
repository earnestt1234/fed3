#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General code for helping with the light cycle for FED3 data.
"""

__all__ = ['set_lightcycle']

import datetime as dt

import pandas as pd

LIGHTCYCLE = {'on': dt.time(hour=7, minute=0), 'off': dt.time(hour=19, minute=0)}
'''Dictionary determining the light cycle.  Should be a dictionary with an
`'on'` key and an `'off'`, each pointint to  `datetime.time` object with the
hour and minute specified (note that further precision is not used).'''

def time_to_float(x):
    '''Convert a datetime/time object to an float in [0-24).'''
    return x.hour + (1/60) * x.minute

def set_lightcycle(on_hour, off_hour, on_minute=0, off_minute=0):
    '''
    Set the light cycle.  This affects shading on plots and operations
    which group data based on the light cycle.

    Parameters
    ----------
    on_hour : int
        Integer indicating the hour of day when lights turn on, in [0-24).
    off_hour : int
        Integer indicating the hour of day when lights turn off, in [0-24).
    on_minute : int, optional
        Minute of the `on_hour` where lights turn on, in [0-60).
    off_minute : int, optional
        Minute of the `off_hour` where lights turn off, in [0-60).

    Returns
    -------
    None.

    '''
    LIGHTCYCLE['on'] = dt.time(hour=on_hour, minute=on_minute)
    LIGHTCYCLE['off'] = dt.time(hour=off_hour, minute=off_minute)

def is_at_night(datetime, lights_on, lights_off):
    '''Returns `True` if an input timestamp is at night.  Note that `lights_on`
    and `lights_off` should be `datetime.time` objects.'''
    ashour = time_to_float(datetime)
    lights_on = time_to_float(lights_on)
    lights_off = time_to_float(lights_off)
    if lights_on > lights_off:
        return (lights_off <= ashour < lights_on)
    else:
        return (ashour < lights_on or ashour >= lights_off)

def lightcycle_tuples(start_date, end_date, lights_on, lights_off, kind='nights',
                      pdconvert=True):
    '''
    Given two input timestamps, return a list of tuples indicating the
    start and end of each day/night period occuring between them.  Used
    for determining when to shade dark periods within `fed3.plot`.

    Parameters
    ----------
    start_date : str or datetime object
        Start time.
    end_date : str or datetime object
        End time.
    lights_on : datetime.time
        Time of day lights turn on.
    lights_off : datetime.time
        Time of day lights turn off.
    kind : str, 'days' or 'nights', optional
        Return tuples corresponding to the daytime or nighttime.
        The default is 'nights'.
    pdconvert : bool, optional
        Use `pandas.to_datetime` to convert `start_date` and `end_date`.
        The default is True.

    Raises
    ------
    ValueError
        Unrecognized value passed to `kind`.

    Returns
    -------
    result : list
        List of two-tuples of datetime objects.

    '''

    if kind not in ['days', 'nights']:
        raise ValueError(f"`kind` must be 'nights' or 'days', not {kind}")

    result = []
    t = start_date
    day = pd.Timedelta('24H')

    lookfor = 'on' if kind == 'days' else 'off'

    if pdconvert:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

    while True:

        if t == end_date:
            if lookfor == 'on' and is_at_night(end_date, lights_on, lights_off):
                result.append(t)
            break

        elif lookfor == 'off':
            if is_at_night(t, lights_on, lights_off):
                result.append(t)
                new_t = t.replace(hour=lights_on.hour, minute=lights_on.minute).floor('1T')
                lookfor = 'on'
            else:
                new_t = t.replace(hour=lights_off.hour, minute=lights_off.minute).floor('1T')

        elif lookfor == 'on':
            if not is_at_night(t, lights_on, lights_off):
                result.append(t)
                new_t = t.replace(hour=lights_off.hour, minute=lights_off.minute).floor('1T')
                lookfor = 'off'
            else:
                new_t = t.replace(hour=lights_on.hour, minute=lights_on.minute).floor('1T')

        if new_t < t:
            new_t += day

        if new_t > end_date:
            new_t = end_date

        t = new_t

    result = list(zip(result[::2], result[1::2]))

    return result