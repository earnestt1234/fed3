# -*- coding: utf-8 -*-

'''
.. include:: ../../docs/plots_getting_started.md
'''

# color cycle
import matplotlib.pyplot as plt

prop_cycle = plt.rcParams['axes.prop_cycle']
COLORCYCLE = list(prop_cycle.by_key()['color'])

def set_colorcycle(colors):
    COLORCYCLE[:] = list(colors)

#imports for package namespace

from .barchart import bar
from .chronogram import (chronogram_circle, chronogram_line, chronogram_spiny)
from .ipi import (ipi)
from .simple import (line, scatter)

__all__ = ['COLORCYCLE',
           'bar',
           'chronogram_circle',
           'chronogram_line',
           'chronogram_spiny',
           'ipi',
           'line',
           'scatter',
           'set_colorcycle']

