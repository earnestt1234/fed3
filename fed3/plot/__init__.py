# -*- coding: utf-8 -*-

# things for all plots

import matplotlib.pyplot as plt

prop_cycle = plt.rcParams['axes.prop_cycle']
COLORCYCLE = prop_cycle.by_key()['color']

#imports for package namespace

from .barchart import bar
from .chronogram import (chronogram_circle, chronogram_line, chronogram_spiny)
from .ipi import (ipi)
from .simple import (line, scatter)



