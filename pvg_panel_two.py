#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#       untitled.py
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

# %%
import wx                 # GUI functions
import os
import numpy as np
import cv2                # camera / video control
import pysolovideo 
import pvg_options
from sys import argv      # file I/O
from pvg_common import previewPanel, options

x, y = options.GetOption("Resolution")    # screen resolution


# %%


class panelLiveView(wx.Panel):
    """
    Panel Number 2
    Live view of selected camera
    """

# %%
    def __init__(self, parent):

        self.panel = wx.Panel.__init__(self, parent)
        self.fsPanel = previewPanel(self,
                                    size=options.GetOption("Resolution"),
                                    showtime=True)

# %%%%%%%%%%%%%%%%%% sizer_Left: Monitor Display
#  Monitor Selection on top
    # Give title to the monitor selection combobox
        title_1 = wx.StaticText(self, wx.ID_ANY, 'Select Monitor')
    # create select monitor combobox on top of left column
        MonitorList = ['Monitor %s' % (int(m) + 1)
                      for m in range(options.GetOption("Monitors"))]            # not reflecting number of monitors in configuration
        thumbnailNumber = wx.ComboBox(self, wx.ID_ANY,
                                     choices=MonitorList,
                                     style=wx.CB_DROPDOWN |
                                     wx.CB_READONLY |
                                     wx.CB_SORT)
        self.Bind(wx.EVT_COMBOBOX, self.onChangeMonitor, thumbnailNumber)

#   sizer for left side, top row control buttons
        sizer_top_Left = wx.BoxSizer(wx.HORIZONTAL)
        sizer_top_Left.Add(title_1, 0, wx.ALL, 5)          # menu title
        sizer_top_Left.Add(thumbnailNumber, 0, wx.ALL, 5)  # menu

# %%  Movie Display on bottom
        videoWarper = wx.StaticBox(self, label='Movie Label',
                                   size=(x/2, y*2/3))
        videoBoxSizer = wx.StaticBoxSizer(videoWarper, wx.VERTICAL) 
        videoFrame = wx.Panel(self, wx.ID_ANY, size=(640, 480))
#        cap = cv2.VideoCapture('fly_movie.avi')                                # not working on thinkpad computer
#        showCap = ShowCapture(videoFrame, cap)                                 # not working on thinkpad computer
        videoBoxSizer.Add(videoFrame, 0)

#  Sizer for left side of display
        sizer_Left = wx.BoxSizer(wx.VERTICAL)
        sizer_Left.Add(sizer_top_Left, 0, wx.ALL, 5)   # monitor combobox
        sizer_Left.Add(videoBoxSizer, 0, wx.ALL, 5)    # movie

# %%%%%%%%%%%%%%%%%%  sizer_Right:  Mask Editing
#     Section Title
        mask_editing = wx.StaticText(self, wx.ID_ANY, 'Mask Editing')

#      top row is single item, no sizer needed
#
# %% Clear Buttons
        btnClearAll = wx.Button(self, wx.ID_ANY, label="Clear All")
#        self.Bind(wx.EVT_BUTTON, self.fsPanel.ClearAll, self.btnClearAll)
#
        btnClearSelected = wx.Button(self, wx.ID_ANY, label="Clear Selected")
#        self.Bind(wx.EVT_BUTTON, self.fsPanel.ClearLast, self.btnClearSelected)
#
#  sizer for clear buttons on right side of display
        sizer_ClrBtns_Right = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ClrBtns_Right.Add(btnClearSelected, 0, wx.ALL, 5)    # clear selected
        sizer_ClrBtns_Right.Add(btnClearAll, 0, wx.ALL, 5)         # clear all

# %%   AutoFill Value
        AFValue = wx.TextCtrl(self, -1, "32")                                   #  make this variable?

        btnAutoFill = wx.Button(self, wx.ID_ANY, label="Auto Fill")
#        self.Bind(wx.EVT_BUTTON, self.onAutoMask, self.btnAutoFill)
#        self.btnAutoFill.Enable(False)

#  sizer for AutoFill controls
        sizer_Autofill_Right = wx.BoxSizer(wx.HORIZONTAL)
        sizer_Autofill_Right.Add(btnAutoFill, 0, wx.ALL, 5)        # Autofill
        sizer_Autofill_Right.Add(AFValue, 0, wx.ALL, 5)            # AF Value


