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
        #self.tagListPanel = wx.Panel(self.frame)
        self.PhotoMaxSize = 600
        self.photoTargetPath = None
        self.allPhotos = []
        self.currentPhotoIdx = 0
        self.tagListSizer = None

        #Initialize widgets
        self.createComponents()
        self.drawLayout()
        self.frame.Show()
 
    def createComponents(self):
        # ============== Components & event ===================
        instructions = 'Browse for an image'
        
        img = wx.EmptyImage(600,600)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.BitmapFromImage(img))
 
        self.instructLbl = wx.StaticText(self.panel, label=instructions)
 
        # browse folder btn & path input bar
        self.browseFolderBtn = wx.Button(self.panel, label=unicode('開啟照片資料夾'))
        self.browseFolderBtn.Bind(wx.EVT_BUTTON, self.onBrowseFolder)
        self.photoTxt = wx.TextCtrl(self.panel, size=(600,-1))


        # taget folder btn & path input bar
        self.targetFolderBtn = wx.Button(self.panel, label=unicode('設定目標資料夾'))
        self.targetFolderBtn.Bind(wx.EVT_BUTTON, self.onSetTargetFolder)
        self.targetPhotoTxt = wx.TextCtrl(self.panel, size=(600,-1))

        # loag tag list btn
        self.loadTagListBtn = wx.Button(self.panel, label=unicode('設定標籤清單檔案'))
        self.loadTagListBtn.Bind(wx.EVT_BUTTON, self.onSetTagListFile)

        # prev photo btn
        self.prevPhotoBtn = wx.Button(self.panel, label= unicode('前一張'))
        self.prevPhotoBtn.Bind(wx.EVT_BUTTON, lambda event: self.onPhotoChange(EnumPhotoCtrl.PREV))

        # next photo btn
        self.nextPhotoBtn = wx.Button(self.panel, label= unicode('下一張'))
        self.nextPhotoBtn.Bind(wx.EVT_BUTTON, lambda event: self.onPhotoChange(EnumPhotoCtrl.NEXT))

        # Test tag btns
        #self.tagBtn1 = wx.Button(self.panel, label= unicode('TEST_TAG1測試'))
        #self.tagBtn2 = wx.Button(self.panel, label= unicode('TEST_TAG2測試'))
        #self.tagBtn3 = wx.Button(self.panel, label= unicode('TEST_TAG3測試'))
        #self.tagBtn4 = wx.Button(self.panel, label= unicode('TEST_TAG4'))

        #self.tagBtn1.Bind(wx.EVT_BUTTON, self.onTagPhoto)
        #self.tagBtn2.Bind(wx.EVT_BUTTON, self.onTagPhoto)
        #self.tagBtn3.Bind(wx.EVT_BUTTON, self.onTagPhoto)
        #self.tagBtn4.Bind(wx.EVT_BUTTON, self.onTagPhoto)

        #=======================================================

        

    def drawLayout(self):
        #=================== Layout ============================
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer4 = wx.BoxSizer(wx.HORIZONTAL)

        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL|wx.EXPAND, 5)
        self.mainSizer.Add(self.instructLbl, 0, wx.ALL, 5)
        
        self.sizer.Add(self.photoTxt, 0, wx.ALL, 5)
        self.sizer.Add(self.browseFolderBtn, 0, wx.ALL, 5)
        self.sizer2.Add(self.targetPhotoTxt, 0, wx.ALL, 5)
        self.sizer2.Add(self.targetFolderBtn, 0, wx.ALL, 5)
        self.sizer3.Add(self.prevPhotoBtn, 0, wx.ALL, 5)
        self.sizer3.Add(self.nextPhotoBtn, 0, wx.ALL, 5)
        self.sizer3.Add(self.loadTagListBtn, 0, wx.ALL, 5)

        #self.sizer4.Add(self.tagBtn1,0,wx.ALL,5)
        #self.sizer4.Add(self.tagBtn2,0,wx.ALL,5)
        #self.sizer4.Add(self.tagBtn3,0,wx.ALL,5)
        #self.sizer4.Add(self.tagBtn4,0,wx.ALL,5)

        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizer2, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizer3, 0, wx.ALL, 5)
        #self.mainSizer.Add(self.sizer4, 0, wx.ALL, 5)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
 
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
 
        self.panel.Layout()
    
        #=======================================================

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

    def onSetTagListFile(self,event):
        dialog = wx.FileDialog(None, "Choose a file", wildcard='*', style=wx.OPEN)
        #dialog = wx.DirDialog(None, "Choose tag list setting file", style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.tagListPath = dialog.GetPath()
        dialog.Destroy()    
        # Extract tag list from file
        #self.tagList = []
        if self.tagListSizer is not None:
            print 'REMOVE tagListSizer'
            self.mainSizer.Remove(self.tagListSizer)
            
        self.tagListSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.tagBtn = []
        tagBtnIdx = 0
        with open(self.tagListPath, "r") as f:
            for tag in f:
                tag = tag.strip()
                if len(tag) > 0:
                    print tag
                    # Dynamic generate tag btns & bind event
                    print 'XDDDDD'
                    tagBtn = wx.ToggleButton(self.panel, label = unicode(tag))
                    tagBtn.Bind(wx.EVT_TOGGLEBUTTON, self.onTagPhoto)
                    # Append Btns to sizer
                    self.tagListSizer.Add(tagBtn, 0, wx.ALL, 5)
                    tagBtnIdx += 1
        #print 'length of self.tagBtn ' ,len(self.tagBtn)
        # Append btns to panel & reload it
        self.mainSizer.Add(self.tagListSizer, 0, wx.ALL, 5)
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
        self.panel.Layout()


    def onPhotoChange(self, PhotoCtrl):
        if PhotoCtrl == EnumPhotoCtrl.PREV and self.currentPhotoIdx > 0:
            self.currentPhotoIdx -= 1
        elif PhotoCtrl == EnumPhotoCtrl.NEXT and self.currentPhotoIdx < len(self.allPhotos) - 1:    
            self.currentPhotoIdx += 1
        
        self.onView(self.allPhotos[self.currentPhotoIdx])

    def onTagPhoto(self,event):
        btn = event.GetEventObject()
        tagName = btn.GetLabel()
        isPress = btn.GetValue()
        print tagName.encode('utf-8') , ' pressed ', ' , btn status is ', isPress
        finalTargetDir = self.photoTargetPath.encode('utf-8') + ENV_SLASH + tagName.encode('utf-8')
        sourceFile_fullpath = self.allPhotos[self.currentPhotoIdx]
        sourceFileName = sourceFile_fullpath.split(ENV_SLASH)[-1]
        finalTargetPath = finalTargetDir + ENV_SLASH + sourceFileName
        
        print finalTargetDir
        if os.path.exists(finalTargetDir) and os.path.isdir(finalTargetDir):
            print 'dir exists, put file directly'
        else:
            print 'dir not exist, mkdir'    
            os.mkdir(finalTargetDir)
        # copy the file to target folder
        if isPress is True:    
            shutil.copyfile(self.allPhotos[self.currentPhotoIdx], finalTargetPath)        
        # delete target folder file
        elif isPress is False:
            os.remove(finalTargetPath)

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