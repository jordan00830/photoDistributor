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
    def __init__(self, debug_flag , redirect=False, filename=None):
        self.debug_flag = debug_flag
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Photo Distributor')
        self.panel = wx.Panel(self.frame)
        #self.tagListPanel = wx.Panel(self.frame)
        self.PhotoMaxSize = 400
        self.photoTargetPath = None
        self.allPhotos = []
        self.currentPhotoIdx = 0
        self.tagListSizer = None
        self.tagStatus = {} # {photoIdx : {btnID:true, btnID:false}}

        #Initialize widgets
        self.createComponents()
        self.drawLayout()
        self.frame.Show()
 
    def createComponents(self):
        # ============== Components & event ===================
        instructions = 'Browse for an image'
        
        img = wx.EmptyImage(self.PhotoMaxSize,self.PhotoMaxSize)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.BitmapFromImage(img))
 
        self.instructLbl = wx.StaticText(self.panel, label=instructions)
 
        # browse folder btn & path input bar
        self.browseFolderBtn = wx.Button(self.panel, label=unicode('開啟照片資料夾'))
        self.browseFolderBtn.Bind(wx.EVT_BUTTON, self.onBrowseFolder)
        self.photoTxt = wx.TextCtrl(self.panel, style=wx.TE_READONLY , size=(600,-1))

        # taget folder btn & path input bar
        self.targetFolderBtn = wx.Button(self.panel, label=unicode('設定目標資料夾'))
        self.targetFolderBtn.Bind(wx.EVT_BUTTON, self.onSetTargetFolder)
        self.targetPhotoTxt = wx.TextCtrl(self.panel, style=wx.TE_READONLY , size=(600,-1))

        # load tag list btn
        self.loadTagListBtn = wx.Button(self.panel, label=unicode('設定標籤清單檔案'))
        self.loadTagListBtn.Bind(wx.EVT_BUTTON, self.onSetTagListFile)
        self.tagListSettingTxt = wx.TextCtrl(self.panel, style=wx.TE_READONLY, size = (600,-1))

        # prev photo btn
        self.prevPhotoBtn = wx.Button(self.panel, label= unicode('前一張'))
        self.prevPhotoBtn.Bind(wx.EVT_BUTTON, lambda event: self.onPhotoChange(EnumPhotoCtrl.PREV))

        # next photo btn
        self.nextPhotoBtn = wx.Button(self.panel, label= unicode('下一張'))
        self.nextPhotoBtn.Bind(wx.EVT_BUTTON, lambda event: self.onPhotoChange(EnumPhotoCtrl.NEXT))

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
        
        # Setting btns
        self.sizer.Add(self.photoTxt, 0, wx.ALL, 5)
        self.sizer.Add(self.browseFolderBtn, 0, wx.ALL, 5)
        self.sizer2.Add(self.targetPhotoTxt, 0, wx.ALL, 5)
        self.sizer2.Add(self.targetFolderBtn, 0, wx.ALL, 5)
        self.sizer3.Add(self.tagListSettingTxt, 0, wx.ALL, 5)              
        self.sizer3.Add(self.loadTagListBtn, 0, wx.ALL, 5)

        # photo control btns
        self.sizer4.Add(self.prevPhotoBtn, 0, wx.ALL, 5)
        self.sizer4.Add(self.nextPhotoBtn, 0, wx.ALL, 5)

        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizer2, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizer3, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizer4, 0, wx.ALL, 5)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)

        # Auto load settgin in debug mode
        self.debugMode()

        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
        self.panel.Layout()
    
        #=======================================================

    def onBrowseFolder(self,event):
        dialog = wx.DirDialog(None, "Choose root folder",style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoRootPath = dialog.GetPath()
            self.photoTxt.SetValue(self.photoRootPath)
            self.getAllFiles(self.photoRootPath)
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
        self.tagStatus = {} # {photoIdx : {btnID:true, btnID:false}} (reinitialize)
        dialog = wx.FileDialog(None, "Choose a file", wildcard='*', style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.tagListPath = dialog.GetPath()
            self.tagListSettingTxt.SetValue(self.tagListPath)
        dialog.Destroy()
        self.genTagBtns()    

    def genTagBtns(self):
        # Remove old tag list (if exist)
        if self.tagListSizer is not None:
            print 'REMOVE old tagListSizer'
            self.mainSizer.Remove(self.tagListSizer)
            
        self.tagListSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.tagBtn = []
        tagBtnIdx = 0
        # Extract tag list from file
        with open(self.tagListPath, "r") as f:
            for tag in f:
                tag = tag.strip()
                if len(tag) > 0:
                    print tag
                    # Dynamic generate tag btns & bind event
                    tagBtn = wx.ToggleButton(self.panel, label = unicode(tag))
                    tagBtn.Bind(wx.EVT_TOGGLEBUTTON, self.onTagPhoto)
                    # Append Btns to sizer
                    self.tagListSizer.Add(tagBtn, 0, wx.ALL, 5)
                    tagBtnIdx += 1
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
        self.loadTagStatus()


    def onTagPhoto(self,event):
        btn = event.GetEventObject()
        tagName = btn.GetLabel()
        isPress = btn.GetValue()
        btnID = btn.GetId()

        # Get the final target path for copy or delete
        finalTargetDir = self.photoTargetPath.encode('utf-8') + ENV_SLASH + tagName.encode('utf-8')
        sourceFile_fullpath = self.allPhotos[self.currentPhotoIdx]
        sourceFileName = sourceFile_fullpath.split(ENV_SLASH)[-1]
        finalTargetPath = finalTargetDir + ENV_SLASH + sourceFileName
        
        if not os.path.exists(finalTargetDir) or not os.path.isdir(finalTargetDir):
            print 'dir not exist, mkdir'    
            os.mkdir(finalTargetDir)
        # copy the file to target folder
        if isPress is True:
            print 'copy file to target folder'    
            shutil.copyfile(self.allPhotos[self.currentPhotoIdx], finalTargetPath)        
            self.saveTagStatus(btnID,isPress)
        # delete target folder file
        elif isPress is False:
            print 'delete target file'
            if os.path.exists(finalTargetPath):
                os.remove(finalTargetPath)
            self.saveTagStatus(btnID,isPress)


    def saveTagStatus(self,btnID,isPress):
        # initialize if have not set
        if self.currentPhotoIdx not in self.tagStatus:
            self.tagStatus[self.currentPhotoIdx] = {}
        # save status
        self.tagStatus[self.currentPhotoIdx][str(btnID)] = isPress

    def loadTagStatus(self):
        #Refresh all tag btn to non-press
        for tagBtn in self.tagListSizer.GetChildren():
            tagBtn.GetWindow().SetValue(False)

        # only handle changed photo index
        if self.currentPhotoIdx in self.tagStatus:
            print self.tagStatus
            for btnID, isPress in self.tagStatus[self.currentPhotoIdx].items():
                self.tagListSizer.GetContainingWindow().FindWindowById(long(btnID)).SetValue(isPress)

        # Refresh layout
        self.panel.Refresh()

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

    def setDebugMode(self,debug_flag):
        self.debug_flag = debug_flag

    def debugMode(self):
        if self.debug_flag is True:
            # photo source folder
            self.photoRootPath = unicode('/Users/Jordan/Dropbox/Projects/photoDistributor/test Imgs測試圖檔')
            self.photoTxt.SetValue(self.photoRootPath)
            self.getAllFiles(self.photoRootPath)    
            self.onView(self.allPhotos[0])            

            # target folder
            self.photoTargetPath = unicode('/Users/Jordan/Dropbox/Projects/photoDistributor/測試目標目錄')
            self.targetPhotoTxt.SetValue(self.photoTargetPath)

            # tag list setting file
            self.tagListPath = unicode('/Users/Jordan/Dropbox/Projects/photoDistributor/tagList測試檔案範例2')
            self.tagListSettingTxt.SetValue(self.tagListPath)
            self.genTagBtns()    

 
class EnumPhotoCtrl(Enum):
    PREV = 1
    NEXT = 2

class EnumEnvSlash(Enum):
    WINDOWS = '\\'
    MAC_LINUX = '/'

if __name__ == '__main__':
    global ENV_SLASH
    ENV_SLASH = EnumEnvSlash.MAC_LINUX
    # Set True as debug mode (auto setting source folder, target folder, tag list file)
    app = PhotoCtrl(True)
    app.MainLoop()