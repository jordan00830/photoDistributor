# create a wx frame with 6 wx buttons and optional tooltips
# hide/disable and show/enable the buttons as they are clicked
# also show right-click and double-click events
# tested with Python24 and wxPython26 by    vegaseat   29may2006
import wx
class MyFrame(wx.Frame):
    """make a frame, inherits wx.Frame"""
    def __init__(self):
        # create a frame, no parent, default to wxID_ANY
        wx.Frame.__init__(self, None, wx.ID_ANY, 'wxButton',
            pos=(300, 150), size=(320, 250))
        self.SetBackgroundColour("green")
        
        self.button1 = wx.Button(self, id=-1, label='Button1',
            pos=(8, 8), size=(175, 28))
        self.button1.Bind(wx.EVT_BUTTON, self.button1Click)
        # optional tooltip
        self.button1.SetToolTip(wx.ToolTip("click to hide"))
        self.button2 = wx.Button(self, id=-1, label='Button2',
            pos=(8, 38), size=(175, 28))
        self.button2.Bind(wx.EVT_BUTTON, self.button2Click)
        # optional tooltip
        self.button2.SetToolTip(wx.ToolTip("click to hide"))
        
        self.button3 = wx.Button(self, id=-1, label='Button3',
            pos=(8, 68), size=(175, 28))
        self.button3.Bind(wx.EVT_BUTTON, self.button3Click)
        # optional tooltip
        self.button3.SetToolTip(wx.ToolTip("click to disable"))
        self.button4 = wx.Button(self, id=-1, label='Button4',
            pos=(8, 98), size=(175, 28))
        self.button4.Bind(wx.EVT_BUTTON, self.button4Click)
        # optional tooltip
        self.button4.SetToolTip(wx.ToolTip("click to disable"))
        
        self.button5 = wx.Button(self, id=-1, label='Button5',
            pos=(8, 128), size=(175, 28))
        self.button5.Bind(wx.EVT_RIGHT_DOWN, self.button5Click)
        # optional tooltip
        self.button5.SetToolTip(wx.ToolTip("right click"))
        self.button6 = wx.Button(self, id=-1, label='Button6',
            pos=(8, 158), size=(175, 28))
        self.button6.Bind(wx.EVT_LEFT_DCLICK, self.button6Click)
        # optional tooltip
        self.button6.SetToolTip(wx.ToolTip("left double click"))
        
        # show the frame
        self.Show(True)
    def button1Click(self,event):
        self.button1.Hide()
        self.SetTitle("Button1 clicked")
        self.button2.Show()
        
    def button2Click(self,event):
        self.button2.Hide()
        self.SetTitle("Button2 clicked")
        self.button1.Show()
    def button3Click(self,event):
        self.button3.Disable()
        self.SetTitle("Button3 clicked")
        self.button4.Enable()
    def button4Click(self,event):
        self.button4.Disable()
        self.SetTitle("Button4 clicked")
        self.button3.Enable()
        
    def button5Click(self,event):
        self.SetTitle("Button5 right-clicked")
        
    def button6Click(self,event):
        self.SetTitle("Button6 double-clicked")
application = wx.PySimpleApp()
# call class MyFrame
window = MyFrame()
# start the event loop
application.MainLoop()