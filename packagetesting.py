#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 11:02:24 2021

@author: earnestt1234
"""

import fed3

p = '/Users/earnestt1234/Documents/fedviz/refed3vizworkshop/FED001_110920_02.CSV'
r = '/Users/earnestt1234/Documents/fedviz/refed3vizworkshop/FED002_110920_02.CSV'

fed1 = fed3.load(p)
fed2 = fed3.load(r)

analysis = fed3.SimpleLine().runfor([fed1, fed2], plot=True)
