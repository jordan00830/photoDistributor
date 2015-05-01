# -*- coding: utf8 -*-

import os
import wx
import sys
import shutil
from enum import Enum
reload(sys)
sys.setdefaultencoding('utf-8')


ENV_SLASH = None
#ENV_SLASH = EnumEnvSlash.WINDOWS

class PhotoCtrl(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Photo Control')
        self.panel = wx.Panel(self.frame)
        self.PhotoMaxSize = 600
        #self.photoRootPath = None
        self.photoTargetPath = None
        self.allPhotos = []
        self.currentPhotoIdx = 0
        #Initialize widgets
        self.createWidgets()
        self.frame.Show()
 
    def createWidgets(self):
        # ============== Components & event ===================
        instructions = 'Browse for an image'
        
        img = wx.EmptyImage(600,600)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.BitmapFromImage(img))
 
        instructLbl = wx.StaticText(self.panel, label=instructions)
 
        # browse folder btn & path input bar
        browseFolderBtn = wx.Button(self.panel, label=unicode('開啟資料夾'))
        browseFolderBtn.Bind(wx.EVT_BUTTON, self.onBrowseFolder)
        self.photoTxt = wx.TextCtrl(self.panel, size=(600,-1))


        # taget folder btn & path input bar
        targetFolderBtn = wx.Button(self.panel, label=unicode('目標資料夾'))
        targetFolderBtn.Bind(wx.EVT_BUTTON, self.onSetTargetFolder)
        self.targetPhotoTxt = wx.TextCtrl(self.panel, size=(600,-1))


        # prev photo btn
        prevPhotoBtn = wx.Button(self.panel, label= unicode('前一張'))
        prevPhotoBtn.Bind(wx.EVT_BUTTON, lambda event: self.onPhotoChange(EnumPhotoCtrl.PREV))

        # next photo btn
        nextPhotoBtn = wx.Button(self.panel, label= unicode('下一張'))
        nextPhotoBtn.Bind(wx.EVT_BUTTON, lambda event: self.onPhotoChange(EnumPhotoCtrl.NEXT))

        # Test tag btns
        tagBtn1 = wx.Button(self.panel, label= unicode('TEST_TAG1測試'))
        tagBtn2 = wx.Button(self.panel, label= unicode('TEST_TAG2測試'))
        tagBtn3 = wx.Button(self.panel, label= unicode('TEST_TAG3測試'))
        tagBtn4 = wx.Button(self.panel, label= unicode('TEST_TAG4'))

        tagBtn1.Bind(wx.EVT_BUTTON, lambda event: self.onTagPhoto(tagBtn1.GetLabel()))
        tagBtn2.Bind(wx.EVT_BUTTON, lambda event: self.onTagPhoto(tagBtn2.GetLabel()))
        tagBtn3.Bind(wx.EVT_BUTTON, lambda event: self.onTagPhoto(tagBtn3.GetLabel()))
        tagBtn4.Bind(wx.EVT_BUTTON, lambda event: self.onTagPhoto(tagBtn4.GetLabel()))

        #=======================================================

        #=================== Layout ============================
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer4 = wx.BoxSizer(wx.HORIZONTAL)

        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL|wx.EXPAND, 5)
        self.mainSizer.Add(instructLbl, 0, wx.ALL, 5)
        
        self.sizer.Add(self.photoTxt, 0, wx.ALL, 5)
        self.sizer.Add(browseFolderBtn, 0, wx.ALL, 5)
        self.sizer2.Add(self.targetPhotoTxt, 0, wx.ALL, 5)
        self.sizer2.Add(targetFolderBtn, 0, wx.ALL, 5)
        self.sizer3.Add(prevPhotoBtn, 0, wx.ALL, 5)
        self.sizer3.Add(nextPhotoBtn, 0, wx.ALL, 5)

        self.sizer4.Add(tagBtn1,0,wx.ALL,5)
        self.sizer4.Add(tagBtn2,0,wx.ALL,5)
        self.sizer4.Add(tagBtn3,0,wx.ALL,5)
        self.sizer4.Add(tagBtn4,0,wx.ALL,5)

        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizer2, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizer3, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizer4, 0, wx.ALL, 5)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
 
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
 
        self.panel.Layout()
    
        #=======================================================

    '''
    Brose a root folder
    '''
    def onBrowseFolder(self,event):
        dialog = wx.DirDialog(None, "Choose root folder",style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            #self.photoRootPath = dialog.GetPath()
            photoRootPath = dialog.GetPath()
            self.photoTxt.SetValue(photoRootPath)
            self.getAllFiles(photoRootPath)
        #Show first photo
        self.onView(self.allPhotos[0])
            
        dialog.Destroy()

    def onSetTargetFolder(self,event):
        dialog = wx.DirDialog(None, "Choose target folder",style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoTargetPath = dialog.GetPath()
            self.targetPhotoTxt.SetValue(self.photoTargetPath)
        dialog.Destroy()

    def onPhotoChange(self, PhotoCtrl):
        if PhotoCtrl == EnumPhotoCtrl.PREV and self.currentPhotoIdx > 0:
            self.currentPhotoIdx -= 1
        elif PhotoCtrl == EnumPhotoCtrl.NEXT and self.currentPhotoIdx < len(self.allPhotos) - 1:    
            self.currentPhotoIdx += 1
        
        self.onView(self.allPhotos[self.currentPhotoIdx])

    def onTagPhoto(self,tagName):
        finalTargetDir = self.photoTargetPath.encode('utf-8') + ENV_SLASH + tagName.encode('utf-8')
        print finalTargetDir
        if os.path.exists(finalTargetDir) and os.path.isdir(finalTargetDir):
            print 'dir exists, put file directly'
        else:
            print 'dir not exist, mkdir'    
            os.mkdir(finalTargetDir)
        sourceFile_fullpath = self.allPhotos[self.currentPhotoIdx]
        sourceFileName = sourceFile_fullpath.split(ENV_SLASH)[-1]
        shutil.copyfile(self.allPhotos[self.currentPhotoIdx], finalTargetDir + ENV_SLASH + sourceFileName)        


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

class EnumEnvSlash(Enum):
    WINDOWS = '\\'
    MAC_LINUX = '/'

if __name__ == '__main__':
    global ENV_SLASH
    ENV_SLASH = EnumEnvSlash.MAC_LINUX
    app = PhotoCtrl()
    app.MainLoop()