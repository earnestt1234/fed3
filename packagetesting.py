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
a = fed3.load(r"/Users/earnestt1234/Documents/fedviz/justin_data/FED7Cat.csv")
b = fed3.load(r"/Users/earnestt1234/Documents/fedviz/justin_data/FED3Cat.csv")

# a = fed3.load(r"C:\Users\earne\Documents\fedviz\justin_data\FED3Cat.csv")
# b = fed3.load(r"C:\Users\earne\Documents\fedviz\justin_data\FED7Cat.csv")

c = fed3.split(a, dates = a.index[[1000, 2000, 3000, 4000, 5000]])
d = fed3.split(b, dates = b.index[[1000, 2000, 3000, 4000, 5000]])

bar_kwargs = {
    'A': {'color':'green'},
    'B': {'color':'red'},
    }

scatter_kwargs = {
    'A': {'color':'green'},
    'B': {'color':'red'}
    }

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(3, 7))
x = fplot.bar({'A':c, 'B':d}, show_individual=True,
              bar_kwargs=bar_kwargs, scatter_kwargs=scatter_kwargs, positions=[0,0],
              ax=ax, normalize='1H')