#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  9 15:24:38 2021

@author: earnestt1234
"""

__all__ = ['format_xaxis_datetime',
           'format_xaxis_elapsed',
           'format_xaxis_time']

import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

def format_xaxis_datetime(ax, start, end):
    d8_span = end - start
    if d8_span < datetime.timedelta(hours=12):
        xfmt = mdates.DateFormatter('%H:%M')
        major = mdates.HourLocator()
        minor = mdates.MinuteLocator(byminute=[0,15,30,45])
    elif datetime.timedelta(hours=12) <= d8_span < datetime.timedelta(hours=24):
        xfmt = mdates.DateFormatter('%b %d %H:%M')
        major = mdates.HourLocator(byhour=[0,6,12,18])
        minor = mdates.HourLocator()
    elif datetime.timedelta(hours=24) <= d8_span < datetime.timedelta(days=3):
        xfmt = mdates.DateFormatter('%b %d %H:%M')
        major = mdates.DayLocator()
        minor = mdates.HourLocator(byhour=[0,6,12,18])
    elif datetime.timedelta(days=3) <= d8_span < datetime.timedelta(days=6):
        xfmt = mdates.DateFormatter('%b %d %H:%M')
        major = mdates.DayLocator(interval=2)
        minor = mdates.DayLocator()
    elif datetime.timedelta(days=6) <= d8_span < datetime.timedelta(days=20):
        xfmt = mdates.DateFormatter('%b %d')
        major = mdates.DayLocator(interval=3)
        minor = mdates.DayLocator()
    elif datetime.timedelta(days=20) <= d8_span < datetime.timedelta(days=32):
        xfmt = mdates.DateFormatter('%b %d')
        major = mdates.DayLocator(interval=5)
        minor = mdates.DayLocator()
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    elif datetime.timedelta(days=32) <= d8_span < datetime.timedelta(days=60):
        xfmt = mdates.DateFormatter('%b %d')
        major = mdates.DayLocator(interval=10)
        minor = mdates.DayLocator(interval=5)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    elif datetime.timedelta(days=62) <= d8_span < datetime.timedelta(days=120):
        xfmt = mdates.DateFormatter('%b %d')
        major = mdates.DayLocator(interval=15)
        minor = mdates.DayLocator(interval=5)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    elif datetime.timedelta(days=120) <= d8_span < datetime.timedelta(days=120):
        xfmt = mdates.DateFormatter("%b '%y")
        major = mdates.MonthLocator()
        minor = mdates.DayLocator(bymonthday=[7,15,23])
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    ax.xaxis.set_major_locator(major)
    ax.xaxis.set_major_formatter(xfmt)
    ax.xaxis.set_minor_locator(minor)
    ax.set_xlabel('Time')

def format_xaxis_time(ax, start, end):
    start = start.floor('1H')
    end = end.ceil('1H')
    diff = (end - start).total_seconds() / 3600

    if diff <= 3:
        ticks = pd.date_range(start, end, freq='30T')
    else:
        freq = 1
        while (diff // freq) > 5:
            freq += 1
        ticks = pd.date_range(start, end, freq=f'{freq}H')

    ticklabels = ((ticks - ticks[0]).total_seconds() / 3600).astype(int)
    ax.set_xticks(ticks)
    ax.set_xticklabels(ticklabels)

    hours_start = start.strftime('%I%p')
    if hours_start[0] == '0':
        hours_start = hours_start[1:]
    ax.set_xlabel(f'Hours since startpoint ({hours_start})')

def format_xaxis_elapsed(ax, start, end):
    start = start.floor('1H')
    end = end.ceil('1H')
    diff = (end - start).total_seconds() / 3600

    if diff <= 3:
        ticks = pd.date_range(start, end, freq='30T')
    else:
        freq = 1
        while (diff // freq) > 5:
            freq += 1
        ticks = pd.date_range(start, end, freq=f'{freq}H')

    ticklabels = ((ticks - ticks[0]).total_seconds() / 3600).astype(int)
    ax.set_xticks(ticks)
    ax.set_xticklabels(ticklabels)

    ax.set_xlabel('Elapsed time (h)')

FORMAT_XAXIS_OPTS = {'datetime': format_xaxis_datetime,
                     'time': format_xaxis_time,
                     'elapsed': format_xaxis_elapsed}