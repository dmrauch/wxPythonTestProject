#! /usr/bin/env python3
"""
Nonsensical Python GUI project using wxPython

This is just to educate myself, nothing here has any real sense.
"""

import wx


class MainWindow(wx.Frame):
  """
  Main window shown upon startup of the application
  """

  def __init__(self):
    """
    Constructor
    """

    super().__init__(parent = None, title = "Hello World Window Title", size = wx.Size(900, 300))
    self.SetIcon(wx.Icon("graphics/Signal-Uncapped-t0obs.ico")) # https://stackoverflow.com/questions/25002573/how-to-set-icon-on-wxframe
    self.Maximize(True)
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

    self.toolLangEnID = 5
    self.toolLangDeID = 6
    self.toolbar = self.CreateToolBar(style = wx.TB_HORZ_TEXT)
    self.toolNew = self.toolbar.AddTool(toolId = 1, label = "New", bitmap = wx.ArtProvider.GetBitmap(id = wx.ART_NEW), shortHelp = "Create new file (Ctrl+N)")
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

    # text control in the centre of the frame

    self.textControl = wx.TextCtrl(self, size = wx.Size(500, 100), style=wx.TE_MULTILINE)


  def bindUI(self):
    """
    Generate the event handling bindings
    """

    self.Bind(event = wx.EVT_MENU, handler = self.menuFileNew_onClick, source = self.menuFileNew)
    self.Bind(event = wx.EVT_MENU, handler = self.menuFileLangEn_onClick, source = self.menuFileLangEn)
    self.Bind(event = wx.EVT_MENU, handler = self.menuFileLangDe_onClick, source = self.menuFileLangDe)
    self.Bind(event = wx.EVT_MENU, handler = self.menuHelpAbout_onClick, source = self.menuHelpAbout)

    self.Bind(event = wx.EVT_TOOL, handler = self.menuFileNew_onClick, source = self.toolNew)
    self.Bind(event = wx.EVT_TOOL, handler = self.menuFileLangEn_onClick, source = self.toolLangEn)
    self.Bind(event = wx.EVT_TOOL, handler = self.menuFileLangDe_onClick, source = self.toolLangDe)
  

  def menuFileNew_onClick(self, event):
    """
    Delete all the text in the textCtrl
    """

    self.textControl.Clear()
  

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


if __name__ == "__main__":
  app = wx.App(redirect = False)
  frame = MainWindow()
  app.MainLoop()
