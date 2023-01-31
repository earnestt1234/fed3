# -*- coding: utf-8 -*-

'''
.. include:: ../../docs/plots_getting_started.md
'''

# define options
OPTIONS = {'default_shadedark': True,
           'default_legend': True}

# imports for package namespace

from .barchart import bar
from .chronogram import (chronogram_circle, chronogram_line, chronogram_spiny)
from .helpers import argh, legend
from .ipi import (ipi)
from .shadedark import shade_darkness
from .simple import (line, scatter)

__all__ = ['argh',
           'bar',
           'chronogram_circle',
           'chronogram_line',
           'chronogram_spiny',
           'ipi',
           'legend',
           'line',
           'scatter',
           'shade_darkness']


