# -*- coding: utf-8 -*-

import os
import wx
import wx.grid

class MyDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self.window_1 = wx.SplitterWindow(self, -1, style=wx.SP_3D|wx.SP_BORDER)
        self.tree_ctrl_1 = wx.TreeCtrl(self, -1, style=wx.TR_HAS_BUTTONS|wx.TR_LINES_AT_ROOT|wx.TR_DEFAULT_STYLE|wx.SUNKEN_BORDER)
        self.text_ctrl_1 = wx.TextCtrl(self.window_1, -1, "This is the Edit", style=wx.TE_MULTILINE)
        self.grid_1 = wx.grid.Grid(self.window_1, -1, size=(1, 1))

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog.__set_properties
        self.SetTitle("dialog_1")
        self.grid_1.CreateGrid(10, 3)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDialog.__do_layout
        grid_sizer_1 = wx.FlexGridSizer(1, 2, 3, 3)
        grid_sizer_1.Add(self.tree_ctrl_1, 1, wx.EXPAND, 0)
        self.window_1.SplitHorizontally(self.text_ctrl_1, self.grid_1)
        grid_sizer_1.Add(self.window_1, 1, wx.EXPAND, 0)
        self.SetSizer(grid_sizer_1)
        grid_sizer_1.Fit(self)
        grid_sizer_1.AddGrowableRow(0)
        grid_sizer_1.AddGrowableCol(0)
        grid_sizer_1.AddGrowableCol(1)
        self.Layout()
        # end wxGlade

# end of class MyDialog


class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        mainDlg = MyDialog(None, -1, "")
        self.SetTopWindow(mainDlg)
        mainDlg.Show()
        return 1

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()