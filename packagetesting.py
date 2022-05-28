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

# d = fplot.chronogram_spiny(a, output='data', bins='15T', color='green', plot_quick=True)

c = fed3.timecrop(a, a.index[1000], a.index[1735])