# -*- coding: utf-8 -*-

'''fed3 is a Python package for working with FED3 data.'''

# set warnings style to remove reprinting of warning
import warnings as __warnings

def __warning_on_one_line(message, category, filename, lineno, file=None, line=None):
        return '%s:%s: %s: %s\n' % (filename, lineno, category.__name__, message)

__warnings.formatwarning = __warning_on_one_line

# version
from ._version import v
__version__ = v
del v

#imports for package namespace
from fed3.core import (FEDFrame,
                       as_aligned,
                       can_concat,
                       concat,
                       load,
                       split,
                       timecrop)

from fed3.examples import list_examples, load_examples

from fed3.lightcycle import set_lightcycle

from fed3.metrics import get_metric, list_metrics

__all__ = [
    'FEDFrame',
    'as_aligned',
    'can_concat',
    'concat',
    'load',
    'split',
    'timecrop',
    'list_examples',
    'load_examples',
    'set_lightcycle',
    'get_metric',
    'list_metrics'
    ]
