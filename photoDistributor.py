# -*- coding: utf8 -*-

import os
import wx
import sys
import shutil
#import ExifTags
from PIL import Image
from enum import Enum
reload(sys)
sys.setdefaultencoding('utf-8')

class PhotoCtrl(wx.App):
    def __init__(self, debug_flag, env , redirect=False, filename=None):
        self.debug_flag = debug_flag
        self.env = env # OS: MAC or WINDOWS
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Photo Distributor')
        self.panel = wx.Panel(self.frame)

        self.PhotoMaxSize = 500
        self.photoTargetPath = None
        self.allPhotos = []
        self.currentPhotoIdx = 0
        self.tagListSizer = None
        self.tagStatus = {} # {photoIdx : {btnID:true, btnID:false}}

        self.Bind(wx.EVT_CHAR_HOOK, self.onKey) # Bind key event
        
        #image_file = 'assets/background.jpg'
        #bmp1 = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        #self.bitmap1 = wx.StaticBitmap(self.panel, -1, bmp1, (0, 0))
 
        self.frame.SetMinSize((1000,750)) 

        #Initialize widgets
        self.createComponents()
        self.drawLayout()
        self.frame.Show()
 
    def createComponents(self):
        # ============== Components & event ===================
        img = wx.EmptyImage(self.PhotoMaxSize,self.PhotoMaxSize)
        self.photoContainer = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.BitmapFromImage(img))
  
        # browse folder btn & path input bar
        self.browseFolderBtn = wx.Button(self.panel, label=unicode('開啟照片資料夾'))
        self.browseFolderBtn.Bind(wx.EVT_BUTTON, self.onBrowseFolder)
        self.photoTxt = wx.TextCtrl(self.panel, style=wx.TE_READONLY , size=(700,-1))

        # taget folder btn & path input bar
        self.targetFolderBtn = wx.Button(self.panel, label=unicode('設定目標資料夾'))
        self.targetFolderBtn.Bind(wx.EVT_BUTTON, self.onSetTargetFolder)
        self.targetPhotoTxt = wx.TextCtrl(self.panel, style=wx.TE_READONLY , size=(700,-1))

        # load tag list btn
        self.loadTagListBtn = wx.Button(self.panel, label=unicode('設定標籤清單檔案'))
        self.loadTagListBtn.Bind(wx.EVT_BUTTON, self.onSetTagListFile)
        self.tagListSettingTxt = wx.TextCtrl(self.panel, style=wx.TE_READONLY, size = (700,-1))

        # current photo path
        self.currentPhotoPathHint = wx.StaticText(self.panel, label=unicode('原始檔路徑: '))
        self.currentPhotoPathContent = wx.StaticText(self.panel, label=unicode('(請設定照片資料夾)'))

        # prev photo btn
        self.prevPhotoBtn = wx.Button(self.panel, label= unicode('<< 前一張'),  size = (230,-1))
        self.prevPhotoBtn.Bind(wx.EVT_BUTTON, lambda event: self.onPhotoChange(EnumPhotoCtrl.PREV))

        # next photo btn
        self.nextPhotoBtn = wx.Button(self.panel, label= unicode('下一張 >>'), size = (230,-1))
        self.nextPhotoBtn.Bind(wx.EVT_BUTTON, lambda event: self.onPhotoChange(EnumPhotoCtrl.NEXT))

        # clockwise rotato photo btn
        self.clkwiseRotateBtn = wx.Button(self.panel, label = unicode('順時針旋轉 ↻'), size = (230,-1))
        self.clkwiseRotateBtn.Bind(wx.EVT_BUTTON, lambda event: self.onPhotoRotate(EnumPhotoCtrl.CL_WISE))

        # counter-clockwise rotate photo btn
        self.c_clkwiseRotateBtn = wx.Button(self.panel, label = unicode('逆時針旋轉 ↺'), size = (230,-1))
        self.c_clkwiseRotateBtn.Bind(wx.EVT_BUTTON, lambda event: self.onPhotoRotate(EnumPhotoCtrl.C_CL_WISE))

    def drawLayout(self):
        #=================== Layout ============================
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.settingSizer = wx.BoxSizer(wx.VERTICAL)
        
        # source tolder
        self.browseFolderSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.browseFolderSizer.Add(self.photoTxt, 0, wx.ALL, 5)
        self.browseFolderSizer.Add(self.browseFolderBtn, 0, wx.ALL, 5)
        self.settingSizer.Add(self.browseFolderSizer, 0, wx.ALL, 5)

        # target folder
        self.targetFolderSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.targetFolderSizer.Add(self.targetPhotoTxt, 0, wx.ALL, 5)
        self.targetFolderSizer.Add(self.targetFolderBtn, 0, wx.ALL, 5)
        self.settingSizer.Add(self.targetFolderSizer, 0, wx.ALL, 5)

        # tag list btns
        self.tagListSettingSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.tagListSettingSizer.Add(self.tagListSettingTxt, 0, wx.ALL, 5)
        self.tagListSettingSizer.Add(self.loadTagListBtn, 0, wx.ALL, 5)
        self.settingSizer.Add(self.tagListSettingSizer, 0, wx.ALL, 5)

        self.photoMainSizer = wx.GridSizer(rows=0, cols=2, hgap=0, vgap=0)
        self.tagController = wx.BoxSizer(wx.VERTICAL)
        
        # photo controller
        self.photoController = wx.GridSizer(rows=0, cols=2, hgap=0, vgap=0)

        # rotate photo btns
        self.photoController.Add(self.c_clkwiseRotateBtn, 0 , wx.ALL, 5)
        self.photoController.Add(self.clkwiseRotateBtn, 0 , wx.ALL, 5)
        # prev btn & next btn
        self.photoController.Add(self.prevPhotoBtn, 0, wx.ALL, 5)
        self.photoController.Add(self.nextPhotoBtn, 0, wx.ALL, 5)
        
        self.tagController.Add(self.photoController, 0, wx.ALL, 5)

        self.photoMainSizer.Add(self.photoContainer, 0, wx.ALL, 5)
        self.photoMainSizer.Add(self.tagController, 0, wx.ALL, 5)

        # basic setting
        self.mainSizer.Add(self.settingSizer, 0, wx.ALL, 5)
        
        # source photo info path 
        self.mainSizer.Add(self.currentPhotoPathHint, 0, wx.ALL, 5)
        self.mainSizer.Add(self.currentPhotoPathContent, 0, wx.ALL, 5)
        
        # photo container && tag controller
        self.mainSizer.Add(self.photoMainSizer, 0, wx.ALL, 5)

        # Auto load settgin in debug mode
        self.debugMode()

        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
        self.panel.Layout()

    
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
            self.tagListSizer.DeleteWindows()

        self.tagListSizer = wx.GridSizer(rows=0, cols=5, hgap=3, vgap=3)
        self.tagBtn = []
        tagBtnIdx = 0
        # Extract tag list from file
        with open(self.tagListPath, "r") as f:
            for tag in f:
                tag = tag.replace("\n","").replace("\r","").strip()
                if self.env is EnumEnv.WINDOWS:
                    tag = tag.decode('big5')
                if len(tag) > 0:
                    print tag
                    # Dynamic generate tag btns & bind event
                    tagBtn = wx.ToggleButton(self.panel, label = unicode(tag))
                    tagBtn.Bind(wx.EVT_TOGGLEBUTTON, self.onTagPhoto)
                    # Append Btns to sizer
                    self.tagListSizer.Add(tagBtn, 0, wx.ALL, 5)
                    tagBtnIdx += 1
        # Append btns to panel
        self.tagController.Add(self.tagListSizer, 0, wx.ALL, 5)
        
        # refresh layout
        self.mainSizer.Layout()


    def onPhotoChange(self, PhotoCtrl):
        if PhotoCtrl == EnumPhotoCtrl.PREV and self.currentPhotoIdx > 0:
            self.currentPhotoIdx -= 1
        elif PhotoCtrl == EnumPhotoCtrl.NEXT and self.currentPhotoIdx < len(self.allPhotos) - 1:    
            self.currentPhotoIdx += 1
        
        self.onView(self.allPhotos[self.currentPhotoIdx])
        self.loadTagStatus()

    def onPhotoRotate(self, PhotoCtrl):
        filename = self.allPhotos[self.currentPhotoIdx]
        img = Image.open(filename)
        if PhotoCtrl == EnumPhotoCtrl.CL_WISE:
            print 'Rotate clickwise'
            img.rotate(-90, expand=True).save(filename)
        elif PhotoCtrl == EnumPhotoCtrl.C_CL_WISE:
            print 'Rotate counter-clockwise'
            img.rotate(90, expand=True).save(filename)


        self.onView(filename)

    def onTagPhoto(self,event):
        btn = event.GetEventObject()
        tagName = btn.GetLabel()
        isPress = btn.GetValue()
        btnID = btn.GetId()

        # Get the final target path for copy or delete
        finalTargetDir = os.path.join(self.photoTargetPath.encode('utf-8'),tagName.encode('utf-8'))
        sourceFile_fullpath = self.allPhotos[self.currentPhotoIdx]
        sourceFileName = os.path.basename(sourceFile_fullpath)
        finalTargetPath = os.path.join(finalTargetDir,sourceFileName)
        
        if self.env is EnumEnv.WINDOWS:
            finalTargetDir = finalTargetDir.decode('utf-8')
            finalTargetPath = finalTargetPath.decode('utf-8')
            self.allPhotos[self.currentPhotoIdx] = self.allPhotos[self.currentPhotoIdx].decode('utf-8')

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
                if filename.lower().endswith(('.jpg', '.jpeg' , '.gif', '.png')):                
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
 
        self.photoContainer.SetBitmap(wx.BitmapFromImage(img))
        self.currentPhotoPathContent.SetLabel(filepath)
        self.panel.Refresh()

    def setDebugMode(self,debug_flag):
        self.debug_flag = debug_flag

    def onKey(self,event):
        keyCode = event.GetKeyCode()
        if (keyCode == 316) or (keyCode == 317):
            # Next photo
            self.onPhotoChange(EnumPhotoCtrl.NEXT)
        if (keyCode == 314) or (keyCode == 315):
            # Prev photo
            self.onPhotoChange(EnumPhotoCtrl.PREV)


    def debugMode(self):
        if self.debug_flag is True:
            # photo source folder
            self.photoRootPath = unicode('/Users/Jordan/Dropbox/Projects/photoDistributor/test/test Imgs測試圖檔')
            self.photoTxt.SetValue(self.photoRootPath)
            self.getAllFiles(self.photoRootPath)    
            self.onView(self.allPhotos[0])            

            # target folder
            self.photoTargetPath = unicode('/Users/Jordan/Dropbox/Projects/photoDistributor/test/測試目標目錄')
            self.targetPhotoTxt.SetValue(self.photoTargetPath)

            # tag list setting file
            self.tagListPath = unicode('/Users/Jordan/Dropbox/Projects/photoDistributor/test/tagList測試檔案範例2')
            self.tagListSettingTxt.SetValue(self.tagListPath)
            self.genTagBtns()    
 
class EnumPhotoCtrl(Enum):
    PREV = 1 # previous photo
    NEXT = 2 # next photo
    CL_WISE = 3 # clockwise rotate photo
    C_CL_WISE = 4 # counter-clockwise rotate photo

class EnumEnv(Enum):
    MAC = 1
    WINDOWS = 2

if __name__ == '__main__':
    # Set True as debug mode (auto setting source folder, target folder, tag list file)
    app = PhotoCtrl(True,EnumEnv.MAC)
    app.MainLoop()