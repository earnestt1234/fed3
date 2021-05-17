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

b = fed3.align(b, 'time')

a = fed3.SimpleLine().runfor([a, b], plot=True)
