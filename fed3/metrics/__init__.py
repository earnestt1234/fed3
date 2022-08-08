# -*- coding: utf-8 -*-
'''This packages defines functions for extracting temporal variables from
FED3Frames, and tools for collecting those variables into tables.  This is used
extensively by `fed3.plot` for extracting the data to plot.

Namely, for plotting functions which accept a paremeter for designating the
variable to be plotted (usually `y`), this package defines the functions for
calculating those variables for individual FEDFrames.

There are two main modules contained here: `fed3.metrics.core` defines
the actual functions which compute variables from FEDFrame objects,
while `fed3.metrics.tables` defines code for reshaping the returned
objects into more concise tables.

There are two main public functions for accessing metric functions, if desired:
`fed3.metrics.get_metric()` and `fed3.metrics.list_metrics()`.  The
latter will report the current metric functions available in fed3:

```python
>>> import fed3
>>> fed3.list_metrics()
['binary_pellets',
 'cumulative_pellets',
 'pellets',
 'binary_pokes',
 'cumulative_pokes',
 'pokes',
 'binary_left_pokes',
 'binary_right_pokes',
 'cumulative_left_pokes',
 'cumulative_right_pokes',
 'cumulative_left_percent',
 'cumulative_right_percent',
 'left_pokes',
 'right_pokes',
 'binary_correct_pokes',
 'binary_error_pokes',
 'cumulative_correct_pokes',
 'cumulative_error_pokes',
 'cumulative_correct_percent',
 'cumulative_error_percent',
 'correct_pokes',
 'error_pokes',
 'battery',
 'ipi',
 'motor',
 'rt']

```

'''

#imports for package namespace

from .core import get_metric, list_metrics

__all__ = ['get_metric', 'list_metrics']