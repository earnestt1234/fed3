#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 11:02:24 2021

@author: earnestt1234
"""

import fed3
import fed3.plot as fplot

import numpy as np

# load FED data
a = fed3.load(r"C:\Users\earne\Documents\fedviz\justin_data\FED7Cat.csv")
b = fed3.load(r"C:\Users\earne\Documents\fedviz\justin_data\FED3Cat.csv")


import matplotlib.pyplot as plt
d = fplot.chronogram_spiny({'B':[a, b]}, output='data', bins='1H', color='green')
plt.tight_layout()

#%%

import pandas as pd

def is_at_night(datetime, lights_on, lights_off):

    ashour = datetime.hour + (1/60) * datetime.minute
    if lights_on > lights_off:
        return (lights_off <= ashour < lights_on)
    else:
        return (ashour < lights_on or ashour >= lights_off)

# def nighttime_intervals(start_date, end_date, lights_on, lights_off):

#     result = []
#     pair = []

#     if is_at_night(start_date):
#         pair.append(start_date)
#     else:
#         first_night = start_date.replace(hour=lights_on)
#         first_night += pd.Timedelta('24H') * (first_night < start_date)
#         pair.append(first_night)



start_date = pd.to_datetime("01-15-2000 19:00")
end_date = pd.to_datetime("01-20-2000 19:01")
lights_on = 7
lights_off = 19

result = []
t = start_date
lookfor = 'off'
day = pd.Timedelta('24H')

if start_date >= end_date:
    raise ValueError("start_date must be strictly earlier than end_date")

if is_at_night(start_date, lights_on, lights_off):
    result.append(start_date)
    lookfor = 'on'

while t < end_date:

    if lookfor == 'off':
        new_t = t.replace(hour=lights_off)
        if new_t < t:
            new_t += day

        t = new_t
        lookfor = 'on'


    elif lookfor == 'on':
        new_t = t.replace(hour=lights_on)
        if new_t < t:
            new_t += day

        t = new_t
        lookfor = 'off'

    if t < end_date:
        result.append(t)

if is_at_night(end_date, lights_on, lights_off) and lookfor == 'off':
    result.append(end_date)


# while True:




#%%