# %%  Right Side, Mask selection controls
#   Mask Title
        Mask_File_Title = wx.StaticText(self, wx.ID_ANY, "Curent Mask")
        self.currentMaskTXT = wx.TextCtrl(self, wx.ID_ANY, value='No Mask Selected',
                                     size=(x/4,20))
#                                     style=wx.TE_READONLY)                     #  get the current mask text for this
        #  sizer for current mask
        sizer_currmsk_Right = wx.BoxSizer(wx.HORIZONTAL)  # button section
        sizer_currmsk_Right.Add(Mask_File_Title, 0, wx.ALL, 5)   # title
        sizer_currmsk_Right.Add(self.currentMaskTXT, 0, wx.ALL, 5)   # title

# %%
#   Mask Buttons
        btnLoad = wx.Button(self, wx.ID_ANY, label="Load Mask")
        self.Bind(wx.EVT_BUTTON, self.onLoadMask, btnLoad)

        btnSave = wx.Button(self, wx.ID_ANY, label="Save Mask")
        self.Bind(wx.EVT_BUTTON, self.onSaveMask, btnSave)

        btnSaveApply = wx.Button( self, wx.ID_ANY, label="Save + Apply")
#        self.Bind(wx.EVT_BUTTON, self.onSaveApply, self.btnSaveApply)

#  sizer for mask buttons
        sizer_maskIO_Right = wx.BoxSizer(wx.HORIZONTAL)  # button section
        sizer_maskIO_Right.Add(btnLoad, 0, wx.ALL, 5)       # load mask btn
        sizer_maskIO_Right.Add(btnSave, 0, wx.ALL, 5)       # Save mask btn
        sizer_maskIO_Right.Add(btnSaveApply, 0, wx.ALL, 5)  # Apply mask btn

# %% Mouse Instructions
#   Section Title
        Controls_Title = wx.StaticText(self, wx.ID_ANY, "Mouse Controls")
#        titleFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        instr = [ ('   Left mouse button - single click outside ROI'),
                  ('        Start dragging ROI. ROI will be a perfect rectangle'),
                  ('   Left mouse button - single click inside ROI'),
                  ('        Select ROI. ROI turns red.'),
                  ('   Left mouse button - double click'),
                  ('        Select corner of ROI.  Will close ROI after fourth selection'),
                  ('   Middle mouse button - single click'),
                  ('        Add currently selected ROI. ROI turns white.'),
                  ('   Right mouse button - click'),
                  ('        Remove selected currently selected ROI'),
                  ('   Auto Fill'),
                  ('        Will fill 32 ROIS (16x2) to fit under the last two'),
                  ('        selected points. To use select first upper left corner,'),
                  ('        then the lower right corner, then use "Auto Fill".')
                  ]

#
#   sizer for instructions
        sizer_instr_Right = wx.BoxSizer(wx.VERTICAL)   # Help Section
        sizer_instr_Right.Add(Controls_Title, 0, wx.ALL, 5)   # title
        for txtline in instr:
            instr_line = wx.StaticText(self, wx.ID_ANY, txtline)  #; t.SetFont(titleFont)
            sizer_instr_Right.Add(instr_line, 0, wx.ALL, 1)   # next instrctn

# %%  sizer for right side of display
        sizer_Right = wx.BoxSizer(wx.VERTICAL)
        sizer_Right.Add(mask_editing, 0, wx.ALL, 5)         # section title
        sizer_Right.Add(sizer_ClrBtns_Right, 0, wx.ALL, 5)      # Mask Buttons
        sizer_Right.Add(sizer_currmsk_Right, 0, wx.ALL, 5)    # Mask Selection
        sizer_Right.Add(sizer_maskIO_Right, 0, wx.ALL, 5)    # Mask Selection
        sizer_Right.Add(sizer_Autofill_Right, 0, wx.ALL, 5)    # AutoFill
        sizer_Right.Add(sizer_instr_Right, 0, wx.ALL, 5)    # Mouse Instruction


# %%  Full Panel
        sizer_All = wx.BoxSizer(wx.HORIZONTAL)       # put everything together
        sizer_All.Add(sizer_Left, 0, wx.ALL, 5)
        sizer_All.Add(sizer_Right, 0, wx.ALL, 5)

        self.SetSizer(sizer_All)                   # displays the grid

# %%                                                                               # What does this do?
#        print wx.Window.FindFocus()
#
#        self.Bind( wx.EVT_CHAR, self.fsPanel.onKeyPressed )

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Event functions
#
#  Stop Playing

    def StopPlaying(self):
        """
        """
        print('Stop Playing Function')                                          # temporary debug print
