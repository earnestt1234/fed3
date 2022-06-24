# -*- coding: utf-8 -*-
'''This packge defines the major FEDFrame class (`fed3.core.fedframe.FEDFrame`)
for representing fed3 data.  It is a subclass of pandas DataFrame.
Other functions are defined for manipulating FEDFrames.'''

#imports for package namespace

from .fedframe import FEDFrame

from .fedfuncs import (align,
                       can_concat,
                       concat,
                       load,
                       split,
                       timecrop)

__all__ = ['FEDFrame',
           'align',
           'can_concat',
           'concat',
           'load',
           'split',
           'timecrop']
