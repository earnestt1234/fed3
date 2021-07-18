#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 11:02:24 2021

@author: earnestt1234
"""

import fed3

p = '/Users/earnestt1234/Documents/fedviz/refed3vizworkshop/FED001_110920_02.CSV'
r = '/Users/earnestt1234/Documents/fedviz/refed3vizworkshop/FED002_110920_02.CSV'

a = fed3.load(p)
b = fed3.load(r)

metrics = 'pellets',
alignments = 'datetime', 'time', 'elapsed'

a.meals()

# for metric in metrics:
#     for align in alignments:
#         for cumulative in True, False:
#             print(metric, align, cumulative)
#             c = fed3.SimpleLine(y=metric,
#                                 align=align,
#                                 cumulative=cumulative).runfor([a, b], plot=True)
