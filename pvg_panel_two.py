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
import wx, os
import numpy as np
import cv2
from pvg_common import previewPanel, options
#import pysolovideo

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

#        self.monitor_name = ''
        self.fsPanel = previewPanel(self,
                                    size=options.GetOption("Resolution"),
                                    showtime=True)

#        sizer_1 = wx.BoxSizer(wx.VERTICAL)
#        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
#        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
#        sizer_4 = wx.BoxSizer(wx.VERTICAL)

# %%
# sizer_1: Monitor Display
# %% Static Box 1:  Monitor input
        self.title_1 = wx.StaticText(self, wx.ID_ANY, 'Select Monitor')
    #create select monitor combobox
        self.MonitorList = ['Monitor %s' % (int(m) + 1)
                            for m in range(options.GetOption("Monitors"))]
        self.thumbnailNumber = wx.ComboBox(self, -1, size=(-1,-1),
                                           choices=self.MonitorList,
                                           style=wx.CB_DROPDOWN
                                           | wx.CB_READONLY
                                           | wx.CB_SORT)
        self.Bind(wx.EVT_COMBOBOX, self.onChangeMonitor, self.thumbnailNumber)

        sizer_1a = wx.BoxSizer(wx.HORIZONTAL)

        sizer_1a.Add(self.title_1, 0, wx.ALL, 5)
        sizer_1a.Add(self.thumbnailNumber, 0, wx.ALL, 5)


# INSERT VIDEO HERE
#        self.movie = wx.ArtProvider.GetBitmap(wx.ART_TIP, wx.ART_OTHER, (16, 16))
        videoWarper = wx.StaticBox(self, size=(640,480))
        videoBoxSizer = wx.StaticBoxSizer(videoWarper, wx.VERTICAL)
        videoFrame = wx.Panel(self, -1, size=(640,480))
        cap = cv2.VideoCapture('fly_movie.avi')
        showCap = ShowCapture(videoFrame, cap)
        videoBoxSizer.Add(videoFrame, 0)
#        self.inputOneIco = wx.StaticBitmap(self, wx.ID_ANY, self.movie)


        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_1a, 0, wx.ALL, 20)
        sizer_1.Add(videoBoxSizer, 0, wx.ALL, 20)

        self.SetSizer(sizer_1)

## Column 2:
##   monitor selection menu staticbox
#        self.select_monitor = wx.StaticTest(self.panel, wx.ID_ANY, "Select Monitor")
##   thumbnail combobox
##   text box for data entry
#        self.sourceTXTBOX = wx.TextCtrl(self, -1,
#                                        name="No monitor selected",
#                                        style=wx.TE_READONLY)

#   apply the boxes to the sizer
#
#        sizer_1.Add(self.select_monitor, 0, wx.ALIGN_CENTRE |
#                                               wx.LEFT |
#                                               wx.RIGHT |
#                                               wx.TOP, 5)
#        sizer_1.Add(self.thumbnailNumber, 0, wx.ALIGN_CENTRE |
#                                               wx.LEFT |
#                                               wx.RIGHT |
#                                               wx.TOP, 5)
#        sizer_1.Add(self.sourceTXTBOX, 0, wx.ALIGN_CENTRE |
#                                               wx.LEFT |
#                                               wx.RIGHT |
#                                               wx.TOP, 5)

## %%
##        Mask Parameters
#        mask_editing = wx.StaticBox(self, -1, "Mask Editing")
## ,
##                            pos=(x*0.6, y*0.02), size=(x*0.3, y*0.3))
##        sbSizer_2 = wx.StaticBoxSizer(sb_2, wx.VERTICAL)
#        fgSizer_1 = wx.FlexGridSizer(4, 0, 10, 10)
#
#        self.btnClear = wx.Button(self, wx.ID_ANY, label="Clear All")
#        self.Bind(wx.EVT_BUTTON, self.fsPanel.ClearAll, self.btnClear)
#
#        self.btnClearLast = wx.Button(self, wx.ID_ANY, label="Clear selected")
#        self.Bind(wx.EVT_BUTTON, self.fsPanel.ClearLast, self.btnClearLast)
#
#        self.AFValue = wx.TextCtrl(self, -1, "32")
#        self.btnAutoFill = wx.Button(self, wx.ID_ANY, label="Auto Fill")
#        self.Bind(wx.EVT_BUTTON, self.onAutoMask, self.btnAutoFill)
#        # self.btnAutoFill.Enable(False)
#
#        fgSizer_1.Add(self.btnClear)
#        fgSizer_1.Add(self.btnClearLast)
#        fgSizer_1.Add(self.AFValue)
#        fgSizer_1.Add(self.btnAutoFill)
#
#        sbSizer_2.Add(fgSizer_1)


