#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       pvg.py pysolovideogui
#
#
#       Copyright 2011 Giorgio Gilestro <giorgio@gilest.ro>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#
#

# %%      
""" Import modules """

import wx, os

from pvg_options import optionsFrame

from pvg_acquire import pvg_AcquirePanel as panelOne
from pvg_panel_two import panelLiveView
from pvg_common import options, DEFAULT_CONFIG

import pysolovideo


# %%    
""" Create main window """


class mainFrame(wx.Frame):
# %%
    """ Initialize """

    def __init__(self, *args, **kwds):

        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.__set_properties()     # set window title, position, and size
        self.__do_layout()          # set shape and size of notebook in window.
        self.__menubar__()          # create the menu bar across the top

# %%   
    """ Set the properties of the main window  """

    def __set_properties(self):
        # begin wxGlade: mainFrame.__set_properties
        self.SetTitle("pySoloVideo")            # Title
        self.SetSize((x*0.95, y*0.95))          # size of window in pixels
        self.SetPosition((x*0.05, y*0.05))      # position of window on display

# %%   
    """  Put a notebook in the window  """

    def __do_layout(self):
        self.videoNotebook = mainNotebook(self, -1)

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(self.videoNotebook, 1, wx.EXPAND, 0)
        self.SetSizer(mainSizer)

# %%  
    """  Generate the menu bar for the notebook.  """

    def __menubar__(self):

    # Get new IDs for the menu options in the menubar -----------------------
     # File menu -----------------------------------------
        ID_FILE_OPEN = wx.NewId()       # Open
        ID_FILE_SAVE = wx.NewId()       # Save
        ID_FILE_SAVE_AS = wx.NewId()    # Save As...
        # ID_FILE_CLOSE =  wx.NewId()   # Close
        ID_FILE_EXIT = wx.NewId()       # Exit

     # Options Menu --------------------------------------
        ID_OPTIONS_SET = wx.NewId()     # Configure

     # Help Menu -----------------------------------------
        ID_HELP_ABOUT = wx.NewId()      # About
        

    # Generate the dropdown lists.  (& indicates shortcut letter) -----------
     # File menu --------------------------------------------------
        filemenu = wx.Menu()
        filemenu.Append(ID_FILE_OPEN, '&Open File', 'Open a file')
        filemenu.Append(ID_FILE_SAVE, '&Save File', 'Save current file')
        filemenu.Append(ID_FILE_SAVE_AS,
                       '&Save as...', 'Save current data in a new file')
        # filemenu.Append(ID_FILE_CLOSE, '&Close File', 'Close')
        filemenu.AppendSeparator()
        filemenu.Append(ID_FILE_EXIT, 'E&xit Program', 'Exit')

     # Options Menu ------------------------------------------------
        optmenu = wx.Menu()
        optmenu.Append(ID_OPTIONS_SET,
                      'Confi&gure', 'View and change settings')

     # Help Menu ---------------------------------------------------
        helpmenu = wx.Menu()
        helpmenu.Append(ID_HELP_ABOUT, 'Abou&t')

   # Create the MenuBar ----------------------------------------------------
        menubar = wx.MenuBar(style=wx.SIMPLE_BORDER)

     # Populate the MenuBar ----------------------------------------
        menubar.Append(filemenu, '&File')
        menubar.Append(optmenu, '&Options')
        menubar.Append(helpmenu, '&Help')

     # and apply the menubar ---------------------------------------
        self.SetMenuBar(menubar)

     # Associate the menu items with their functions ---------------
        wx.EVT_MENU(self, ID_FILE_OPEN, self.onFileOpen)
        wx.EVT_MENU(self, ID_FILE_SAVE, self.onFileSave)
        wx.EVT_MENU(self, ID_FILE_SAVE_AS, self.onFileSaveAs)
        # wx.EVT_MENU(self, ID_FILE_CLOSE, self.onFileClose)
        wx.EVT_MENU(self, ID_FILE_EXIT, self.onFileExit)
        wx.EVT_MENU(self, ID_OPTIONS_SET, self.onConfigure)
        wx.EVT_MENU(self, ID_HELP_ABOUT, self.onAbout)

# %%
    """  About Dialog  """

    def onAbout(self, event):
        pySoloVideoVersion = "XXXXXXXXXXX"                                       # temporary value
        info = wx.AboutDialogInfo()
        
        info.SetVersion('pySolo-Video - v' + pySoloVideoVersion)                 # PySoloVideoVersion not specified
        info.SetCopyright('by Giorgio F. Gilestro\n')
        info.SetWebSite('http://www.pysolo.net')

        wx.AboutBox(info)

# %%
    """  Saves the current configuration to the same file that was opened. """

    def onFileSave(self, event):
        print(' File > Save ')                                                   # temporary debug print
        options.Save()                  # options class contains config info
                                        #    see pvg_common.py class MyConfig()

# %%
    """  Saves the current configuration to a new file, named by the user. """

    def onFileSaveAs(self, event):
        filename = DEFAULT_CONFIG
        wildcard = "pySolo Video config file (*.cfg)|*.cfg |" \
                    "All files (*.*)|*.*"

        # opens the file explorer for user to choose file path and name.
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(),
            defaultFile=filename, wildcard=wildcard, style=wx.SAVE
            )

        # dlg.SetFilterIndex(2)

        # If user clicks "OK", save the file to the chosen path and name
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            options.Save(filename=path)

        dlg.Destroy()

# %%
    """  Opens a file  """
    
    def onFileOpen(self, event):
        wildcard = "pySolo Video config file (*.cfg)|*.cfg"

        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
            )

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            options.New(path)

        dlg.Destroy()

# %%
    """  Closes a file   """

    def onFileExit(self, event):
        self.Close()

# %%
    """ Change Configuration  """
    def onConfigure(self, event):
        frame_opt = optionsFrame(self)
        #frame_opt.Show()
        res = frame_opt.ShowModal()
        frame_opt.Destroy()
        if res == wx.ID_OK:
            self.videoNotebook.updateUI()
        elif res == wx.ID_CANCEL:
            print "no changes were made"

# %%
"""  The main notebook containing all the panels for data displaying and
     analysis.  This is displayed inside the main window.  """
class mainNotebook(wx.Notebook):
# %% 
    """  creates a notebook with tabs on the left side  """

    def __init__(self, *args, **kwds):
        # begin wxGlade: propertiesNotebook.__init__
        kwds["style"] = wx.NB_LEFT
        wx.Notebook.__init__(self, *args, **kwds)

        self.panelOne = panelOne(self)         # in file panelOne.py
        self.AddPage(self.panelOne, "Monitors sheet")

        self.panelTwo = panelLiveView(self)         # in file panelTwo.py
        self.AddPage(self.panelTwo, "Live View")

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)

        self.Layout()

# %%
    """  refreshes screens  """

    def updateUI(self):
        self.panelOne.onRefresh()
        self.panelTwo.onRefresh()
        self.Layout()

# %%
    """  refreshes screens after configuration change  """

    def OnPageChanging(self, event):
        # self.panelOne.StopPlaying()                                           # old, unnecessary code?
        self.panelTwo.StopPlaying()

# %%
"""  Main Program  """

x, y = options.GetOption("Resolution")    # screen resolution global variables.

if __name__ == "__main__":

    app = wx.App(False)  # Create a new GUI,
    #                False => don't redirect stdout/stderr to a window.
    frame_1 = mainFrame(None, -1, "")     # create the GUI window
    frame_1.Show()
    app.SetTopWindow(frame_1)
    app.MainLoop()                        # begin interaction with user
    print('done')                                                               # temporary debug print
    
