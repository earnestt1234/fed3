#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 12:34:52 2022

@author: earnestt1234
"""

from collections import defaultdict

from matplotlib import colors
import matplotlib.pyplot as plt
import pandas as pd

# ---- 'Private'

def _assign_plot_names(feds, name_ddict):
    if isinstance(feds, pd.DataFrame):
        feds = [feds]

    for fed in feds:
        count = name_ddict[fed.name]
        if count == 0:
            fed._plot_name = fed.name
        else:
            fed._plot_name = f'{fed.name}_{count}'

        name_ddict[fed.name] += 1

def _get_most_recent_color(ax, kind='line', default='gray'):

    if kind == 'line':
        color = ax.get_lines()[-1].get_color()
    elif kind == 'scatter':
        color = ax.collections[-1].get_facecolor()
    elif kind == 'bar':
        color = ax.patches[-1].get_facecolor()

    try:
        color = colors.to_hex(color)
    except ValueError:
        color = default

    return color


def _get_return_value(FIG, DATA, output):

    if output == 'plot':
        return FIG

    elif output in ['dataonly', 'data']:
        return DATA

    elif output == 'both':
        return FIG, DATA

    else:
        raise ValueError(f'output value "{output}" not recognized.')

def _parse_feds(feds):

    name_ddict = defaultdict(int)

    if isinstance(feds, pd.DataFrame):
        feds = [feds]

    if not isinstance(feds, dict):
        _assign_plot_names(feds=feds, name_ddict=name_ddict)
        feds = {f._plot_name : [f] for f in feds}

    else:
        for k, v in feds.items():
            if isinstance(v, pd.DataFrame):
                feds[k] = [v]
            _assign_plot_names(feds=v, name_ddict=name_ddict)

    return feds

def _process_plot_kwargs(kwargs, plot_labels):

    kwargs_for_all = {}
    output = {name: {} for name in plot_labels}
    for k, v in kwargs.items():
        if isinstance(v, ArgHelper):
            output.update(v.generate_kwargs(k, plot_labels))
        elif k not in plot_labels:
            kwargs_for_all[k] = v

    for lab in plot_labels:
        output[lab].update(kwargs_for_all.copy())
        if kwargs.get(lab):
            output[lab].update(kwargs[lab])

    return output

# ---- Public

def argh(args):
    '''
    argh = arg helper.  Use this to pass each argument in `args`
    one at a time to each curve being plotted.  If not used,
    a list of args will be passed to each curve in its entirety.

    Parameters
    ----------
    args : list-like
        Arguments to pass out.

    Returns
    -------
    ArgHelper
        Object for distributing the arguments.

    '''
    return ArgHelper(args)

def legend(*args, **kwargs):
    '''Convenience method for calling `plt.legend()` to generate a legend'''
    plt.legend(*args, **kwargs)

class ArgHelper:

    def __init__(self, args):
        self.args = args

    def generate_kwargs(self, argname, plot_labels):
        return {name: {argname: arg} for name, arg in zip(plot_labels, self.args)}
