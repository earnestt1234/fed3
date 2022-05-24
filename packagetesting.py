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
a = fed3.load("/Users/earnestt1234/Documents/fedviz/justin_data/FED7Cat.csv")
b = fed3.load("/Users/earnestt1234/Documents/fedviz/justin_data/FED3Cat.csv")

d = fplot.ipi({'B':[a, b]}, output='data')