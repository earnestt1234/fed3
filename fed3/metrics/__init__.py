# -*- coding: utf-8 -*-
'''This packages defines functions for extracting temporal variables from
FED3Frames, and tools for collecting those variables into tables.  This is used
extensively by `fed3.plot` for extracting the data to plot.

Fed3 uses "metrics" to specifically return to temporal variables, which are
represented as pandas Series objects (with timestamps in the index).'''

#imports for package namespace

from .core import get_metric, list_metrics

__all__ = ['get_metric', 'list_metrics']