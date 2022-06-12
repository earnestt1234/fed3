#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 11:02:24 2021

@author: earnestt1234
"""

import fed3
import fed3.plot as fplot

# load FED data
# a = fed3.load(r"/Users/earnestt1234/Documents/fedviz/justin_data/FED7Cat.csv")
# b = fed3.load(r"/Users/earnestt1234/Documents/fedviz/justin_data/FED3Cat.csv")

a = fed3.load(r"C:\Users\earne\Documents\fedviz\justin_data\FED3Cat.csv")
b = a.copy()
c = b[b.index.duplicated()]
# b = fed3.load(r"C:\Users\earne\Documents\fedviz\justin_data\FED7Cat.csv")
# c = fed3.load(r"C:\Users\earne\Documents\fedviz\WEEK 1\WEEK 1 - Copy\4-1_FED3024_111120_01.CSV")
# d = fed3.load(r"C:\Users\earne\Documents\fedviz\poketime\FED002_110920_02.CSV")

fplot.scatter(a, y='ipi')