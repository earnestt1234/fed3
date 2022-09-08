# -*- coding: utf-8 -*-

'''
.. include:: ../../docs/plots_getting_started.md
'''

#imports for package namespace

from .barchart import bar
from .chronogram import (chronogram_circle, chronogram_line, chronogram_spiny)
from .ipi import (ipi)
from .simple import (line, scatter)

__all__ = ['bar',
           'chronogram_circle',
           'chronogram_line',
           'chronogram_spiny',
           'ipi',
           'line',
           'scatter']

