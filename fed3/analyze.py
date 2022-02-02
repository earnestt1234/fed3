#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 18:06:53 2021

@author: earnestt1234
"""

from abc import ABCMeta, abstractmethod

import matplotlib.pyplot as plt
import pandas as pd

from fed3.fedfuncs import screen_mixed_alignment

from fed3.metrics import METRICS, METRICNAMES

from fed3.plotting import (plot_line_data,
                           plot_hist_data,
                           plot_scatter_data)

class FED3Analysis(metaclass=ABCMeta):

    def __init__(self):
        self.data = pd.DataFrame()

    @abstractmethod
    def run(self, feds):
        pass

    @abstractmethod
    def plot(self):
        pass

    def verify_data(plotfunc):

        def check_data_and_plot(self, *args, **kwargs):

            # check
            if self.data.empty:
                raise RuntimeError('The data attribute is an empty DataFrame; '
                                   'the analysis needs to be run on FEDS before plotting.')

            # plot
            plotfunc(self, *args, **kwargs)

        return check_data_and_plot

class TimestampsByFEDs(FED3Analysis):

    def __init__(self, y):
        super().__init__()
        self.y = y
        self._metric = None
        self._metricname = None
        self._alignment = None

    def _set_metric(self, y):
        if isinstance(y, str):

            key = y.lower()
            try:
                self._metric = METRICS[key]
                self._metricname = METRICNAMES[key]
            except KeyError:
                raise ValueError(f'y-value "{y}" is not recognized.')

        else:
            self._metric = y
            self._metricname = y.__name__

    def _handle_feds(self, feds):
        if isinstance(feds, pd.DataFrame):
            feds = [feds]
        return feds

    def run(self, feds, plot=False, mixed_align='raise'):

        # parse feds to list
        feds = self._handle_feds(feds)

        # handle mixed alignment
        self._alignment = screen_mixed_alignment(feds, option=mixed_align)

        # reset data and metric
        self.data = pd.DataFrame()
        self._set_metric(self.y)

        # calculate metric for each fed
        for fed in feds:
            y = self._metric(fed)
            y.name = fed.name
            self.data = self.data.join(y, how='outer')

        # plot if desired
        if plot:
            self.plot()

        return self

class LinePlot(TimestampsByFEDs):

    @FED3Analysis.verify_data
    def plot(self, xaxis='auto', shadedark=True, ax=None, legend=True,
             fed_styles=None, **kwargs):

        if ax is None:
            ax = plt.gca()

        if xaxis == 'auto':
            xaxis = self._alignment

        if xaxis == 'elapsed':
            shadedark = False

        fig = plot_line_data(ax=ax,
                             data=self.data,
                             shadedark=shadedark,
                             legend=legend,
                             xaxis=xaxis,
                             ylabel=self._metricname,
                             fed_styles=fed_styles,
                             **kwargs)

        return fig

class IPI(TimestampsByFEDs):
    def __init__(self):
        super().__init__(y='ipi')

    def plot(self, logx=False, kde=True, ax=None, legend=True,
             fed_styles=None, **kwargs):
        if ax is None:
            ax = plt.gca()

        fig = plot_hist_data(ax=ax,
                             data=self.data,
                             logx=logx,
                             kde=kde,
                             xlabel=self._metricname,
                             fed_styles=fed_styles,
                             legend=legend,
                             **kwargs)

        return fig

class ScatterPlot(TimestampsByFEDs):

    @FED3Analysis.verify_data
    def plot(self, xaxis='auto', shadedark=True, ax=None, legend=True,
             fed_styles=None, **kwargs):

        if ax is None:
            ax = plt.gca()

        if xaxis == 'auto':
            xaxis = self._alignment

        if xaxis == 'elapsed':
            shadedark = False

        fig = plot_scatter_data(ax=ax,
                                data=self.data,
                                shadedark=shadedark,
                                legend=legend,
                                xaxis=xaxis,
                                ylabel=self._metricname,
                                fed_styles=fed_styles,
                                **kwargs)

        return fig



