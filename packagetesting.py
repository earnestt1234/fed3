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
d = fplot.line({'B':[a, b]}, output='data', bins='1H', color='green')