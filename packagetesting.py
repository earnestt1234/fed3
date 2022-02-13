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
f1 = fed3.load("/Users/earnestt1234/Documents/fedviz/justin_data/FED2Cat.csv")
f2 = fed3.load("/Users/earnestt1234/Documents/fedviz/justin_data/FED3Cat.csv")
f3 = fed3.load("/Users/earnestt1234/Documents/fedviz/justin_data/FED4Cat.csv")

d = fplot._simple_group_plot({'a':[f1, f2, f3]}, output='data', y='bpellets')