#        if self.fsPanel and self.fsPanel.isPlaying: self.fsPanel.Stop()
#
#
# %%  Change Monitor

    def onChangeMonitor(self, event):
        """
        FIX THIS
        this is a mess
        """
        print("onChangeMonitor activated")                                      # temporary debug print
#        mn = event.GetSelection() + 1
#
#        if options.HasMonitor(mn):
#
#            md = options.GetMonitor(mn)
#
#            if md['source']:
#                if self.fsPanel.isPlaying: self.fsPanel.Stop()
#
#
#                self.fsPanel.setMonitor( pysolovideo.MONITORS[mn] )
#                self.sourceTXTBOX.SetValue( 'Source: %s' % md['source'] )
#
#                self.fsPanel.Play()
#
#                if md['mask_file']:
#                    self.fsPanel.mon.loadROIS(md['mask_file'])
#                    self.currentMaskTXT.SetValue(os.path.split(md['mask_file'])[1] or '')
#
#            else:
#                #sourceType, source, track, mask_file, trackType = [0, '', False, '', 1]
#                self.sourceTXTBOX.SetValue('No Source for this monitor')


## %%
#    def onAutoMask(self, event):
#        """
#        """
#        n_roi = int( self.AFValue.GetValue() )
#        self.fsPanel.autoDivideMask(n_roi)
#
#
# %%  Save Mask
    """  Save ROIs to File  """
    
    def onSaveMask(self, event):
                                                                                # temporary debug print
        print('Current Mask Name = ' + self.currentMaskTXT.GetValue())          # each switch between file types adds another .msk to the filename
        wildcard = "PySolo Mask (*.msk) | *.msk |" \
                   "All files (*.*)|*.*"
                   
        print('wildcard = ' + wildcard)                                         # temporary debug print

        dlg = wx.FileDialog(self, message="Save file as ...", 
                            defaultDir=options.GetOption("Mask_Folder"),
                            defaultFile=self.currentMaskTXT.GetValue(),
                            wildcard=wildcard, 
                            style=wx.SAVE | wx.FD_OVERWRITE_PROMPT)

        print('Current Mask Name = ' + self.currentMaskTXT.GetValue())          # temporary debug print
#        dlg.SetFilterIndex(2)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print('save path = ' + path)                                        # temporary debug print
            self.fsPanel.mon.saveROIS(path)
            self.currentMaskTXT.SetValue(os.path.split(path)[1])

        dlg.Destroy()
#        return path

## %%
#    def onSaveApply(self, event):
#        """
#        Save ROIs to file and apply to current monitor
#        """
#        path = self.onSaveMask(None)
#        mn = self.monitor_name.replace(' ','')
#        options.setValue(mn, 'maskfile', path)
#        options.Save()
#
# %%
    def onLoadMask(self, event):
        """
        Load Mask from file
        """
        print('Load Mask Function')                                             # temporary debug print
        wildcard = "PySolo Mask (*.msk) | *.msk | " \
                   "All files (*.*)|*.*"

    
        print('before filedialog')                                              # temporary debug print
        dlg = wx.FileDialog(self, message="Choose a file",
            defaultDir=options.GetOption("Mask_Folder"),
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR
            )
        print('after filedialog')                                               # temporary debug print
        if dlg.ShowModal() == wx.ID_OK:
            print('showmodal is true')                                          # temporary debug print
            path = dlg.GetPath()
            print('Load Path = ' + path)                                        # temporary debug print
            self.fsPanel.mon.saveROIS(path)                                     # load set to save temporarily since load isn't working
            self.currentMaskTXT.SetValue(os.path.split(path)[1])
            
        print('done')                                                           # temporary debug print
        dlg.Destroy()


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class ShowCapture(wx.Panel):

    def __init__(self, parent, capture, fps=24):
        wx.Panel.__init__(self, parent, wx.ID_ANY, (0,0), (640,480))

        self.capture = capture
        ret, frame = self.capture.read()

        height, width = frame.shape[:2]             #  ??? no attribute 'shape'

        parent.SetSize((width, height))

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.bmp = wx.BitmapFromBuffer(width, height, frame)

        self.timer = wx.Timer(self)
        self.timer.Start(1000./fps)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    def NextFrame(self, event):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(frame)
            self.Refresh()
