# -*- coding: utf-8 -*-

#imports for package namespace
import warnings

from fed3.core import *
from fed3.lightcycle import set_lightcycle

# set warnings style to remove reprinting of warning
def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
        return '%s:%s: %s: %s\n' % (filename, lineno, category.__name__, message)

warnings.formatwarning = warning_on_one_line