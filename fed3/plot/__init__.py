# -*- coding: utf-8 -*-

# things for all plots

import matplotlib.pyplot as plt

prop_cycle = plt.rcParams['axes.prop_cycle']
COLORCYCLE = prop_cycle.by_key()['color']

#imports for package namespace

from .ipi import (ipi)
from .simple import (line, scatter)



