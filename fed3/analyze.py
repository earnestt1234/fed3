#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 18:06:53 2021

@author: earnestt1234
"""

from abc import ABCMeta, abstractmethod

import matplotlib.pyplot as plt
import pandas as pd

from fed3.fedfuncs import determine_alignment, screen_mixed_alignment

from fed3.metrics import metricsdict

from fed3.plotting import (plot_line_data,
                           plot_hist_data)

class FED3Analysis(metaclass=ABCMeta):
    def __init__(self):
        self.data = pd.DataFrame()

    @abstractmethod
    def run(self, feds):
        pass

    @abstractmethod
    def plot(self):
        pass

class TimestampsByFEDs(FED3Analysis):
    def __init__(self, y):
        super().__init__()
        self.y = y
        self._metric = None

    def _set_metric(self, y):
        if isinstance(y, str):
            self._metric = metricsdict[y]
        else:
            self._metric = y

    def _handle_feds(self, feds):
        if isinstance(feds, pd.DataFrame):
            feds = [feds]
        return feds

    def run(self, feds, plot=False, mixed_align='raise'):
        screen_mixed_alignment(feds, option=mixed_align)
        self.data = pd.DataFrame()
        self._set_metric(self.y)
        for fed in self.feds:
            y = self._metric(fed)
            y.name = fed.name
            self.data = self.data.join(y, how='outer')

        if plot:
            self.plot()

        return self

class SimpleLine(TimestampsByFEDs):
    def plot(self, xaxis='auto', shadedark=True, ax=None, legend=True, **kwargs):
        if ax is None:
            fig, ax = plt.subplots()

        if xaxis == 'auto':
            xaxis = determine_alignment(self.feds)

        if xaxis == 'elapsed':
            shadedark=False

        plot_line_data(ax=ax,
                       data=self.data,
                       shadedark=shadedark,
                       legend=legend,
                       xaxis=xaxis,
                       ylabel=self._metric.nicename,
                       **kwargs)

class IPI(TimestampsByFEDs):
    def __init__(self):
        super().__init__(y='ipi')

    def plot(self, logx=False, kde=True, ax=None, **kwargs):
        if ax is None:
            fig, ax = plt.subplots()

        plot_hist_data(ax=ax,
                       data=self.data,
                       logx=logx,
                       kde=kde,
                       xlabel=self._metric.nicename,
                       **kwargs)




