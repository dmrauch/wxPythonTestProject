#! /usr/bin/env python3
"""
Nonsensical Python GUI project using wxPython

This is just to educate myself, nothing here has any real sense.
"""

from datetime import date
from datetime import datetime
import json
import urllib.request
import wx
import wxMatPlotLib


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

    super().__init__(parent = None, title = "Hello World Window Title", size = wx.Size(900, 600))
    self.SetIcon(wx.Icon("graphics/Signal-Uncapped-t0obs.ico")) # https://stackoverflow.com/questions/25002573/how-to-set-icon-on-wxframe
    # self.Maximize(True)
    # self.ShowFullScreen(True)

    self.generateUI()
    self.bindUI()

    self.Show(True)


  def generateUI(self):
    """
    Generate the GUI
    """

    # program menubar at the top of the frame
    # list of standard IDs which lead to small icons in the menu: https://wxpython.org/Phoenix/docs/html/wx.StandardID.enumeration.html

    menuFilePaste = wx.Menu()
    menuFilePaste.Append(id = wx.ID_PASTE, item = "with &format", helpString = "Paste string including formatting", kind = wx. ITEM_RADIO)
    menuFilePaste.Append(id = wx.ID_ANY, item = "witho&ut format\tCtrl+U", helpString = "Paste string without formatting", kind = wx. ITEM_RADIO)

    menuFileLang = wx.Menu()
    self.menuFileLangEn = menuFileLang.Append(id = wx.ID_ANY, item = "&English\tCtrl+E", helpString = "Show interface in English", kind = wx.ITEM_RADIO)
    self.menuFileLangDe = menuFileLang.Append(id = wx.ID_ANY, item = "&German\tCtrl+G", helpString = "Show interface in German", kind = wx.ITEM_RADIO)

    menuFile = wx.Menu()
    self.menuFileNew = menuFile.Append(id = wx.ID_NEW, item = "New file\tCtrl+N", helpString = "Create a new file")
    self.menuFileDownload = menuFile.Append(id = wx.ID_DOWN, item = "Download\tCtrl+D", helpString = "Download JSON data file from the internet")
    self.menuFileOpen = menuFile.Append(id = wx.ID_OPEN, item = "Open", helpString = "Open local JSON data file")
    menuFile.AppendSeparator()
    menuFile.Append(id = wx.ID_ANY, item = "Toggle something", helpString = "This is a toggle menu item", kind = wx.ITEM_CHECK)
    menuFile.Append(id = wx.ID_ANY, item = "&Paste", subMenu = menuFilePaste, helpString = "Paste string")
    menuFile.Append(id = wx.ID_ANY, item = "&Language", subMenu = menuFileLang, helpString = "Interface language")
    menuFile.AppendSeparator()
    menuFile.Append(wx.ID_EXIT, "E&xit", " Terminate the program")

    menuHelp = wx.Menu()
    self.menuHelpAbout = menuHelp.Append(id = wx.ID_ABOUT, item = "&About\tCtrl+A", helpString = "Information about this program", kind =  wx.ITEM_NORMAL)

    menubar = wx.MenuBar()
    menubar.Append(menuFile, "&File")
    menubar.Append(menuHelp, "&Help")
    self.SetMenuBar(menubar)

    # toolbar at the top of the frame, just below the menubar

    self.toolDownloadID = 8
    self.toolOpenID = 7
    self.toolLangEnID = 5
    self.toolLangDeID = 6
    self.toolbar = self.CreateToolBar(style = wx.TB_HORZ_TEXT)
    self.toolNew = self.toolbar.AddTool(toolId = 1, label = "New", bitmap = wx.ArtProvider.GetBitmap(id = wx.ART_NEW), shortHelp = "Create new file (Ctrl+N)")
    self.toolDownload = self.toolbar.AddTool(toolId = self.toolDownloadID, label = "Download", bitmap = wx.ArtProvider.GetBitmap(id = wx.ART_GO_DOWN), shortHelp = "Download JSON data file from the internet (Ctrl+D)")
    self.toolOpen = self.toolbar.AddTool(toolId = self.toolOpenID, label = "Open", bitmap = wx.ArtProvider.GetBitmap(id = wx.ART_FILE_OPEN), shortHelp = "Open local JSON data file (Ctrl+O)")
    self.toolbar.AddSeparator()
    self.toolbar.AddTool(toolId = 2, label = "Toggle somthing", bitmap = wx.Bitmap("graphics/complicatedMerged_Var2_noLabel_30pix.bmp"), shortHelp = "Toggle somthing", kind = wx.ITEM_CHECK)
    toolCheck = self.toolbar.AddTool(toolId = 3, label = "Paste with format", bitmap = wx.Bitmap("graphics/complicatedMerged_Var2_noLabel_30pix.bmp"), shortHelp = "Check something", kind = wx.ITEM_RADIO)
    toolCheck2 = self.toolbar.AddTool(toolId = 4, label = "Paste without format", bitmap = wx.Bitmap("graphics/complicatedMerged_Var2_noLabel_30pix.bmp"), shortHelp = "Check something", kind = wx.ITEM_RADIO)
    self.toolbar.AddSeparator()
    self.toolLangEn = self.toolbar.AddTool(toolId = self.toolLangEnID, label = "en", bitmap = wx.Bitmap("graphics/lang_en_32x16.bmp"), shortHelp = "English", kind = wx.ITEM_RADIO)
    self.toolLangDe = self.toolbar.AddTool(toolId = self.toolLangDeID, label = "de", bitmap = wx.Bitmap("graphics/lang_de_27x16.bmp"), shortHelp = "German", kind = wx.ITEM_RADIO)
    self.toolbar.Realize()

    # statusbar at the bottom of the frame

    self.CreateStatusBar()

    # matplotlib plot(s) in the centre of the frame
    # self.plot = wxMatPlotLib.Plot(self)
    self.plotNotebook = wxMatPlotLib.PlotNotebook(self)


  def bindUI(self):
    """
    Generate the event handling bindings
    """

    self.Bind(event = wx.EVT_MENU, handler = self.menuFileNew_onClick, source = self.menuFileNew)
    self.Bind(event = wx.EVT_MENU, handler = self.download, source = self.menuFileDownload)
    self.Bind(event = wx.EVT_MENU, handler = self.open, source = self.menuFileOpen)
    self.Bind(event = wx.EVT_MENU, handler = self.menuFileLangEn_onClick, source = self.menuFileLangEn)
    self.Bind(event = wx.EVT_MENU, handler = self.menuFileLangDe_onClick, source = self.menuFileLangDe)
    self.Bind(event = wx.EVT_MENU, handler = self.menuHelpAbout_onClick, source = self.menuHelpAbout)

    self.Bind(event = wx.EVT_TOOL, handler = self.menuFileNew_onClick, source = self.toolNew)
    self.Bind(event = wx.EVT_TOOL, handler = self.download, source = self.toolDownload)
    self.Bind(event = wx.EVT_TOOL, handler = self.open, source = self.toolOpen)
    self.Bind(event = wx.EVT_TOOL, handler = self.menuFileLangEn_onClick, source = self.toolLangEn)
    self.Bind(event = wx.EVT_TOOL, handler = self.menuFileLangDe_onClick, source = self.toolLangDe)
  

  def menuFileNew_onClick(self, event):
    """
    Delete all the text in the textCtrl
    """

    self.textControl.Clear()
  

  def download(self, event):
    """
    Download COVID-19 timeseries JSON data file from the internet
    """

    # show save file dialog, based on https://wxpython.org/Phoenix/docs/html/wx.FileDialog.html
    with wx.FileDialog(parent = self,
                       message = "Save JSON data file as",
                       defaultFile = "covid19-timeseries-{}.json".format(datetime.now().strftime("%Y%m%d-%H%M%S")),
                       wildcard = "JSON files (*.json)|*.json|All files|*",
                       style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as saveFileDialog:
      if saveFileDialog.ShowModal() == wx.ID_CANCEL:
        return

      # download from the internet, based on https://www.simplifiedpython.net/python-download-file/
      filePath = saveFileDialog.GetPath()
      url = "https://pomber.github.io/covid19/timeseries.json"
      self.SetStatusText("Downloading COVID-19 timeseries JSON data file")
      urllib.request.urlretrieve(url, filePath)
      self.SetStatusText("Successfully downloaded COVID-19 timeseries JSON data file to '{}'".format(filePath.split('/')[-1]))
      self.statusTextClearAfterDelay()


  def open(self, event):
    """
    Open and load locally saved COVID-19 timeseries JSON data file
    """

    # show open file dialog, based on https://wxpython.org/Phoenix/docs/html/wx.FileDialog.html
    with wx.FileDialog(parent = self,
                       message = "Open JSON data file",
                       wildcard = "JSON files (*.json)|*.json|All files|*",
                       style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as openFileDialog:
      if openFileDialog.ShowModal() == wx.ID_CANCEL:
        return
      filePath = openFileDialog.GetPath()
      try:
        # open JSON file, based on https://www.askpython.com/python/examples/read-a-json-file-in-python
        with open(filePath, "r") as jsonFile:
          jsonData = json.load(jsonFile)
      except IOError:
        wx.LogError("Cannot open file '{}'".format(filePath))
        return

      # do something with the data

      # simple version - just one individual plot
      # self.plot.figure.gca().plot(*self.getTimeseries(jsonData, 'Afghanistan'), label = 'Afghanistan')
      # self.plot.figure.gca().plot(*self.getTimeseries(jsonData, 'Germany'), label = 'Germany')
      # self.plot.figure.gca().plot(*self.getTimeseries(jsonData, 'Colombia'), label = 'Colombia')
      # self.plot.figure.gca().plot(*self.getTimeseries(jsonData, 'Mexico'), label = 'Mexico')
      # self.plot.figure.gca().legend(loc = 2)
      # self.plot.canvas.draw()

      # more interesting - a notebook with different plots in different tabs
      plotConfirmed = self.plotNotebook.add("Confirmed")
      plotConfirmed.gca().plot(*self.getTimeseries(jsonData, 'Afghanistan'), label = 'Afghanistan')
      plotConfirmed.gca().plot(*self.getTimeseries(jsonData, 'Germany'), label = 'Germany')
      plotConfirmed.gca().plot(*self.getTimeseries(jsonData, 'Colombia'), label = 'Colombia')
      plotConfirmed.gca().plot(*self.getTimeseries(jsonData, 'Mexico'), label = 'Mexico')
      plotConfirmed.gca().legend(loc = 2)
      plotDeaths = self.plotNotebook.add("Deaths")
      plotDeaths.gca().plot(*self.getTimeseries(jsonData, 'Afghanistan', observable = 'deaths'), label = 'Afghanistan')
      plotDeaths.gca().plot(*self.getTimeseries(jsonData, 'Germany', observable = 'deaths'), label = 'Germany')
      plotDeaths.gca().plot(*self.getTimeseries(jsonData, 'Colombia', observable = 'deaths'), label = 'Colombia')
      plotDeaths.gca().plot(*self.getTimeseries(jsonData, 'Mexico', observable = 'deaths'), label = 'Mexico')
      plotDeaths.gca().legend(loc = 2)
      plotRecovered = self.plotNotebook.add("Recovered")
      plotRecovered.gca().plot(*self.getTimeseries(jsonData, 'Afghanistan', observable = 'recovered'), label = 'Afghanistan')
      plotRecovered.gca().plot(*self.getTimeseries(jsonData, 'Germany', observable = 'recovered'), label = 'Germany')
      plotRecovered.gca().plot(*self.getTimeseries(jsonData, 'Colombia', observable = 'recovered'), label = 'Colombia')
      plotRecovered.gca().plot(*self.getTimeseries(jsonData, 'Mexico', observable = 'recovered'), label = 'Mexico')
      plotRecovered.gca().legend(loc = 2)


  def getTimeseries(self, data, country, observable = 'confirmed'):
    """
    Get the COVID-19 timeseries of a certain observable for a certain country

    :param data: Dataset containing the COVID-19 data
    :type data: JSON object
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
    for datapoint in data[country]:
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
    dlg = wx.MessageDialog(frame, "A small text editor", "About Sample Editor", wx.OK)
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
  frame = MainWindow()
  app.MainLoop()
