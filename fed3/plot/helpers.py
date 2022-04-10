#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 12:34:52 2022

@author: earnestt1234
"""

import pandas as pd

def _get_return_value(FIG, DATA, output):

    if output == 'plot':
        return FIG

    elif output in ['dataonly', 'data']:
        return DATA

    elif output == 'both':
        return FIG, DATA

    else:
        raise ValueError(f'output value "{output}" not recognized.')

def _handle_feds(feds):
    if isinstance(feds, pd.DataFrame):
        feds = [feds]
    return feds

def _parse_feds(feds, raise_name_clash=True):

    if isinstance(feds, pd.DataFrame):
        feds = [feds]

    if not isinstance(feds, dict):

        _raise_name_clash(feds) if raise_name_clash else None
        feds = {f.name : [f] for f in feds}

    if raise_name_clash:
        for l in feds.values():
            _raise_name_clash(l)

    return feds

def _raise_name_clash(feds):

    names_okay = len(set(f.name for f in feds)) == len(feds)
    if not names_okay:
        raise ValueError("Some FEDFrames passed have conflicting names; set the `name` attribute uniquely to plot.")