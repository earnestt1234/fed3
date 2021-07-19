#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 11:02:24 2021

@author: earnestt1234
"""

import fed3

a = fed3.load(r"C:\Users\earne\Documents\fedviz\justin_data\FED2Cat.csv")
b = fed3.load(r"C:\Users\earne\Documents\fedviz\justin_data\FED3Cat.csv")


hist = fed3.IPI().runfor([a, b])
hist.plot(logx=True)