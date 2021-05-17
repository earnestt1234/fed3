#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  9 12:42:13 2021

@author: earnestt1234
"""

from fed3.format_axis import (FORMAT_XAXIS_OPTS,)

from fed3.lightcycle import (LIGHTCYCLE,
                             shade_darkness)

def _plot_line_data(data, ax, xaxis='datetime', shadedark=True,
                    legend=True, drawstyle='steps', ylabel=''):
    for col in data.columns:
        y = data[col].dropna()
        x = y.index
        ax.plot(x, y, label=col, drawstyle=drawstyle)

    if shadedark:
        shade_darkness(ax, x.min(), x.max(),
                       lights_on=LIGHTCYCLE['on'],
                       lights_off=LIGHTCYCLE['off'])

    if legend:
        ax.legend()

    FORMAT_XAXIS_OPTS[xaxis](ax, x.min(), x.max())
    ax.set_ylabel(ylabel)