##   text box for data entry
#        self.sourceTXTBOX = wx.TextCtrl(self, -1,
#                                        pos=(x*0.45, y*0.13),
#                                        name="No monitor selected",
#                                        style=wx.TE_READONLY)
#
#        Sizer_1.Add(self.thumbnailNumber, 0, wx.ALIGN_CENTRE |
#                                               wx.LEFT |
#                                               wx.RIGHT |
#                                               wx.TOP, 5)
#        sbSizer_1.Add(self.sourceTXTBOX, 0, wx.ALIGN_CENTRE |
#                                               wx.LEFT |
#                                               wx.RIGHT |
#                                               wx.TOP, 5)
## %%         Play video in Static Box 1
##
##
##        print('Playing Video')
##        cap = cv2.VideoCapture('c:\Users\Lori\Documents\GitHub\fly_movie.avi')
##
##        while(cap.isOpened()):
##            ret, frame = cap.read()
##
##            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
##
##            cv2.imshow('frame',gray)
##            if cv2.waitKey(1) & 0xFF == ord('q'):
##                break
##
##        cap.release()
##        cv2.destroyAllWindows()
##
#
## %%
##        # Static box2: Mask Parameters
#        sb_2 = wx.StaticBox(self, -1, "Mask Editing",
#                            pos=(x*0.6, y*0.02), size=(x*0.3, y*0.3))
##        sbSizer_2 = wx.StaticBoxSizer(sb_2, wx.VERTICAL)
#        fgSizer_1 = wx.FlexGridSizer(4, 0, 10, 10)
#
#        self.btnClear = wx.Button(self, wx.ID_ANY, label="Clear All")
#        self.Bind(wx.EVT_BUTTON, self.fsPanel.ClearAll, self.btnClear)
#
#        self.btnClearLast = wx.Button(self, wx.ID_ANY, label="Clear selected")
#        self.Bind(wx.EVT_BUTTON, self.fsPanel.ClearLast, self.btnClearLast)
#
#        self.AFValue = wx.TextCtrl(self, -1, "32")
#        self.btnAutoFill = wx.Button(self, wx.ID_ANY, label="Auto Fill")
#        self.Bind(wx.EVT_BUTTON, self.onAutoMask, self.btnAutoFill)
#        # self.btnAutoFill.Enable(False)
#
#        fgSizer_1.Add(self.btnClear)
#        fgSizer_1.Add(self.btnClearLast)
#        fgSizer_1.Add(self.AFValue)
#        fgSizer_1.Add(self.btnAutoFill)
##
##        sbSizer_2.Add(fgSizer_1)
#
#
### %%
##        # Static box3: mask I/O
##        sb_3 = wx.StaticBox(self, -1, "Mask File")#, size=(250,-1))
##        sbSizer_3 = wx.StaticBoxSizer (sb_3, wx.VERTICAL)
##
##        self.currentMaskTXT = wx.TextCtrl (self, -1, "No Mask Loaded", style=wx.TE_READONLY)
##
##        btnSizer_1 = wx.BoxSizer(wx.HORIZONTAL)
##        self.btnLoad = wx.Button( self, wx.ID_ANY, label="Load Mask")
##        self.Bind(wx.EVT_BUTTON, self.onLoadMask, self.btnLoad)
##        self.btnSave = wx.Button( self, wx.ID_ANY, label="Save Mask")
##        self.Bind(wx.EVT_BUTTON, self.onSaveMask, self.btnSave)
##        self.btnSaveApply = wx.Button( self, wx.ID_ANY, label="Save and Apply")
##        self.Bind(wx.EVT_BUTTON, self.onSaveApply, self.btnSaveApply)
##
##        btnSizer_1.Add(self.btnLoad)
##        btnSizer_1.Add(self.btnSave)
##        btnSizer_1.Add(self.btnSaveApply)
##
##        sbSizer_3.Add ( self.currentMaskTXT, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )
##        sbSizer_3.Add (btnSizer_1, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
##
##        ##
##
### %%        # Static box4: help
##        sb_4 = wx.StaticBox(self, -1, "Help")
##        sbSizer_4 = wx.StaticBoxSizer (sb_4, wx.VERTICAL)
##        titleFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
##        instr = [ ('Left mouse button - single click outside ROI', 'Start dragging ROI. ROI will be a perfect rectangle'),
##                  ('Left mouse button - single click inside ROI', 'Select ROI. ROI turns red.'),
##                  ('Left mouse button - double click', 'Select corner of ROI.\nWill close ROI after fourth selection'),
##                  ('Middle mouse button - single click', 'Add currently selected ROI. ROI turns white.'),
##                  ('Right mouse button - click', 'Remove selected currently selected ROI'),
##                  ('Auto Fill', 'Will fill 32 ROIS (16x2) to fit under the last two\nselected points. To use select first upper left corner,\n then the lower right corner, then use "Auto Fill".')
##                  ]
##
##        for title, text in instr:
##            t = wx.StaticText(self, -1, title); t.SetFont(titleFont)
##            sbSizer_4.Add( t, 0, wx.ALL, 2 )
##            sbSizer_4.Add(wx.StaticText(self, -1, text) , 0 , wx.ALL, 2 )
##            sbSizer_4.Add ( (wx.StaticLine(self)), 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )
##
##        sizer_4.Add(sbSizer_1, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )
##        sizer_4.Add(sbSizer_2, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )
##        sizer_4.Add(sbSizer_3, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )
##        sizer_4.Add(sbSizer_4, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )
##
##
##        sizer_3.Add(self.fsPanel, 0, wx.LEFT|wx.TOP, 20 )
##        sizer_3.Add(sizer_4, 0, wx.ALIGN_RIGHT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
##
##        sizer_1.Add(sizer_3, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
##        sizer_1.Add(sizer_2, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
##
##
##        self.SetSizer(sizer_1)
##        print wx.Window.FindFocus()
##
##        self.Bind( wx.EVT_CHAR, self.fsPanel.onKeyPressed )
#
## %%
#
    def StopPlaying(self):
        """
        """
        if self.fsPanel and self.fsPanel.isPlaying: self.fsPanel.Stop()
