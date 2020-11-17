#! /usr/bin/env python3

import wx


class MainWindow(wx.Frame):

  def __init__(self):

    super().__init__(parent = None, title = "Hello World Window Title", size = wx.Size(900, 300))
    self.SetIcon(wx.Icon("graphics/Signal-Uncapped-t0obs.ico")) # https://stackoverflow.com/questions/25002573/how-to-set-icon-on-wxframe
    self.Maximize(True)
    # self.ShowFullScreen(True)

    self.generateUI()
    self.bindUI()

    self.Show(True)


  def generateUI(self):

    # program menubar at the top of the frame
    # list of standard IDs which lead to small icons in the menu: https://wxpython.org/Phoenix/docs/html/wx.StandardID.enumeration.html

    menuFilePaste = wx.Menu()
    menuFilePaste.Append(id = wx.ID_PASTE, item = "with &format", helpString = "Paste string including formatting", kind = wx. ITEM_RADIO)
    menuFilePaste.Append(id = wx.ID_ANY, item = "witho&ut format\tCtrl+U", helpString = "Paste string without formatting", kind = wx. ITEM_RADIO)
    menuFilePaste.AppendSeparator()
    menuFilePaste.Append(id = wx.ID_ANY, item = "Option 1", helpString = "First option", kind = wx. ITEM_RADIO)
    menuFilePaste.Append(id = wx.ID_ANY, item = "Option 2", helpString = "Second option", kind = wx. ITEM_RADIO)
    menuFilePaste.Append(id = wx.ID_ANY, item = "Option 3", helpString = "Third option", kind = wx. ITEM_RADIO)

    menuFile = wx.Menu()
    self.menuFileNew = menuFile.Append(id = wx.ID_NEW, item = "New file\tCtrl+N", helpString = "Create a new file")
    menuFile.AppendSeparator()
    menuFile.Append(id = wx.ID_ANY, item = "Toggle something", helpString = "This is a toggle menu item", kind = wx.ITEM_CHECK)
    menuFile.Append(id = wx.ID_ANY, item = "&Paste", subMenu = menuFilePaste, helpString = "Paste string")
    menuFile.AppendSeparator()
    menuFile.Append(wx.ID_EXIT, "E&xit", " Terminate the program")

    menuHelp = wx.Menu()
    self.menuHelpAbout = menuHelp.Append(id = wx.ID_ABOUT, item = "&About\tCtrl+A", helpString = "Information about this program", kind =  wx.ITEM_NORMAL)

    menubar = wx.MenuBar()
    menubar.Append(menuFile, "&File")
    menubar.Append(menuHelp, "&Help")
    self.SetMenuBar(menubar)

    # toolbar at the top of the frame, just below the menubar

    toolbar = self.CreateToolBar(style = wx.TB_HORZ_TEXT)
    self.toolNew = toolbar.AddTool(toolId = 1, label = "New", bitmap = wx.ArtProvider.GetBitmap(id = wx.ART_NEW), shortHelp = "Create new file (Ctrl+N)")
    toolbar.AddSeparator()
    toolbar.AddTool(toolId = 2, label = "Toggle somthing", bitmap = wx.Bitmap("graphics/complicatedMerged_Var2_noLabel_30pix.bmp"), shortHelp = "Toggle somthing", kind = wx.ITEM_CHECK)
    toolCheck = toolbar.AddTool(toolId = 3, label = "Paste with format", bitmap = wx.Bitmap("graphics/complicatedMerged_Var2_noLabel_30pix.bmp"), shortHelp = "Check something", kind = wx.ITEM_RADIO)
    toolCheck2 = toolbar.AddTool(toolId = 4, label = "Paste without format", bitmap = wx.Bitmap("graphics/complicatedMerged_Var2_noLabel_30pix.bmp"), shortHelp = "Check something", kind = wx.ITEM_RADIO)
    toolbar.AddSeparator()
    toolRadio1 = toolbar.AddTool(toolId = 5, label = "Paste option 1", bitmap = wx.Bitmap("graphics/complicatedMerged_Var2_noLabel_30pix.bmp"), shortHelp = "Drop something", kind = wx.ITEM_RADIO)
    toolRadio2 = toolbar.AddTool(toolId = 6, label = "Paste option 2", bitmap = wx.Bitmap("graphics/complicatedMerged_Var2_noLabel_30pix.bmp"), shortHelp = "Drop something", kind = wx.ITEM_RADIO)
    toolRadio3 = toolbar.AddTool(toolId = 7, label = "Paste option 3", bitmap = wx.Bitmap("graphics/complicatedMerged_Var2_noLabel_30pix.bmp"), shortHelp = "Drop something", kind = wx.ITEM_RADIO)
    toolbar.Realize()

    # statusbar at the bottom of the frame

    self.CreateStatusBar()

    # text control in the centre of the frame

    self.textControl = wx.TextCtrl(self, size = wx.Size(500, 100), style=wx.TE_MULTILINE)


  def bindUI(self):

    self.Bind(event = wx.EVT_MENU, handler = self.menuFileNew_onClick, source = self.menuFileNew)
    self.Bind(event = wx.EVT_MENU, handler = self.menuHelpAbout_onClick, source = self.menuHelpAbout)

    self.Bind(event = wx.EVT_TOOL, handler = self.menuFileNew_onClick, source = self.toolNew)
  

  def menuFileNew_onClick(self, event):

    self.textControl.Clear()
  

  def menuHelpAbout_onClick(self, event):

    print("you just clicked on the about menu item")

    # message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
    dlg = wx.MessageDialog(frame, "A small text editor", "About Sample Editor", wx.OK)
    dlg.ShowModal() # show it
    dlg.Destroy() # finally destroy it when finished.


app = wx.App(redirect = False)
frame = MainWindow()
app.MainLoop()
