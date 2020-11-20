#! /usr/bin/env python3
"""
Module providing classes for adding :mod:`matplotlib` plots to wxPython GUIs
"""

import matplotlib as mpl
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar

import wx
import wx.lib.agw.aui as aui


class Plot(wx.Panel):
  """
  :mod:`matplotlib` plot

  Based on https://matplotlib.org/3.2.1/gallery/user_interfaces/embedding_in_wx5_sgskip.html.
  """

  def __init__(self, parent, id=-1, dpi=None, interactive=True, **kwargs):
    wx.Panel.__init__(self, parent, id=id, **kwargs)
    self.figure = mpl.figure.Figure(dpi=dpi, figsize=(2, 2))
    self.canvas = FigureCanvas(self, -1, self.figure)
    if interactive:
      self.toolbar = NavigationToolbar(self.canvas)
      self.toolbar.Realize()

    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(self.canvas, 1, wx.EXPAND)
    if interactive:
      sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
    self.SetSizer(sizer)


class PlotNotebook(wx.Panel):
  """
  Notebook of :mod:`matplotlib` plots

  Based on https://matplotlib.org/3.2.1/gallery/user_interfaces/embedding_in_wx5_sgskip.html.
  """

  def __init__(self, parent, id=-1, interactive=True):
    wx.Panel.__init__(self, parent, id=id)
    self.nb = aui.AuiNotebook(self)
    sizer = wx.BoxSizer()
    sizer.Add(self.nb, 1, wx.EXPAND)
    self.SetSizer(sizer)
    self.interactive = interactive

  def add(self, name="plot"):
    page = Plot(self.nb, interactive=self.interactive)
    self.nb.AddPage(page, name)
    # return page.figure
    return page

  def clear(self):
    while self.nb.GetPageCount() > 0:
      self.nb.DeletePage(0)
