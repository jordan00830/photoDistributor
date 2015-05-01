# -*- coding: utf8 -*-

import os
import wx
import sys
from enum import Enum
reload(sys)
sys.setdefaultencoding('utf-8')

class PhotoCtrl(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Photo Control')
        self.panel = wx.Panel(self.frame)
        self.PhotoMaxSize = 600
        #self.photoRootPath = None
        self.allPhotos = []
        self.currentPhotoIdx = 0
        #Initialize widgets
        self.createWidgets()
        self.frame.Show()
 
    def createWidgets(self):
        # Components & event
        instructions = 'Browse for an image'
        
        img = wx.EmptyImage(600,600)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.BitmapFromImage(img))
 
        instructLbl = wx.StaticText(self.panel, label=instructions)
        self.photoTxt = wx.TextCtrl(self.panel, size=(600,-1))
 

        browseFolderBtn = wx.Button(self.panel, label=unicode('開啟資料夾'))
        browseFolderBtn.Bind(wx.EVT_BUTTON, self.onBrowseFolder)

        prevPhotoBtn = wx.Button(self.panel, label= unicode('前一張'))
        prevPhotoBtn.Bind(wx.EVT_BUTTON, lambda event: self.onPhotoChange(EnumPhotoCtrl.PREV))

        nextPhotoBtn = wx.Button(self.panel, label= unicode('下一張'))
        nextPhotoBtn.Bind(wx.EVT_BUTTON, lambda event: self.onPhotoChange(EnumPhotoCtrl.NEXT))


        # Layout
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
 
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL|wx.EXPAND, 5)
        self.mainSizer.Add(instructLbl, 0, wx.ALL, 5)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
        self.sizer.Add(self.photoTxt, 0, wx.ALL, 5)
        self.sizer.Add(browseFolderBtn, 0, wx.ALL, 5)
        self.sizer.Add(prevPhotoBtn, 0, wx.ALL, 5)
        self.sizer.Add(nextPhotoBtn, 0, wx.ALL, 5)

        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)
 
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
 
        self.panel.Layout()
     
    def onPhotoChange(self, PhotoCtrl):
        if PhotoCtrl == EnumPhotoCtrl.PREV and self.currentPhotoIdx > 0:
            self.currentPhotoIdx -= 1
        elif PhotoCtrl == EnumPhotoCtrl.NEXT and self.currentPhotoIdx < len(self.allPhotos) - 1:    
            self.currentPhotoIdx += 1
        
        self.onView(self.allPhotos[self.currentPhotoIdx])

            

    def onBrowseFolder(self, event):
        '''
        Brose a root folder
        '''
        dialog = wx.DirDialog(None, "Choose root folder",style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            #self.photoRootPath = dialog.GetPath()
            photoRootPath = dialog.GetPath()
            self.photoTxt.SetValue(photoRootPath)
            self.getAllFiles(photoRootPath)
        #Show first photo
        self.onView(self.allPhotos[0])
            
        dialog.Destroy()

    def getAllFiles(self,rootPath):
        self.allPhotos = []
        for root, dirnames, filenames in os.walk(rootPath):
            for filename in filenames:
                if filename.endswith(('.jpg', '.jpeg', '.gif', '.png')):
                    self.allPhotos.append(os.path.join(root, filename).encode('utf-8'))
        print self.allPhotos
        print 'Total #Files: ' , len(self.allPhotos)            

    def onView(self,filepath):
        filepath = unicode(filepath)
        #filepath = self.photoTxt.GetValue()
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW,NewH)
 
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.panel.Refresh()
 
class EnumPhotoCtrl(Enum):
    PREV = 1
    NEXT = 2

if __name__ == '__main__':
    app = PhotoCtrl()
    app.MainLoop()