#
#
# %%
    def onChangeMonitor(self, event):
        """
        FIX THIS
        this is a mess
        """
        print("onChangeMonitor activated")
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
## %%
#    def onSaveMask(self, event):
#        """
#        Save ROIs to File
#        """
#
#        filename = '%s.msk' % self.monitor_name.replace(' ','_')
#        wildcard = "pySolo mask file (*.msk)|*.msk"
#
#        dlg = wx.FileDialog(
#            self, message="Save file as ...", defaultDir=options.GetOption("Mask_Folder"),
#            defaultFile=filename, wildcard=wildcard, style=wx.SAVE
#            )
#
#        # dlg.SetFilterIndex(2)
#
#        if dlg.ShowModal() == wx.ID_OK:
#            path = dlg.GetPath()
#            self.fsPanel.mon.saveROIS(path)
#            self.currentMaskTXT.SetValue(os.path.split(path)[1])
#
#        dlg.Destroy()
#        return path
#
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
## %%
#    def onLoadMask(self, event):
#        """
#        Load Mask from file
#        """
#
#        wildcard = "pySolo mask file (*.msk)|*.msk"
#
#        dlg = wx.FileDialog(
#            self, message="Choose a file",
#            defaultDir=options.GetOption("Mask_Folder"),
#            defaultFile="",
#            wildcard=wildcard,
#            style=wx.OPEN | wx.CHANGE_DIR
#            )
#
#        if dlg.ShowModal() == wx.ID_OK:
#            path = dlg.GetPath()
#            self.fsPanel.mon.loadROIS(path)
#            self.currentMaskTXT.SetValue(os.path.split(path)[1])
#
#        dlg.Destroy()
#
#
#
#x, y = options.GetOption("Resolution")    # screen resolution global variables.
#
class ShowCapture(wx.Panel):

    def __init__(self, parent, capture, fps=24):
        wx.Panel.__init__(self, parent, wx.ID_ANY, (0,0), (640,480))

        self.capture = capture
        ret, frame = self.capture.read()

        height, width = frame.shape[:2]

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
