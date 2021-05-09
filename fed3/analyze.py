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
from fed3.plotting import (format_xaxis_datetime,
                           format_xaxis_time,
                           _plot_line_data)

def determine_alignment(feds):
    alignments = set(f._alignment for f in feds)
    return 'datetime' if len(alignments) > 1 else list(alignments)[0]

class FED3Analysis(metaclass=ABCMeta):
    def __init__(self):
        self.data = None
        self.feds = None

    @abstractmethod
    def runfor(self, feds):
        pass

    @abstractmethod
    def rerun(self):
        pass

    @abstractmethod
    def plot(self):
        pass

class SimpleLine(FED3Analysis):
    def __init__(self, y='pellets', align=None, cumulative='auto'):
        super().__init__()
        self.y = y
        self.align = align
        if cumulative == 'auto':
            cumulative = True
        self.cumulative = cumulative
        self._metric = None

    def runfor(self, feds, plot=False):
        self.feds = self._handle_feds(feds)
        if self.align is not None:
            feds = [align(f, self.align) for f in self.feds]
        else:
            feds = self.feds
        self.data = pd.DataFrame()
        self._metric = metricsdict[self.y]
        for fed in feds:
            y = self._metric(fed, self.cumulative)
            y.name = fed.name
            self.data = self.data.join(y, how='outer')

        if plot:
            self.plot()

        return self

    def rerun(self):
        return self.run(self.feds)

    def plot(self, xaxis='auto', shadedark=True, ax=None, legend=True):
        if ax is None:
            ax = plt.gca()

        if xaxis == 'auto':
            xaxis = determine_alignment(self.feds)

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



