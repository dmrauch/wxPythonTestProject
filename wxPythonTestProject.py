#! /usr/bin/env python3
"""
Nonsensical Python GUI project using wxPython

This is just to educate myself, nothing here has any real sense.
"""

import builtins
from datetime import date
from datetime import datetime
import gettext
import json
import matplotlib as mpl
import os
import sys
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

    In case the application is run from a bundle created with PyInstaller, resources such as icons, bitmaps and internationalisation files are not available in the application folder  but rather in a temporary directory accessible via :code:`sys._MEIPASS`.
    Based on https://pyinstaller.readthedocs.io/en/stable/runtime-information.html
    """
    super().__init__(parent = None, title = "COVID-19 Data Plotter", size = wx.Size(1200, 800))

    # special treatment of resource files for bundled application
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
      self.graphicsPath = os.path.join(sys._MEIPASS, "graphics")
      self.localePath = os.path.join(sys._MEIPASS, "locale")
    else:
      self.graphicsPath = "graphics"
      self.localePath = "locale"

    self.appName = os.path.split(os.path.realpath(__file__))[1].replace(".py", "")
    self.appPath = os.path.split(os.path.realpath(__file__))[0]
    self.SetIcon(wx.Icon(os.path.join(self.graphicsPath, "logo.ico"))) # https://stackoverflow.com/questions/25002573/how-to-set-icon-on-wxframe
    # self.Maximize(True)

    self.initialiseSettings()
    self.initialiseLanguages()
    self.generateUI()
    self.bindUI()
    self.toggleLanguageButtons()

    self.Show(True)


  def initialiseSettings(self):
    """
    Create the ``self.appConfig`` settings object
    and create the settings file if does not yet exist
    """
    fileName = os.path.join(self.appPath, self.appName) + ".config"
    self.appConfig = wx.FileConfig(appName = self.appName, localFilename = fileName)

    if not self.appConfig.HasEntry("Language"):
      self.appConfig.Write(key = "Language", value = "en")

    self.appConfig.Flush()


  def initialiseLanguages(self):
    """
    Load all languages and apply the appropriate settings

    The English version of the UI is included in the source code already and therefore not loaded explicitly.
    """
    self.languages = {}
    self.loadLanguage("de") # German

    if "de" in self.languages and self.appConfig.Read(key = "Language") == "de":
      self.language = wx.LANGUAGE_GERMAN
      self.languages["de"].install()
    else:
      self.language = wx.LANGUAGE_ENGLISH
    self.locale = wx.Locale(self.language, wx.LOCALE_LOAD_DEFAULT)


  def loadLanguage(self, lang):
    """
    Load the translation from the corresponding .mo file
    and provide a :class:`gettext.Translations` instance in the ``self.languages`` dict

    :param lang: The two-character language identifier (e.g. "en", "de")
    :type lang: string
    """
    dir = os.path.join(self.localePath, lang, "LC_MESSAGES", "{}.mo".format(self.appName))
    if os.path.exists(dir):
      self.languages[lang] = gettext.translation(domain = self.appName, localedir = self.localePath, languages = [lang])

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

    menuFile = wx.Menu()
    self.menuFileDownload = menuFile.Append(id = wx.ID_DOWN, item = _(u"&Download\tCtrl+D"), helpString = _(u"Download JSON data file from the internet"))
    self.menuFileOpen = menuFile.Append(id = wx.ID_OPEN, item = _(u"&Open"), helpString = _(u"Open local JSON data file"))
    # menuFile.AppendSeparator()
    menuFile.Append(wx.ID_EXIT, _(u"E&xit"), _(u"Terminate the program"))

    menuCountries = wx.Menu()
    self.menuAF = menuCountries.Append(id = wx.ID_ANY, item = _(u"AF / Afghanistan"), kind = wx.ITEM_CHECK)
    self.menuCO = menuCountries.Append(id = wx.ID_ANY, item = _(u"CO / Colombia"), kind = wx.ITEM_CHECK)
    self.menuCZ = menuCountries.Append(id = wx.ID_ANY, item = _(u"CZ / Czechia"), kind = wx.ITEM_CHECK)
    self.menuDE = menuCountries.Append(id = wx.ID_ANY, item = _(u"DE / Germany"), kind = wx.ITEM_CHECK)
    self.menuES = menuCountries.Append(id = wx.ID_ANY, item = _(u"ES / Spain"), kind = wx.ITEM_CHECK)
    self.menuFR = menuCountries.Append(id = wx.ID_ANY, item = _(u"FR / France"), kind = wx.ITEM_CHECK)
    self.menuGB = menuCountries.Append(id = wx.ID_ANY, item = _(u"GB / United Kingdom"), kind = wx.ITEM_CHECK)
    self.menuGR = menuCountries.Append(id = wx.ID_ANY, item = _(u"GR / Greece"), kind = wx.ITEM_CHECK)
    self.menuMX = menuCountries.Append(id = wx.ID_ANY, item = _(u"MX / Mexico"), kind = wx.ITEM_CHECK)
    self.menuSE = menuCountries.Append(id = wx.ID_ANY, item = _(u"SE / Sweden"), kind = wx.ITEM_CHECK)
    self.menuSK = menuCountries.Append(id = wx.ID_ANY, item = _(u"SK / Slovakia"), kind = wx.ITEM_CHECK)
    menuCountries.AppendSeparator()
    self.menuCountriesNone = menuCountries.Append(id = wx.ID_ANY, item = _(u"Select &none\tCtrl+N"))
    self.menuCountriesAll = menuCountries.Append(id = wx.ID_ANY, item = _(u"Select &all\tCtrl+A"))

    menuLang = wx.Menu()
    self.menuLangEn = menuLang.Append(id = wx.ID_ANY, item = _("&English\tCtrl+E"), helpString = _(u"Show interface in English"), kind = wx.ITEM_RADIO)
    self.menuLangDe = menuLang.Append(id = wx.ID_ANY, item = _("&German\tCtrl+G"), helpString = _(u"Show interface in German"), kind = wx.ITEM_RADIO)

    menuView = wx.Menu()
    menuView.Append(id = wx.ID_ANY, item = _(u"&Countries"), subMenu = menuCountries, helpString = _(u"Country selection for timeseries plotting"))
    menuView.Append(id = wx.ID_ANY, item = _(u"&Language"), subMenu = menuLang, helpString = _(u"Interface language"))
    self.menuFullScreen = menuView.Append(id = wx.ID_ANY, item = _(u"&Fullscreen\tCtrl+F"), kind = wx.ITEM_CHECK, helpString = _(u"Show interface in fullscreen mode"))

    menuHelp = wx.Menu()
    self.menuHelpAbout = menuHelp.Append(id = wx.ID_ABOUT, item = _(u"A&bout\tCtrl+B"), helpString = _(u"Information about this program"), kind =  wx.ITEM_NORMAL)

    self.menubar = wx.MenuBar()
    self.menubar.Append(menuFile, _(u"&File"))
    self.menubar.Append(menuView, _(u"&View"))
    self.menubar.Append(menuHelp, _(u"&Help"))
    self.SetMenuBar(self.menubar)

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
    self.toolFullScreenID = 33
    self.toolbar = self.CreateToolBar(style = wx.TB_HORZ_TEXT)
    self.toolDownload = self.toolbar.AddTool(toolId = self.toolDownloadID, label = _(u"Download"), bitmap = wx.ArtProvider.GetBitmap(id = wx.ART_GO_DOWN), shortHelp = _(u"Download JSON data file from the internet (Ctrl+D)"))
    self.toolOpen = self.toolbar.AddTool(toolId = self.toolOpenID, label = _(u"Open"), bitmap = wx.ArtProvider.GetBitmap(id = wx.ART_FILE_OPEN), shortHelp = _(u"Open local JSON data file (Ctrl+O)"))
    self.toolbar.AddSeparator()
    self.toolAF = self.toolbar.AddTool(toolId = self.toolAF_ID, label = "AF", bitmap = wx.Bitmap(os.path.join(self.graphicsPath, "flag_AF_30x20.bmp")), bmpDisabled = wx.Bitmap(os.path.join(self.graphicsPath, "flag_AF_30x20_disabled.bmp")), kind = wx.ITEM_CHECK, shortHelp = _(u"Afghanistan"), longHelp = _(u"Include/exclude Afghanistan in/from timeseries plotting"))
    self.toolCO = self.toolbar.AddTool(toolId = self.toolCO_ID, label = "CO", bitmap = wx.Bitmap(os.path.join(self.graphicsPath, "flag_CO_30x20.bmp")), bmpDisabled = wx.Bitmap(os.path.join(self.graphicsPath, "flag_CO_30x20_disabled.bmp")), kind = wx.ITEM_CHECK, shortHelp = _(u"Colombia"), longHelp = _(u"Include/exclude Colombia in/from timeseries plotting"))
    self.toolCZ = self.toolbar.AddTool(toolId = self.toolCZ_ID, label = "CZ", bitmap = wx.Bitmap(os.path.join(self.graphicsPath, "flag_CZ_30x20.bmp")), bmpDisabled = wx.Bitmap(os.path.join(self.graphicsPath, "flag_CZ_30x20_disabled.bmp")), kind = wx.ITEM_CHECK, shortHelp = _(u"Czechia"), longHelp = _(u"Include/exclude Czechia in/from timeseries plotting"))
    self.toolDE = self.toolbar.AddTool(toolId = self.toolDE_ID, label = "DE", bitmap = wx.Bitmap(os.path.join(self.graphicsPath, "flag_DE_33x20.bmp")), bmpDisabled = wx.Bitmap(os.path.join(self.graphicsPath, "flag_DE_33x20_disabled.bmp")), kind = wx.ITEM_CHECK, shortHelp = _(u"Germany"), longHelp = _(u"Include/exclude Germany in/from timeseries plotting"))
    self.toolES = self.toolbar.AddTool(toolId = self.toolES_ID, label = "ES", bitmap = wx.Bitmap(os.path.join(self.graphicsPath, "flag_ES_30x20.bmp")), bmpDisabled = wx.Bitmap(os.path.join(self.graphicsPath, "flag_ES_30x20_disabled.bmp")), kind = wx.ITEM_CHECK, shortHelp = _(u"Spain"), longHelp = _(u"Include/exclude Spain in/from timeseries plotting"))
    self.toolFR = self.toolbar.AddTool(toolId = self.toolFR_ID, label = "FR", bitmap = wx.Bitmap(os.path.join(self.graphicsPath, "flag_FR_30x20.bmp")), bmpDisabled = wx.Bitmap(os.path.join(self.graphicsPath, "flag_FR_30x20_disabled.bmp")), kind = wx.ITEM_CHECK, shortHelp = _(u"France"), longHelp = _(u"Include/exclude France in/from timeseries plotting"))
    self.toolGB = self.toolbar.AddTool(toolId = self.toolGB_ID, label = "GB", bitmap = wx.Bitmap(os.path.join(self.graphicsPath, "flag_GB_40x20.bmp")), bmpDisabled = wx.Bitmap(os.path.join(self.graphicsPath, "flag_GB_40x20_disabled.bmp")), kind = wx.ITEM_CHECK, shortHelp = _(u"United Kingdom"), longHelp = _(u"Include/exclude United Kingdom in/from timeseries plotting"))
    self.toolGR = self.toolbar.AddTool(toolId = self.toolGR_ID, label = "GR", bitmap = wx.Bitmap(os.path.join(self.graphicsPath, "flag_GR_30x20.bmp")), bmpDisabled = wx.Bitmap(os.path.join(self.graphicsPath, "flag_GR_30x20_disabled.bmp")), kind = wx.ITEM_CHECK, shortHelp = _(u"Greece"), longHelp = _(u"Include/exclude Greece in/from timeseries plotting"))
    self.toolMX = self.toolbar.AddTool(toolId = self.toolMX_ID, label = "MX", bitmap = wx.Bitmap(os.path.join(self.graphicsPath, "flag_MX_35x20.bmp")), bmpDisabled = wx.Bitmap(os.path.join(self.graphicsPath, "flag_MX_35x20_disabled.bmp")), kind = wx.ITEM_CHECK, shortHelp = _(u"Mexico"), longHelp = _(u"Include/exclude Mexico in/from timeseries plotting"))
    self.toolSE = self.toolbar.AddTool(toolId = self.toolSE_ID, label = "SE", bitmap = wx.Bitmap(os.path.join(self.graphicsPath, "flag_SE_32x20.bmp")), bmpDisabled = wx.Bitmap(os.path.join(self.graphicsPath, "flag_SE_32x20_disabled.bmp")), kind = wx.ITEM_CHECK, shortHelp = _(u"Sweden"), longHelp = _(u"Include/exclude Sweden in/from timeseries plotting"))
    self.toolSK = self.toolbar.AddTool(toolId = self.toolSK_ID, label = "SK", bitmap = wx.Bitmap(os.path.join(self.graphicsPath, "flag_SK_30x20.bmp")), bmpDisabled = wx.Bitmap(os.path.join(self.graphicsPath, "flag_SK_30x20_disabled.bmp")), kind = wx.ITEM_CHECK, shortHelp = _(u"Slovakia"), longHelp = _(u"Include/exclude Slovakia in/from timeseries plotting"))
    self.toolNone = self.toolbar.AddTool(toolId = self.toolNone_ID, label = _(u"none  "), bitmap = wx.Bitmap(os.path.join(self.graphicsPath, "transparent_1x1.bmp")), bmpDisabled = wx.Bitmap(os.path.join(self.graphicsPath, "transparent_1x1.bmp")), kind = wx.ITEM_NORMAL, shortHelp = _(u"Select no country (Ctrl+N)"), longHelp = _(u"Exclude all countries from timeseries plotting (Ctrl+N)"))
    self.toolAll = self.toolbar.AddTool(toolId = self.toolAll_ID, label = _(u"all  "), bitmap = wx.Bitmap(os.path.join(self.graphicsPath, "transparent_1x1.bmp")), bmpDisabled = wx.Bitmap(os.path.join(self.graphicsPath, "transparent_1x1.bmp")), kind = wx.ITEM_NORMAL, shortHelp = _(u"Select all countries (Ctrl+A)"), longHelp = _(u"Include all countries in timeseries plotting (Ctrl+A)"))
    self.toolbar.AddSeparator()
    self.toolLangEn = self.toolbar.AddTool(toolId = self.toolLangEnID, label = "en  ", bitmap = wx.Bitmap(os.path.join(self.graphicsPath, "transparent_1x1.bmp")), shortHelp = _(u"English"), kind = wx.ITEM_RADIO)
    self.toolLangDe = self.toolbar.AddTool(toolId = self.toolLangDeID, label = "de  ", bitmap = wx.Bitmap(os.path.join(self.graphicsPath, "transparent_1x1.bmp")), shortHelp = _(u"German"), kind = wx.ITEM_RADIO)
    self.toolbar.AddSeparator()
    self.toolFullScreen = self.toolbar.AddTool(toolId = self.toolFullScreenID, label = "", bitmap = wx.Bitmap(os.path.join(self.graphicsPath, "fullscreen_34x24.bmp")), kind = wx.ITEM_CHECK, shortHelp = _(u"Fullscreen"))
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
    self.Bind(event = wx.EVT_MENU, handler = self.menuAF_click, source = self.menuAF)
    self.Bind(event = wx.EVT_MENU, handler = self.menuCO_click, source = self.menuCO)
    self.Bind(event = wx.EVT_MENU, handler = self.menuCZ_click, source = self.menuCZ)
    self.Bind(event = wx.EVT_MENU, handler = self.menuDE_click, source = self.menuDE)
    self.Bind(event = wx.EVT_MENU, handler = self.menuES_click, source = self.menuES)
    self.Bind(event = wx.EVT_MENU, handler = self.menuFR_click, source = self.menuFR)
    self.Bind(event = wx.EVT_MENU, handler = self.menuGB_click, source = self.menuGB)
    self.Bind(event = wx.EVT_MENU, handler = self.menuGR_click, source = self.menuGR)
    self.Bind(event = wx.EVT_MENU, handler = self.menuMX_click, source = self.menuMX)
    self.Bind(event = wx.EVT_MENU, handler = self.menuSE_click, source = self.menuSE)
    self.Bind(event = wx.EVT_MENU, handler = self.menuSK_click, source = self.menuSK)
    self.Bind(event = wx.EVT_MENU, handler = self.countriesSelectNone, source = self.menuCountriesNone)
    self.Bind(event = wx.EVT_MENU, handler = self.countriesSelectAll, source = self.menuCountriesAll)
    self.Bind(event = wx.EVT_MENU, handler = self.menuLangEn_onClick, source = self.menuLangEn)
    self.Bind(event = wx.EVT_MENU, handler = self.menuLangDe_onClick, source = self.menuLangDe)
    self.Bind(event = wx.EVT_MENU, handler = self.fullscreen, source = self.menuFullScreen)
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
    self.Bind(event = wx.EVT_TOOL, handler = self.menuLangEn_onClick, source = self.toolLangEn)
    self.Bind(event = wx.EVT_TOOL, handler = self.menuLangDe_onClick, source = self.toolLangDe)
    self.Bind(event = wx.EVT_TOOL, handler = self.fullscreen, source = self.toolFullScreen)


  # keep the toolbar buttons in sync with the file menu buttons

  def menuAF_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolAF_ID, toggle = self.menuAF.IsChecked())
    self.plotAllTimeseries()
  def menuCO_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolCO_ID, toggle = self.menuCO.IsChecked())
    self.plotAllTimeseries()
  def menuCZ_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolCZ_ID, toggle = self.menuCZ.IsChecked())
    self.plotAllTimeseries()
  def menuDE_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolDE_ID, toggle = self.menuDE.IsChecked())
    self.plotAllTimeseries()
  def menuES_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolES_ID, toggle = self.menuES.IsChecked())
    self.plotAllTimeseries()
  def menuFR_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolFR_ID, toggle = self.menuFR.IsChecked())
    self.plotAllTimeseries()
  def menuGB_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolGB_ID, toggle = self.menuGB.IsChecked())
    self.plotAllTimeseries()
  def menuGR_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolGR_ID, toggle = self.menuGR.IsChecked())
    self.plotAllTimeseries()
  def menuMX_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolMX_ID, toggle = self.menuMX.IsChecked())
    self.plotAllTimeseries()
  def menuSE_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolSE_ID, toggle = self.menuSE.IsChecked())
    self.plotAllTimeseries()
  def menuSK_click(self, event):
    self.toolbar.ToggleTool(toolId = self.toolSK_ID, toggle = self.menuSK.IsChecked())
    self.plotAllTimeseries()

  # keep the file menu buttons in sync with the toolbar buttons

  def toolAF_click(self, event):
    self.menuAF.Check(self.toolbar.GetToolState(self.toolAF_ID))
    self.plotAllTimeseries()
  def toolCO_click(self, event):
    self.menuCO.Check(self.toolbar.GetToolState(self.toolCO_ID))
    self.plotAllTimeseries()
  def toolCZ_click(self, event):
    self.menuCZ.Check(self.toolbar.GetToolState(self.toolCZ_ID))
    self.plotAllTimeseries()
  def toolDE_click(self, event):
    self.menuDE.Check(self.toolbar.GetToolState(self.toolDE_ID))
    self.plotAllTimeseries()
  def toolES_click(self, event):
    self.menuES.Check(self.toolbar.GetToolState(self.toolES_ID))
    self.plotAllTimeseries()
  def toolFR_click(self, event):
    self.menuFR.Check(self.toolbar.GetToolState(self.toolFR_ID))
    self.plotAllTimeseries()
  def toolGB_click(self, event):
    self.menuGB.Check(self.toolbar.GetToolState(self.toolGB_ID))
    self.plotAllTimeseries()
  def toolGR_click(self, event):
    self.menuGR.Check(self.toolbar.GetToolState(self.toolGR_ID))
    self.plotAllTimeseries()
  def toolMX_click(self, event):
    self.menuMX.Check(self.toolbar.GetToolState(self.toolMX_ID))
    self.plotAllTimeseries()
  def toolSE_click(self, event):
    self.menuSE.Check(self.toolbar.GetToolState(self.toolSE_ID))
    self.plotAllTimeseries()
  def toolSK_click(self, event):
    self.menuSK.Check(self.toolbar.GetToolState(self.toolSK_ID))
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
    self.menuAF.Enable(enable)
    self.menuCO.Enable(enable)
    self.menuCZ.Enable(enable)
    self.menuFR.Enable(enable)
    self.menuDE.Enable(enable)
    self.menuGR.Enable(enable)
    self.menuMX.Enable(enable)
    self.menuES.Enable(enable)
    self.menuSE.Enable(enable)
    self.menuSK.Enable(enable)
    self.menuGB.Enable(enable)
    self.menuCountriesNone.Enable(enable)
    self.menuCountriesAll.Enable(enable)
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
    self.menuAF.Check(select)
    self.menuCO.Check(select)
    self.menuCZ.Check(select)
    self.menuDE.Check(select)
    self.menuES.Check(select)
    self.menuFR.Check(select)
    self.menuGB.Check(select)
    self.menuGR.Check(select)
    self.menuMX.Check(select)
    self.menuSE.Check(select)
    self.menuSK.Check(select)
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
    if self.toolbar.GetToolState(self.toolAF_ID): plot.figure.gca().plot(*self.getTimeseries('Afghanistan', observable), label = _(u"AF / Afghanistan"), linewidth = lw)
    if self.toolbar.GetToolState(self.toolCO_ID): plot.figure.gca().plot(*self.getTimeseries('Colombia', observable), label = _(u"CO / Colombia"), linewidth = lw)
    if self.toolbar.GetToolState(self.toolCZ_ID): plot.figure.gca().plot(*self.getTimeseries('Czechia', observable), label = _(u"CZ / Czechia"), linewidth = lw)
    if self.toolbar.GetToolState(self.toolDE_ID): plot.figure.gca().plot(*self.getTimeseries('Germany', observable), label = _(u"DE / Germany"), linewidth = lw)
    if self.toolbar.GetToolState(self.toolES_ID): plot.figure.gca().plot(*self.getTimeseries('Spain', observable), label = _(u"ES / Spain"), linewidth = lw)
    if self.toolbar.GetToolState(self.toolFR_ID): plot.figure.gca().plot(*self.getTimeseries('France', observable), label = _(u"FR / France"), linewidth = lw)
    if self.toolbar.GetToolState(self.toolGB_ID): plot.figure.gca().plot(*self.getTimeseries('United Kingdom', observable), label = _(u"GB / United Kingdom"), linewidth = lw)
    if self.toolbar.GetToolState(self.toolGR_ID): plot.figure.gca().plot(*self.getTimeseries('Greece', observable), label = _(u"GR / Greece"), linewidth = lw)
    if self.toolbar.GetToolState(self.toolMX_ID): plot.figure.gca().plot(*self.getTimeseries('Mexico', observable), label = _(u"MX / Mexico"), linewidth = lw)
    if self.toolbar.GetToolState(self.toolSE_ID): plot.figure.gca().plot(*self.getTimeseries('Sweden', observable), label = _(u"SE / Sweden"), linewidth = lw)
    if self.toolbar.GetToolState(self.toolSK_ID): plot.figure.gca().plot(*self.getTimeseries('Slovakia', observable), label = _(u"SK / Slovakia"), linewidth = lw)
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


  def menuLangEn_onClick(self, event):
    """
    Event handling function for interface switch to English
    """
    self.language = wx.LANGUAGE_ENGLISH
    self.appConfig.Write(key = "Language", value = "en")
    self.appConfig.Flush()
    self.switchLanguage()

  def menuLangDe_onClick(self, event):
    """
    Event handling function for interface switch to English
    """
    self.language = wx.LANGUAGE_GERMAN
    self.appConfig.Write(key = "Language", value = "de")
    self.appConfig.Flush()
    self.switchLanguage()

  def switchLanguage(self):
    self.toggleLanguageButtons()
    dlg = wx.MessageDialog(self, _(u"Please restart the program for this change to take effect"), style = wx.OK)
    dlg.ShowModal()

  def toggleLanguageButtons(self):
    """
    Update the toggle state of the language buttons

    Since this handler is bound to both the corresponding menu item and the
    corresponding toolbar item, both controls have to be updated / toggled
    to also correctly set / toggle the one that wasn't clicked.
    """
    if self.language == wx.LANGUAGE_ENGLISH:
      self.menuLangEn.Check(True)
      self.toolbar.ToggleTool(toolId = self.toolLangEnID, toggle = True)
    elif self.language == wx.LANGUAGE_GERMAN:
      self.menuLangDe.Check(True)
      self.toolbar.ToggleTool(toolId = self.toolLangDeID, toggle = True)


  def fullscreen(self, event):
    """
    Activate / deactivate fullscreen mode

    Based on https://wiki.wxpython.org/Using%20Frame.ShowFullScreen
    """
    fullscreen = not self.IsFullScreen()
    self.menuFullScreen.Check(fullscreen)
    self.toolbar.ToggleTool(toolId = self.toolFullScreenID, toggle = fullscreen)
    self.ShowFullScreen(fullscreen, style = wx.FULLSCREEN_NOCAPTION | wx.FULLSCREEN_NOMENUBAR | wx.FULLSCREEN_NOSTATUSBAR)


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

  # # internationalisation stuff
  # wx.Locale.AddCatalogLookupPathPrefix("locale")
  # # language = wx.LANGUAGE_ENGLISH
  # language = wx.LANGUAGE_GERMAN
  # app.locale = wx.Locale(language)
  # app.locale.AddCatalog("wxPythonTestProject")

  frame = MainWindow()
  app.MainLoop()
