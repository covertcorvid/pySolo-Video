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
#      Import modules

import wx, os

from pvg_options import optionsFrame

from pvg_acquire import pvg_AcquirePanel as panelOne
from pvg_panel_two import panelLiveView
from pvg_common import options, DEFAULT_CONFIG

from pysolovideo import pySoloVideoVersion


# %%


class mainFrame(wx.Frame):
    """
    Creates the main window of the application.
    """
# %%

    def __init__(self, *args, **kwds):

        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.__set_properties()     # set title, position, and size of
        #                                     main window.
        self.__do_layout()          # set shape and size of notebook in window.
        self.__menubar__()          # create the menu bar across the top

# %%    Set the properties of the main window

    def __set_properties(self):
        # begin wxGlade: mainFrame.__set_properties
        self.SetTitle("pySoloVideo")                # Title
        self.SetSize((x*0.95, y*0.95))            # size of window in pixels
        self.SetPosition((x*0.05, y*0.05))          # position of window on display

# %%

    def __do_layout(self):
        # Add Notebook
        self.videoNotebook = mainNotebook(self, -1)

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(self.videoNotebook, 1, wx.EXPAND, 0)
        self.SetSizer(mainSizer)

# %%

    def __menubar__(self):

        # Gives new IDs to the menu voices in the menubar
        # File menu
        ID_FILE_OPEN = wx.NewId()       # Open
        ID_FILE_SAVE = wx.NewId()
        ID_FILE_SAVE_AS = wx.NewId()    # Save As...
        # ID_FILE_CLOSE =  wx.NewId()
        ID_FILE_EXIT = wx.NewId()       # Exit

        # Options Menu
        ID_OPTIONS_SET = wx.NewId()     # Configure

        # Help Menu
        ID_HELP_ABOUT = wx.NewId()      # About

        # Generate the dropdown lists.  & indicates shortcut letter
        # File menu
        filemenu = wx.Menu()
        filemenu. Append(ID_FILE_OPEN, '&Open File', 'Open a file')
        filemenu. Append(ID_FILE_SAVE, '&Save File', 'Save current file')
        filemenu. Append(ID_FILE_SAVE_AS,
                         '&Save as...', 'Save current data in a new file')
        # filemenu. Append(ID_FILE_CLOSE, '&Close File', 'Close')
        filemenu. AppendSeparator()
        filemenu. Append(ID_FILE_EXIT, 'E&xit Program', 'Exit')

        # Options Menu
        optmenu = wx.Menu()
        optmenu. Append(ID_OPTIONS_SET,
                        'Confi&gure', 'View and change settings')

        # Help Menu
        helpmenu = wx.Menu()
        helpmenu. Append(ID_HELP_ABOUT, 'Abou&t')

        # Create the MenuBar
        menubar = wx.MenuBar(style=wx.SIMPLE_BORDER)

        # Populate the MenuBar
        menubar. Append(filemenu, '&File')
        menubar. Append(optmenu, '&Options')
        menubar. Append(helpmenu, '&Help')

        # and apply the menubar
        self.SetMenuBar(menubar)

        # Associate the menu items with their functions
        wx.EVT_MENU(self, ID_FILE_OPEN, self.onFileOpen)
        wx.EVT_MENU(self, ID_FILE_SAVE, self.onFileSave)
        wx.EVT_MENU(self, ID_FILE_SAVE_AS, self.onFileSaveAs)
        # wx.EVT_MENU(self, ID_FILE_CLOSE, self.onFileClose)
        wx.EVT_MENU(self, ID_FILE_EXIT, self.onFileExit)
        wx.EVT_MENU(self, ID_OPTIONS_SET, self.onConfigure)
        wx.EVT_MENU(self, ID_HELP_ABOUT, self.onAbout)

# %%

    def onAbout(self, event):
        """
        Shows the about dialog
        """
        about = 'pySolo-Video - v %s\n' % pySoloVideoVersion
        about += 'by Giorgio F. Gilestro\n'
        about += 'Visit http://www.pysolo.net for more information'

        dlg = wx.MessageDialog(self,
                               about, 'About', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

# %%

    def onFileSave(self, event):
        """
        Saves the current configuration to the same file that was opened.
        """
        options.Save()

# %%

    def onFileSaveAs(self, event):
        """
        Saves the current configuration to a new file, named by the user.
        """
        filename = DEFAULT_CONFIG
        wildcard = "pySolo Video config file (*.cfg)|*.cfg"

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

    def onFileOpen(self, event):
        """
        """
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

    def onFileExit(self, event):
        """
        """
        self.Close()

# %%

    def onConfigure(self, event):
        """
        """
        frame_opt = optionsFrame(self, -1, '')
        frame_opt.Show()

# %%


class mainNotebook(wx.Notebook):
    #
    #    The main notebook containing all the panels for data displaying and
    #    analysis.  This is displayed inside the main window.
    #

    # %%
    #
    #   creates a notebook with tabs on the left side

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

    def OnPageChanging(self, event):
        """
        """
        # self.panelOne.StopPlaying()
        self.panelTwo.StopPlaying()

# %%

x, y = options.GetOption("Resolution")    # screen resolution global variables.

if __name__ == "__main__":

    app = wx.App(False)  # Create a new GUI,
    #                False => don't redirect stdout/stderr to a window.
    frame_1 = mainFrame(None, -1, "")     # create the GUI window
    frame_1.Show()
    app.SetTopWindow(frame_1)
    app.MainLoop()                        # begin interaction with user
