#! /usr/bin/env python3
"""
Nonsensical Python GUI project using wxPython

This is just to educate myself, nothing here has any real sense.
"""

import builtins
from datetime import date
from datetime import datetime
import json
import matplotlib as mpl
import urllib.request
import wx
import wxMatPlotLib


builtins.__dict__['_'] = wx.GetTranslation


class MainWindow(wx.Frame):
  """
  Main window shown upon startup of the application
  """

  statusTextClearDelay = 5000
  """ Delay in milliseconds after which the text in the status bar is cleared """


  def __init__(self):
    """
    Constructor
    """

    super().__init__(parent = None, title = "COVID-19 Data Plotter", size = wx.Size(1150, 800))
    self.SetIcon(wx.Icon("graphics/Signal-Uncapped-t0obs.ico")) # https://stackoverflow.com/questions/25002573/how-to-set-icon-on-wxframe
    # self.Maximize(True)
    # self.ShowFullScreen(True)

    self.generateUI()
    self.bindUI()

    self.Show(True)


  def generateUI(self):
    """
    Generate the GUI

    For the country flags shown in the buttons that select / deselect a country from the plots, besides the regular flag bitmap another bitmap is needed which is greyed out and shown when the button is disabled. These greyed-out bitmaps are derived from the regular bitmaps using GIMP with the following manipulations:

    ..    include:: <isonum.txt>
    - Colors |rarr| Brightness-Contrast |rarr| Contrast = -60
    - Colors |rarr| Hue-Saturation |rarr| Saturation = -60

    """

    # program menubar at the top of the frame
    # list of standard IDs which lead to small icons in the menu: https://wxpython.org/Phoenix/docs/html/wx.StandardID.enumeration.html

    menuFileCountries = wx.Menu()
    self.menuFileAF = menuFileCountries.Append(id = wx.ID_ANY, item = _(u"Afghanistan"), kind = wx.ITEM_CHECK)
    self.menuFileCO = menuFileCountries.Append(id = wx.ID_ANY, item = _(u"Colombia"), kind = wx.ITEM_CHECK)
    self.menuFileCZ = menuFileCountries.Append(id = wx.ID_ANY, item = _(u"Czechia"), kind = wx.ITEM_CHECK)
    self.menuFileFR = menuFileCountries.Append(id = wx.ID_ANY, item = _(u"France"), kind = wx.ITEM_CHECK)
    self.menuFileDE = menuFileCountries.Append(id = wx.ID_ANY, item = _(u"Germany"), kind = wx.ITEM_CHECK)
    self.menuFileGR = menuFileCountries.Append(id = wx.ID_ANY, item = _(u"Greece"), kind = wx.ITEM_CHECK)
    self.menuFileMX = menuFileCountries.Append(id = wx.ID_ANY, item = _(u"Mexico"), kind = wx.ITEM_CHECK)
    self.menuFileSK = menuFileCountries.Append(id = wx.ID_ANY, item = _(u"Slovakia"), kind = wx.ITEM_CHECK)
    self.menuFileES = menuFileCountries.Append(id = wx.ID_ANY, item = _(u"Spain"), kind = wx.ITEM_CHECK)
    self.menuFileSE = menuFileCountries.Append(id = wx.ID_ANY, item = _(u"Sweden"), kind = wx.ITEM_CHECK)
    self.menuFileGB = menuFileCountries.Append(id = wx.ID_ANY, item = _(u"United Kingdom"), kind = wx.ITEM_CHECK)
    menuFileCountries.AppendSeparator()
    self.menuFileNone = menuFileCountries.Append(id = wx.ID_ANY, item = _(u"Select &none\tCtrl+N"))
    self.menuFileAll = menuFileCountries.Append(id = wx.ID_ANY, item = _(u"Select &all\tCtrl+A"))

    menuFileLang = wx.Menu()
    self.menuFileLangEn = menuFileLang.Append(id = wx.ID_ANY, item = _("&English\tCtrl+E"), helpString = _(u"Show interface in English"), kind = wx.ITEM_RADIO)
    self.menuFileLangDe = menuFileLang.Append(id = wx.ID_ANY, item = _("&German\tCtrl+G"), helpString = _(u"Show interface in German"), kind = wx.ITEM_RADIO)

    menuFile = wx.Menu()
    self.menuFileDownload = menuFile.Append(id = wx.ID_DOWN, item = _(u"&Download\tCtrl+D"), helpString = _(u"Download JSON data file from the internet"))
    self.menuFileOpen = menuFile.Append(id = wx.ID_OPEN, item = _(u"&Open"), helpString = _(u"Open local JSON data file"))
    menuFile.Append(id = wx.ID_ANY, item = _(u"&Countries"), subMenu = menuFileCountries)
    menuFile.AppendSeparator()
    menuFile.Append(id = wx.ID_ANY, item = _(u"&Language"), subMenu = menuFileLang, helpString = _(u"Interface language"))
    menuFile.AppendSeparator()
    menuFile.Append(wx.ID_EXIT, _(u"E&xit"), _(u"Terminate the program"))

    menuHelp = wx.Menu()
    self.menuHelpAbout = menuHelp.Append(id = wx.ID_ABOUT, item = _(u"A&bout\tCtrl+B"), helpString = _(u"Information about this program"), kind =  wx.ITEM_NORMAL)

    menubar = wx.MenuBar()
    menubar.Append(menuFile, _(u"&File"))
    menubar.Append(menuHelp, _(u"&Help"))
    self.SetMenuBar(menubar)

    # toolbar at the top of the frame, just below the menubar

    self.toolDownloadID = 8
    self.toolOpenID = 7
    self.toolLangEnID = 5
    self.toolLangDeID = 6
    self.toolAF_ID = 20
    self.toolCO_ID = 21
    self.toolCZ_ID = 22
    self.toolDE_ID = 23
    self.toolES_ID = 24
    self.toolFR_ID = 25
    self.toolGB_ID = 26
    self.toolGR_ID = 27
    self.toolMX_ID = 28
    self.toolSE_ID = 30
    self.toolSK_ID = 29
    self.toolNone_ID = 31
    self.toolAll_ID = 32
    self.toolbar = self.CreateToolBar(style = wx.TB_HORZ_TEXT)
    self.toolDownload = self.toolbar.AddTool(toolId = self.toolDownloadID, label = _(u"Download"), bitmap = wx.ArtProvider.GetBitmap(id = wx.ART_GO_DOWN), shortHelp = _(u"Download JSON data file from the internet (Ctrl+D)"))
    self.toolOpen = self.toolbar.AddTool(toolId = self.toolOpenID, label = _(u"Open"), bitmap = wx.ArtProvider.GetBitmap(id = wx.ART_FILE_OPEN), shortHelp = _(u"Open local JSON data file (Ctrl+O)"))
    self.toolbar.AddSeparator()
    self.toolAF = self.toolbar.AddTool(toolId = self.toolAF_ID, label = "AF", bitmap = wx.Bitmap("graphics/flag_AF_30x20.bmp"), bmpDisabled = wx.Bitmap("graphics/flag_AF_30x20_disabled.bmp"), kind = wx.ITEM_CHECK, shortHelp = _(u"Afghanistan"), longHelp = _(u"Include/exclude Afghanistan in/from timeseries plotting"))
    self.toolCO = self.toolbar.AddTool(toolId = self.toolCO_ID, label = "CO", bitmap = wx.Bitmap("graphics/flag_CO_30x20.bmp"), bmpDisabled = wx.Bitmap("graphics/flag_CO_30x20_disabled.bmp"), kind = wx.ITEM_CHECK, shortHelp = _(u"Colombia"), longHelp = _(u"Include/exclude Colombia in/from timeseries plotting"))
    self.toolCZ = self.toolbar.AddTool(toolId = self.toolCZ_ID, label = "CZ", bitmap = wx.Bitmap("graphics/flag_CZ_30x20.bmp"), bmpDisabled = wx.Bitmap("graphics/flag_CZ_30x20_disabled.bmp"), kind = wx.ITEM_CHECK, shortHelp = _(u"Czechia"), longHelp = _(u"Include/exclude Czechia in/from timeseries plotting"))
    self.toolDE = self.toolbar.AddTool(toolId = self.toolDE_ID, label = "DE", bitmap = wx.Bitmap("graphics/flag_DE_33x20.bmp"), bmpDisabled = wx.Bitmap("graphics/flag_DE_33x20_disabled.bmp"), kind = wx.ITEM_CHECK, shortHelp = _(u"Germany"), longHelp = _(u"Include/exclude Germany in/from timeseries plotting"))
    self.toolES = self.toolbar.AddTool(toolId = self.toolES_ID, label = "ES", bitmap = wx.Bitmap("graphics/flag_ES_30x20.bmp"), bmpDisabled = wx.Bitmap("graphics/flag_ES_30x20_disabled.bmp"), kind = wx.ITEM_CHECK, shortHelp = _(u"Spain"), longHelp = _(u"Include/exclude Spain in/from timeseries plotting"))
    self.toolFR = self.toolbar.AddTool(toolId = self.toolFR_ID, label = "FR", bitmap = wx.Bitmap("graphics/flag_FR_30x20.bmp"), bmpDisabled = wx.Bitmap("graphics/flag_FR_30x20_disabled.bmp"), kind = wx.ITEM_CHECK, shortHelp = _(u"France"), longHelp = _(u"Include/exclude France in/from timeseries plotting"))
    self.toolGB = self.toolbar.AddTool(toolId = self.toolGB_ID, label = "GB", bitmap = wx.Bitmap("graphics/flag_GB_40x20.bmp"), bmpDisabled = wx.Bitmap("graphics/flag_GB_40x20_disabled.bmp"), kind = wx.ITEM_CHECK, shortHelp = _(u"United Kingdom"), longHelp = _(u"Include/exclude United Kingdom in/from timeseries plotting"))
    self.toolGR = self.toolbar.AddTool(toolId = self.toolGR_ID, label = "GR", bitmap = wx.Bitmap("graphics/flag_GR_30x20.bmp"), bmpDisabled = wx.Bitmap("graphics/flag_GR_30x20_disabled.bmp"), kind = wx.ITEM_CHECK, shortHelp = _(u"Greece"), longHelp = _(u"Include/exclude Greece in/from timeseries plotting"))
    self.toolMX = self.toolbar.AddTool(toolId = self.toolMX_ID, label = "MX", bitmap = wx.Bitmap("graphics/flag_MX_35x20.bmp"), bmpDisabled = wx.Bitmap("graphics/flag_MX_35x20_disabled.bmp"), kind = wx.ITEM_CHECK, shortHelp = _(u"Mexico"), longHelp = _(u"Include/exclude Mexico in/from timeseries plotting"))
    self.toolSE = self.toolbar.AddTool(toolId = self.toolSE_ID, label = "SE", bitmap = wx.Bitmap("graphics/flag_SE_32x20.bmp"), bmpDisabled = wx.Bitmap("graphics/flag_SE_32x20_disabled.bmp"), kind = wx.ITEM_CHECK, shortHelp = _(u"Sweden"), longHelp = _(u"Include/exclude Sweden in/from timeseries plotting"))
    self.toolSK = self.toolbar.AddTool(toolId = self.toolSK_ID, label = "SK", bitmap = wx.Bitmap("graphics/flag_SK_30x20.bmp"), bmpDisabled = wx.Bitmap("graphics/flag_SK_30x20_disabled.bmp"), kind = wx.ITEM_CHECK, shortHelp = _(u"Slovakia"), longHelp = _(u"Include/exclude Slovakia in/from timeseries plotting"))
    self.toolNone = self.toolbar.AddTool(toolId = self.toolNone_ID, label = _(u"none  "), bitmap = wx.Bitmap("graphics/transparent_1x1.bmp"), bmpDisabled = wx.Bitmap("graphics/transparent_1x1.bmp"), kind = wx.ITEM_NORMAL, shortHelp = _(u"Select no country (Ctrl+N)"), longHelp = _(u"Exclude all countries from timeseries plotting (Ctrl+N)"))
    self.toolAll = self.toolbar.AddTool(toolId = self.toolAll_ID, label = _(u"all  "), bitmap = wx.Bitmap("graphics/transparent_1x1.bmp"), bmpDisabled = wx.Bitmap("graphics/transparent_1x1.bmp"), kind = wx.ITEM_NORMAL, shortHelp = _(u"Select all countries (Ctrl+A)"), longHelp = _(u"Include all countries in timeseries plotting (Ctrl+A)"))
    self.toolbar.AddSeparator()
    self.toolLangEn = self.toolbar.AddTool(toolId = self.toolLangEnID, label = "en  ", bitmap = wx.Bitmap("graphics/transparent_1x1.bmp"), shortHelp = _(u"English"), kind = wx.ITEM_RADIO)
    self.toolLangDe = self.toolbar.AddTool(toolId = self.toolLangDeID, label = "de  ", bitmap = wx.Bitmap("graphics/transparent_1x1.bmp"), shortHelp = _(u"German"), kind = wx.ITEM_RADIO)
    self.toolbar.Realize()

    # disable countries at startup because no json file is loaded yet
    self.countriesEnable(False)

    # statusbar at the bottom of the frame
    self.CreateStatusBar()

    # matplotlib plot(s) in the centre of the frame
    # self.plot = wxMatPlotLib.Plot(self)
    self.plotNotebook = wxMatPlotLib.PlotNotebook(self)


  def bindUI(self):
    """
    Generate the event handling bindings
    """

    self.Bind(event = wx.EVT_MENU, handler = self.download, source = self.menuFileDownload)
    self.Bind(event = wx.EVT_MENU, handler = self.open, source = self.menuFileOpen)
    self.Bind(event = wx.EVT_MENU, handler = self.menuFileAF_click, source = self.menuFileAF)
    self.Bind(event = wx.EVT_MENU, handler = self.menuFileCO_click, source = self.menuFileCO)
    self.Bind(event = wx.EVT_MENU, handler = self.menuFileCZ_click, source = self.menuFileCZ)
    self.Bind(event = wx.EVT_MENU, handler = self.menuFileDE_click, source = self.menuFileDE)
    self.Bind(event = wx.EVT_MENU, handler = self.menuFileES_click, source = self.menuFileES)
    self.Bind(event = wx.EVT_MENU, handler = self.menuFileFR_click, source = self.menuFileFR)
    self.Bind(event = wx.EVT_MENU, handler = self.menuFileGB_click, source = self.menuFileGB)
    self.Bind(event = wx.EVT_MENU, handler = self.menuFileGR_click, source = self.menuFileGR)
    self.Bind(event = wx.EVT_MENU, handler = self.menuFileMX_click, source = self.menuFileMX)
    self.Bind(event = wx.EVT_MENU, handler = self.menuFileSE_click, source = self.menuFileSE)
    self.Bind(event = wx.EVT_MENU, handler = self.menuFileSK_click, source = self.menuFileSK)
    self.Bind(event = wx.EVT_MENU, handler = self.countriesSelectNone, source = self.menuFileNone)
    self.Bind(event = wx.EVT_MENU, handler = self.countriesSelectAll, source = self.menuFileAll)
    self.Bind(event = wx.EVT_MENU, handler = self.menuFileLangEn_onClick, source = self.menuFileLangEn)
    self.Bind(event = wx.EVT_MENU, handler = self.menuFileLangDe_onClick, source = self.menuFileLangDe)
    self.Bind(event = wx.EVT_MENU, handler = self.menuHelpAbout_onClick, source = self.menuHelpAbout)

    self.Bind(event = wx.EVT_TOOL, handler = self.download, source = self.toolDownload)
    self.Bind(event = wx.EVT_TOOL, handler = self.open, source = self.toolOpen)
    self.Bind(event = wx.EVT_TOOL, handler = self.toolAF_click, source = self.toolAF)
    self.Bind(event = wx.EVT_TOOL, handler = self.toolCO_click, source = self.toolCO)
    self.Bind(event = wx.EVT_TOOL, handler = self.toolCZ_click, source = self.toolCZ)
    self.Bind(event = wx.EVT_TOOL, handler = self.toolDE_click, source = self.toolDE)
    self.Bind(event = wx.EVT_TOOL, handler = self.toolES_click, source = self.toolES)
    self.Bind(event = wx.EVT_TOOL, handler = self.toolFR_click, source = self.toolFR)
    self.Bind(event = wx.EVT_TOOL, handler = self.toolGB_click, source = self.toolGB)
    self.Bind(event = wx.EVT_TOOL, handler = self.toolGR_click, source = self.toolGR)
    self.Bind(event = wx.EVT_TOOL, handler = self.toolMX_click, source = self.toolMX)
    self.Bind(event = wx.EVT_TOOL, handler = self.toolSE_click, source = self.toolSE)
    self.Bind(event = wx.EVT_TOOL, handler = self.toolSK_click, source = self.toolSK)
    self.Bind(event = wx.EVT_TOOL, handler = self.countriesSelectNone, source = self.toolNone)
    self.Bind(event = wx.EVT_TOOL, handler = self.countriesSelectAll, source = self.toolAll)
    self.Bind(event = wx.EVT_TOOL, handler = self.menuFileLangEn_onClick, source = self.toolLangEn)
    self.Bind(event = wx.EVT_TOOL, handler = self.menuFileLangDe_onClick, source = self.toolLangDe)


  # keep the toolbar buttons in sync with the file menu buttons

  def menuFileAF_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolAF_ID, toggle = self.menuFileAF.IsChecked())
    self.plotAllTimeseries()
  def menuFileCO_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolCO_ID, toggle = self.menuFileCO.IsChecked())
    self.plotAllTimeseries()
  def menuFileCZ_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolCZ_ID, toggle = self.menuFileCZ.IsChecked())
    self.plotAllTimeseries()
  def menuFileDE_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolDE_ID, toggle = self.menuFileDE.IsChecked())
    self.plotAllTimeseries()
  def menuFileES_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolES_ID, toggle = self.menuFileES.IsChecked())
    self.plotAllTimeseries()
  def menuFileFR_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolFR_ID, toggle = self.menuFileFR.IsChecked())
    self.plotAllTimeseries()
  def menuFileGB_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolGB_ID, toggle = self.menuFileGB.IsChecked())
    self.plotAllTimeseries()
  def menuFileGR_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolGR_ID, toggle = self.menuFileGR.IsChecked())
    self.plotAllTimeseries()
  def menuFileMX_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolMX_ID, toggle = self.menuFileMX.IsChecked())
    self.plotAllTimeseries()
  def menuFileSE_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolSE_ID, toggle = self.menuFileSE.IsChecked())
    self.plotAllTimeseries()
  def menuFileSK_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolSK_ID, toggle = self.menuFileSK.IsChecked())
    self.plotAllTimeseries()

  # keep the file menu buttons in sync with the toolbar buttons

  def toolAF_click(self, event):
    self.menuFileAF.Check(self.toolbar.GetToolState(self.toolAF_ID))
    self.plotAllTimeseries()
  def toolCO_click(self, event):
    self.menuFileCO.Check(self.toolbar.GetToolState(self.toolCO_ID))
    self.plotAllTimeseries()
  def toolCZ_click(self, event):
    self.menuFileCZ.Check(self.toolbar.GetToolState(self.toolCZ_ID))
    self.plotAllTimeseries()
  def toolDE_click(self, event):
    self.menuFileDE.Check(self.toolbar.GetToolState(self.toolDE_ID))
    self.plotAllTimeseries()
  def toolES_click(self, event):
    self.menuFileES.Check(self.toolbar.GetToolState(self.toolES_ID))
    self.plotAllTimeseries()
  def toolFR_click(self, event):
    self.menuFileFR.Check(self.toolbar.GetToolState(self.toolFR_ID))
    self.plotAllTimeseries()
  def toolGB_click(self, event):
    self.menuFileGB.Check(self.toolbar.GetToolState(self.toolGB_ID))
    self.plotAllTimeseries()
  def toolGR_click(self, event):
    self.menuFileGR.Check(self.toolbar.GetToolState(self.toolGR_ID))
    self.plotAllTimeseries()
  def toolMX_click(self, event):
    self.menuFileMX.Check(self.toolbar.GetToolState(self.toolMX_ID))
    self.plotAllTimeseries()
  def toolSE_click(self, event):
    self.menuFileSE.Check(self.toolbar.GetToolState(self.toolSE_ID))
    self.plotAllTimeseries()
  def toolSK_click(self, event):
    self.menuFileSK.Check(self.toolbar.GetToolState(self.toolSK_ID))
    self.plotAllTimeseries()


  def download(self, event):
    """
    Download COVID-19 timeseries JSON data file from the internet
    """

    # show save file dialog, based on https://wxpython.org/Phoenix/docs/html/wx.FileDialog.html
    with wx.FileDialog(parent = self,
                       message = _(u"Save JSON data file as"),
                       defaultFile = "covid19-timeseries-{}.json".format(datetime.now().strftime("%Y%m%d-%H%M%S")),
                       wildcard = _(u"JSON files (*.json)|*.json|All files|*"),
                       style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as saveFileDialog:
      if saveFileDialog.ShowModal() == wx.ID_CANCEL:
        return

      # download from the internet, based on https://www.simplifiedpython.net/python-download-file/
      filePath = saveFileDialog.GetPath()
      url = "https://pomber.github.io/covid19/timeseries.json"
      self.SetStatusText(_(u"Downloading COVID-19 timeseries JSON data file"))
      urllib.request.urlretrieve(url, filePath)
      self.SetStatusText(_(u"Successfully downloaded COVID-19 timeseries JSON data file to '{}'").format(filePath.split('/')[-1]))
      self.statusTextClearAfterDelay()


  def open(self, event):
    """
    Open and load locally saved COVID-19 timeseries JSON data file
    """

    # show open file dialog, based on https://wxpython.org/Phoenix/docs/html/wx.FileDialog.html
    with wx.FileDialog(parent = self,
                       message = _(u"Open JSON data file"),
                       wildcard = _(u"JSON files (*.json)|*.json|All files|*"),
                       style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as openFileDialog:
      if openFileDialog.ShowModal() == wx.ID_CANCEL:
        return
      filePath = openFileDialog.GetPath()
      try:
        # open JSON file, based on https://www.askpython.com/python/examples/read-a-json-file-in-python
        with open(filePath, "r") as jsonFile:
          self.jsonData = json.load(jsonFile)
      except IOError:
        wx.LogError(_(u"Cannot open file '{}'").format(filePath))
        return

      # enable the country buttons (they are disabled during initGUI)
      self.countriesEnable(True)

      # do something with the data
      self.plotAllTimeseries()

      # simple version - just one individual plot
      # self.plot.figure.gca().plot(*self.getTimeseries(jsonData, 'Afghanistan'), label = 'Afghanistan')
      # self.plot.figure.gca().plot(*self.getTimeseries(jsonData, 'Germany'), label = 'Germany')
      # self.plot.figure.gca().plot(*self.getTimeseries(jsonData, 'Colombia'), label = 'Colombia')
      # self.plot.figure.gca().plot(*self.getTimeseries(jsonData, 'Mexico'), label = 'Mexico')
      # self.plot.figure.gca().legend(loc = 2)
      # self.plot.canvas.draw()


  def countriesEnable(self, enable):
    """
    Enable / disable all country buttons

    :param enable: Whether countries should be enabled (clickable buttons) or disabled (buttons greyed out and unclickable)
    :type enable: bool
    """
    self.menuFileAF.Enable(enable)
    self.menuFileCO.Enable(enable)
    self.menuFileCZ.Enable(enable)
    self.menuFileFR.Enable(enable)
    self.menuFileDE.Enable(enable)
    self.menuFileGR.Enable(enable)
    self.menuFileMX.Enable(enable)
    self.menuFileES.Enable(enable)
    self.menuFileSE.Enable(enable)
    self.menuFileSK.Enable(enable)
    self.menuFileGB.Enable(enable)
    self.menuFileNone.Enable(enable)
    self.menuFileAll.Enable(enable)
    self.toolbar.EnableTool(toolId = self.toolAF_ID, enable = enable)
    self.toolbar.EnableTool(toolId = self.toolCO_ID, enable = enable)
    self.toolbar.EnableTool(toolId = self.toolCZ_ID, enable = enable)
    self.toolbar.EnableTool(toolId = self.toolDE_ID, enable = enable)
    self.toolbar.EnableTool(toolId = self.toolES_ID, enable = enable)
    self.toolbar.EnableTool(toolId = self.toolFR_ID, enable = enable)
    self.toolbar.EnableTool(toolId = self.toolGB_ID, enable = enable)
    self.toolbar.EnableTool(toolId = self.toolGR_ID, enable = enable)
    self.toolbar.EnableTool(toolId = self.toolMX_ID, enable = enable)
    self.toolbar.EnableTool(toolId = self.toolSE_ID, enable = enable)
    self.toolbar.EnableTool(toolId = self.toolSK_ID, enable = enable)
    self.toolbar.EnableTool(toolId = self.toolNone_ID, enable = enable)
    self.toolbar.EnableTool(toolId = self.toolAll_ID, enable = enable)

  def countriesSelectNone(self, event):
    """
    Deselect all coutries and update the plots
    """
    self.countriesSelect(select = False)
    self.plotAllTimeseries()

  def countriesSelectAll(self, event):
    """
    Select all countries and update the plots
    """
    self.countriesSelect(select = True)
    self.plotAllTimeseries()

  def countriesSelect(self, select):
    """
    Adjust the button state of all country buttons according to whether they should be selected or deselected

    :param select: Whether all countries should be selected or deselected
    :type select: bool
    """
    self.menuFileAF.Check(select)
    self.menuFileCO.Check(select)
    self.menuFileCZ.Check(select)
    self.menuFileDE.Check(select)
    self.menuFileES.Check(select)
    self.menuFileFR.Check(select)
    self.menuFileGB.Check(select)
    self.menuFileGR.Check(select)
    self.menuFileMX.Check(select)
    self.menuFileSE.Check(select)
    self.menuFileSK.Check(select)
    self.toolbar.ToggleTool(toolId = self.toolAF_ID, toggle = select)
    self.toolbar.ToggleTool(toolId = self.toolCO_ID, toggle = select)
    self.toolbar.ToggleTool(toolId = self.toolCZ_ID, toggle = select)
    self.toolbar.ToggleTool(toolId = self.toolDE_ID, toggle = select)
    self.toolbar.ToggleTool(toolId = self.toolES_ID, toggle = select)
    self.toolbar.ToggleTool(toolId = self.toolFR_ID, toggle = select)
    self.toolbar.ToggleTool(toolId = self.toolGB_ID, toggle = select)
    self.toolbar.ToggleTool(toolId = self.toolGR_ID, toggle = select)
    self.toolbar.ToggleTool(toolId = self.toolMX_ID, toggle = select)
    self.toolbar.ToggleTool(toolId = self.toolSE_ID, toggle = select)
    self.toolbar.ToggleTool(toolId = self.toolSK_ID, toggle = select)
  
  def countriesActiveBool(self):
    """
    Determine whether at least one country is selected
    """
    return(self.toolbar.GetToolState(self.toolAF_ID) \
        or self.toolbar.GetToolState(self.toolCO_ID) \
        or self.toolbar.GetToolState(self.toolCZ_ID) \
        or self.toolbar.GetToolState(self.toolDE_ID) \
        or self.toolbar.GetToolState(self.toolES_ID) \
        or self.toolbar.GetToolState(self.toolFR_ID) \
        or self.toolbar.GetToolState(self.toolGB_ID) \
        or self.toolbar.GetToolState(self.toolGR_ID) \
        or self.toolbar.GetToolState(self.toolMX_ID) \
        or self.toolbar.GetToolState(self.toolSE_ID) \
        or self.toolbar.GetToolState(self.toolSK_ID))


  def plotAllTimeseries(self):
    """
    Plot the timeseries for all observables
    """
    if not self.countriesActiveBool():
      self.plotNotebook.clear()
      return

    if self.plotNotebook.nb.GetPageCount() == 0:
      self.plotConfirmed = self.plotAddTimeseries(observable = "confirmed", title = _(u"Confirmed"))
      self.plotRecovered = self.plotAddTimeseries(observable = "recovered", title = _(u"Recovered"))
      self.plotDeaths = self.plotAddTimeseries(observable = "deaths", title = _(u"Deaths"))
    else:
      self.plotUpdateTimeseries(plot = self.plotConfirmed, observable = "confirmed")
      self.plotUpdateTimeseries(plot = self.plotRecovered, observable = "recovered")
      self.plotUpdateTimeseries(plot = self.plotDeaths, observable = "deaths")


  def plotAddTimeseries(self, observable, title):
    """
    Create a new :class:`wxMatPlotLib.PlotNotebook` tab and plot the timeseries of a particular observable in it

    :param observable: Must be one of of the following: ``confirmed``, ``recovered``, ``deaths``
    :type observable: string
    """
    plot = self.plotNotebook.add(title)
    self.plotTimeseries(plot, observable)
    return(plot)
  
  def plotUpdateTimeseries(self, plot, observable):
    """
    Clear the figure in an existing :class:`wxMatPlotLib.PlotNotebook` tab and replot the timeseries of a particular observable in it

    This is necessary when the set of selected countries changes.

    :param plot: The plot that is to be updated
    :type plot: :class:`wxMatPlotLib.Plot`
    :param observable: Must be one of of the following: ``confirmed``, ``recovered``, ``deaths``
    :type observable: string
    """
    plot.figure.clear()
    self.plotTimeseries(plot, observable)
    plot.canvas.draw()
  
  def plotTimeseries(self, plot, observable):
    """
    Plot the timeseries of a given observable onto given plot

    :param plot: The plot onto which the timeseries is to be plotted
    :type plot: :class:`wxMatPlotLib.Plot`
    :param observable: Must be one of of the following: ``confirmed``, ``recovered``, ``deaths``
    :type observable: string
    """
    lw = 2.5 # linewidth
    if self.toolbar.GetToolState(self.toolAF_ID): plot.figure.gca().plot(*self.getTimeseries('Afghanistan', observable), label = _(u"Afghanistan"), linewidth = lw)
    if self.toolbar.GetToolState(self.toolCO_ID): plot.figure.gca().plot(*self.getTimeseries('Colombia', observable), label = _(u"Colombia"), linewidth = lw)
    if self.toolbar.GetToolState(self.toolCZ_ID): plot.figure.gca().plot(*self.getTimeseries('Czechia', observable), label = _(u"Czechia"), linewidth = lw)
    if self.toolbar.GetToolState(self.toolFR_ID): plot.figure.gca().plot(*self.getTimeseries('France', observable), label = _(u"France"), linewidth = lw)
    if self.toolbar.GetToolState(self.toolDE_ID): plot.figure.gca().plot(*self.getTimeseries('Germany', observable), label = _(u"Germany"), linewidth = lw)
    if self.toolbar.GetToolState(self.toolGR_ID): plot.figure.gca().plot(*self.getTimeseries('Greece', observable), label = _(u"Greece"), linewidth = lw)
    if self.toolbar.GetToolState(self.toolMX_ID): plot.figure.gca().plot(*self.getTimeseries('Mexico', observable), label = _(u"Mexico"), linewidth = lw)
    if self.toolbar.GetToolState(self.toolES_ID): plot.figure.gca().plot(*self.getTimeseries('Spain', observable), label = _(u"Spain"), linewidth = lw)
    if self.toolbar.GetToolState(self.toolSE_ID): plot.figure.gca().plot(*self.getTimeseries('Sweden', observable), label = _(u"Sweden"), linewidth = lw)
    if self.toolbar.GetToolState(self.toolSK_ID): plot.figure.gca().plot(*self.getTimeseries('Slovakia', observable), label = _(u"Slovakia"), linewidth = lw)
    if self.toolbar.GetToolState(self.toolGB_ID): plot.figure.gca().plot(*self.getTimeseries('United Kingdom', observable), label = _(u"United Kingdom"), linewidth = lw)
    plot.figure.gca().get_yaxis().set_major_formatter(mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',').replace(',', ' ')))
    plot.figure.gca().legend(loc = 2)


  def getTimeseries(self, country, observable = 'confirmed'):
    """
    Get the COVID-19 timeseries of a certain observable for a certain country

    :param country: Country whose timeseries should be returned
    :type country: string
    :param observable: Quantity of interest.
                       Must be one of (``confirmed``, ``recovered``, ``deaths``).
    :type observable: string

    :returns: Tuple (x, y) of the x and y values, which themselves are lists.
              The tuple (x, y) can be unpacked with a preceding asterisk, ``*(x, y)``, when passing it to :mod:`matplotlib`'s plot function.
    """

    x = []
    y = []
    for datapoint in self.jsonData[country]:
      dateString = datapoint['date'].split('-')
      x.append(date(int(dateString[0]), int(dateString[1]), int(dateString[2])))
      y.append(datapoint[observable])
    return(x, y)


  def menuFileLangEn_onClick(self, event):
    """
    Event handling function for interface switch to English

    Since this handler is bound to both the corresponding menu item and the
    corresponding toolbar item, both controls have to be updated / toggled
    to also correctly set / toggle the one that wasn't clicked.

    .. todo:: Actually manipulate the settings and update all relevant texts
    """
    
    self.menuFileLangEn.Check(True)
    self.toolbar.ToggleTool(toolId = self.toolLangEnID, toggle = True)
  
  def menuFileLangDe_onClick(self, event):
    """
    Event handling function for interface switch to English

    Since this handler is bound to both the corresponding menu item and the
    corresponding toolbar item, both controls have to be updated / toggled
    to also correctly set / toggle the one that wasn't clicked.

    .. todo:: Actually manipulate the settings and update all relevant texts
    """
    
    self.menuFileLangDe.Check(True)
    self.toolbar.ToggleTool(toolId = self.toolLangDeID, toggle = True)


  def menuHelpAbout_onClick(self, event):
    """
    Show a message dialog box

    :param self: Self-reference to the class
    :type self: :class:`MainWindow`
    :param event: The event that was triggered
    :type event: :class:`wx.Event`

    :raises: Perhaps this function could throw an exception

    :returns: Nothing
    :rtype: My function doesn't return anything

    Here in this message dialog box, some information about the application could be displayed.
    This could include a description, a version number and possibly also a link to the GitHub repo.

    :example: This is some example, hopefully useful to many people.

    And besides that, I can write a whole lot more.

    .. seealso:: Always try to look beyond the horizon!
    .. warning:: Some warning - be careful
    .. note:: Some note to the reader
    .. todo:: Some todo item
    """

    print("you just clicked on the about menu item")

    # message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
    dlg = wx.MessageDialog(frame, _(u"A plotting tool for COVID-19 data"), _(u"About this program"), wx.OK)
    dlg.SetOKLabel(_(u"OK"))
    dlg.ShowModal() # show it
    dlg.Destroy() # finally destroy it when finished.


  def statusTextClearAfterDelay(self, delay = statusTextClearDelay):
    """
    Clear the status text after a delay

    :param delay: delay in milliseconds
    :type delay: uint
    
    Using ``wx.CallLater``, based on https://realpython.com/python-sleep/#sleeping-in-wxpython
    """

    wx.CallLater(delay, lambda: self.SetStatusText(""))
    # wx.CallLater(delay, self.SetStatusText, "") # alternative implementation


if __name__ == "__main__":
  app = wx.App(redirect = False)

  # internationalisation stuff
  wx.Locale.AddCatalogLookupPathPrefix("locale")
  # language = wx.LANGUAGE_ENGLISH
  language = wx.LANGUAGE_GERMAN
  app.locale = wx.Locale(language)
  app.locale.AddCatalog("wxPythonTestProject")

  frame = MainWindow()
  app.MainLoop()
