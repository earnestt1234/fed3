#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 18:06:53 2021

@author: earnestt1234
"""

from abc import ABCMeta, abstractmethod
from collections import Iterable

import matplotlib.pyplot as plt
import pandas as pd

from fed3.fed import align

from fed3.metrics import metricsdict

from fed3.plotting import _plot_line_data

def determine_alignment(feds, mixed='datetime'):
    alignments = set(f._alignment for f in feds)
    return mixed if len(alignments) > 1 else list(alignments)[0]

class FED3Analysis(metaclass=ABCMeta):
    def __init__(self):
        self.data = pd.DataFrame()
        self.feds = []

    @abstractmethod
    def runfor(self, feds):
        pass

    @abstractmethod
    def plot(self):
        pass

    def rerun(self):
        self.runfor(self.feds)

class SimpleLine(FED3Analysis):
    def __init__(self, y, align=None, cumulative='auto'):
        super().__init__()
        self.y = y
        self.align = align
        if cumulative == 'auto':
            cumulative = True
        self.cumulative = cumulative
        self._metric = None

    def runfor(self, feds, plot=False, mixed_align='raise'):
        self.feds = self._handle_feds(feds)
        if self.align is not None:
            self.feds = [align(f, self.align) for f in self.feds]
        if determine_alignment(self.feds, 'mixed') == 'mixed':
            if mixed_align == 'raise':
                raise ValueError('The passed feds have mixed alignment; '
                                 'you can either align them with the `align` argument '
                                 'or force plotting by setting the `mixed_align` argument.')
            if mixed_align == 'warn':
                print("PLACE A REAL WARNING HERE")
            elif mixed_align != 'ignore':
                raise ValueError('`mixed_align` must be "ignore", "warn", or "raise"')
        self.data = pd.DataFrame()
        self._metric = metricsdict[self.y]
        for fed in self.feds:
            y = self._metric(fed, self.cumulative)
            y.name = fed.name
            self.data = self.data.join(y, how='outer')

        if plot:
            self.plot()

        return self

    def rerun(self):
        return self.runfor(self.feds)

    def plot(self, xaxis='auto', shadedark=True, ax=None, legend=True):
        if ax is None:
            fig, ax = plt.subplots()

        if xaxis == 'auto':
            xaxis = determine_alignment(self.feds)

        if xaxis == 'elapsed':
            shadedark=False

        _plot_line_data(data=self.data,
                        ax=ax,
                        shadedark=shadedark,
                        legend=legend,
                        xaxis=xaxis,
                        ylabel=self._metric.nicename)

    def _handle_feds(self, feds):
        if not isinstance(feds, Iterable):
            feds = [feds]
        return feds

class Histogram(FED3Analysis):
    def __init__(self, y='ipi', logx=False,):
        super().__init__()



