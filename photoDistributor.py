# -*- coding: utf8 -*-

import os
import wx
import sys
import shutil
#import ExifTags
# from PIL import Image
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
        #self.panel.Bind(wx.EVT_SIZE, self.onResizeWindow)

        self.PhotoMaxSize = 500
        self.photoTargetPath = None
        self.allPhotos = []
        self.currentPhotoIdx = 0
        self.tagListSizer = None
        self.tagStatus = {} # {photoIdx : {btnID:true, btnID:false}}
        self.btnIdTagNameMap = {} # {btnID : tagName,...}

        self.Bind(wx.EVT_CHAR_HOOK, self.onKey) # Bind key event
        
        #image_file = 'assets/background.jpg'
        #bmp1 = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        #self.bitmap1 = wx.StaticBitmap(self.panel, -1, bmp1, (0, 0))
 
        self.frameWidth = 1000
        self.frameHeight = 750

        self.frame.SetMinSize((self.frameWidth,self.frameHeight)) 

        #Initialize widgets
        self.createComponents()
        self.drawLayout()
        self.frame.Show()
    
    #def onResizeWindow(self,event):
    #    print 'Window RESIZE!!!!!'
    #    self.panel.Layout()

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
        self.prevPhotoBtn = wx.Button(self.panel, label= unicode('<< 前一張'),  size = (155,-1))
        self.prevPhotoBtn.Bind(wx.EVT_BUTTON, lambda event: self.onPhotoChange(EnumPhotoCtrl.PREV))

        # next photo btn
        self.nextPhotoBtn = wx.Button(self.panel, label= unicode('下一張 >>'), size = (155,-1))
        self.nextPhotoBtn.Bind(wx.EVT_BUTTON, lambda event: self.onPhotoChange(EnumPhotoCtrl.NEXT))

        # previous tags btn
        self.prevTagsBtn = wx.Button(self.panel, label= unicode('套用上一張照片設定'), size = (155,-1))
        self.prevTagsBtn.Bind(wx.EVT_BUTTON, lambda event: self.onTagPrevSetting())

        # clockwise rotato photo btn
        # self.clkwiseRotateBtn = wx.Button(self.panel, label = unicode('順時針旋轉 ↻'), size = (230,-1))
        # self.clkwiseRotateBtn.Bind(wx.EVT_BUTTON, lambda event: self.onPhotoRotate(EnumPhotoCtrl.CL_WISE))

        # # counter-clockwise rotate photo btn
        # self.c_clkwiseRotateBtn = wx.Button(self.panel, label = unicode('逆時針旋轉 ↺'), size = (230,-1))
        # self.c_clkwiseRotateBtn.Bind(wx.EVT_BUTTON, lambda event: self.onPhotoRotate(EnumPhotoCtrl.C_CL_WISE))

        # author information
        self.authorInfo = wx.StaticText(self.panel,label=unicode('- Power by Jordan Hsu, jordan00830@gmail.com -'),size = (self.frameWidth,15),  style=wx.ALIGN_CENTER)

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
        self.photoController = wx.GridSizer(rows=0, cols=3, hgap=0, vgap=0)

        # rotate photo btns
        # self.photoController.Add(self.c_clkwiseRotateBtn, 0 , wx.ALL, 5)
        # self.photoController.Add(self.clkwiseRotateBtn, 0 , wx.ALL, 5)
        
        # # prev btn & prev tags btn & next btn
        self.photoController.Add(self.prevPhotoBtn, 0, wx.ALL, 5)
        self.photoController.Add(self.prevTagsBtn, 0 , wx.ALL, 5)
        self.photoController.Add(self.nextPhotoBtn, 0, wx.ALL, 5)
        
        self.tagController.Add(self.photoController, 0, wx.ALL, 5)

        self.photoMainSizer.Add(self.photoContainer, 0, wx.ALL, 5)
        self.photoMainSizer.Add(self.tagController, 0, wx.ALL, 5)

        # author info
        self.mainSizer.Add(self.authorInfo, 0 , wx.ALL, 5)

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
        dialog = wx.DirDialog(None, "Choose root folder",style=wx.DD_DEFAULT_STYLE)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoRootPath = dialog.GetPath()
            self.photoTxt.SetValue(self.photoRootPath)
            self.getAllFiles(self.photoRootPath)
        #Show first photo
        self.onView(self.allPhotos[0])            
        dialog.Destroy()

    def onSetTargetFolder(self,event):
        dialog = wx.DirDialog(None, "Choose target folder",style=wx.DD_DEFAULT_STYLE)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoTargetPath = dialog.GetPath()
            self.targetPhotoTxt.SetValue(self.photoTargetPath)
        dialog.Destroy()

    def onSetTagListFile(self,event):
        self.tagStatus = {} # {photoIdx : {btnID:true, btnID:false}} (reinitialize)
        dialog = wx.FileDialog(None, "Choose a file", wildcard='*', style=wx.DD_DEFAULT_STYLE)
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
            print '====== tag list ====='
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
            print '===================='
        # Append btns to panel
        self.tagController.Add(self.tagListSizer, 0, wx.ALL, 5)
        
        # refresh layout
        self.mainSizer.Layout()

    def onPhotoChange(self, PhotoCtrl):
        if PhotoCtrl == EnumPhotoCtrl.PREV:
            if self.currentPhotoIdx > 0:
                self.currentPhotoIdx -= 1
            elif self.currentPhotoIdx == 0:
                wx.MessageDialog(self.panel, style=wx.OK|wx.CENTRE, message=unicode("已經是第一張照片啦！")).ShowModal()
        
        elif PhotoCtrl == EnumPhotoCtrl.NEXT:    
            if self.currentPhotoIdx < len(self.allPhotos) - 1:
                self.currentPhotoIdx += 1
            elif self.currentPhotoIdx == len(self.allPhotos) - 1:
                wx.MessageDialog(self.panel, style=wx.OK|wx.CENTRE, message=unicode("已經是最後一張照片啦！")).ShowModal()

        self.onView(self.allPhotos[self.currentPhotoIdx])
        self.loadTagStatus()

    def onPhotoRotate(self, PhotoCtrl):
        filename = self.allPhotos[self.currentPhotoIdx]
        # img = Image.open(filename)
        # if PhotoCtrl == EnumPhotoCtrl.CL_WISE:
        #     print 'Rotate clickwise'
        #     img.rotate(-90, expand=True).save(filename)
        # elif PhotoCtrl == EnumPhotoCtrl.C_CL_WISE:
        #     print 'Rotate counter-clockwise'
        #     img.rotate(90, expand=True).save(filename)
 
        self.onView(filename)

    def onTagPrevSetting(self):
        print 'load previous photo tags setting'
        if self.currentPhotoIdx == 0:
            wx.MessageDialog(self.panel, style=wx.OK|wx.CENTRE, message=unicode("沒有上一張照片的設定")).ShowModal()
        else:
            for btnID, isBtnPress in self.tagStatus[self.currentPhotoIdx -1].items():
                if btnID in self.btnIdTagNameMap:
                    tagName = self.btnIdTagNameMap[btnID]
                    # copy files
                    self.copyFile(tagName, isBtnPress, btnID)
            self.loadTagStatus()

    def onTagPhoto(self,event):
        btn = event.GetEventObject()
        tagName = btn.GetLabel()
        isBtnPress = btn.GetValue()
        btnID = btn.GetId()
        self.copyFile(tagName, isBtnPress, btnID)
        self.updatebtnIdTagNameMap(btnID, tagName)

    def copyFile(self, tagName, isBtnPress, btnID):
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
            print 'folder ' + tagName + ' not exist, mkdir'
            os.mkdir(finalTargetDir)
        # copy the file to target folder
        if isBtnPress is True:
            print 'copy file ' + self.allPhotos[self.currentPhotoIdx] + ' to target folder ' + tagName
            shutil.copyfile(self.allPhotos[self.currentPhotoIdx], finalTargetPath)        
            self.saveTagStatus(btnID,isBtnPress)
        # delete target folder file
        elif isBtnPress is False:
            print 'delete target file'
            if os.path.exists(finalTargetPath):
                os.remove(finalTargetPath)
            self.saveTagStatus(btnID,isBtnPress)

    def updatebtnIdTagNameMap(self, btnID, tagName):
        if not str(btnID) in self.btnIdTagNameMap:
            self.btnIdTagNameMap[str(btnID)] = tagName

        print 'btnIdTagNameMap: '
        print self.btnIdTagNameMap


    def saveTagStatus(self,btnID,isBtnPress):
        # initialize if have not set
        if self.currentPhotoIdx not in self.tagStatus:
            self.tagStatus[self.currentPhotoIdx] = {}
        # save status
        self.tagStatus[self.currentPhotoIdx][str(btnID)] = isBtnPress

    def loadTagStatus(self):
        #Refresh all tag btn to non-press
        for tagBtn in self.tagListSizer.GetChildren():
            tagBtn.GetWindow().SetValue(False)

        # only handle changed photo index
        if self.currentPhotoIdx in self.tagStatus:
            print self.tagStatus
            for btnID, isBtnPress in self.tagStatus[self.currentPhotoIdx].items():
                self.tagListSizer.GetContainingWindow().FindWindowById(long(btnID)).SetValue(isBtnPress)

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
        self.currentImg = img

        self.photoContainer.SetBitmap(wx.BitmapFromImage(img))
        self.currentPhotoPathContent.SetLabel(filepath)
        self.panel.Refresh()

    def setDebugMode(self,debug_flag):
        self.debug_flag = debug_flag

    def onKey(self,event):
        keyCode = event.GetKeyCode()
        if keyCode in (EnumKeyCode.ARROW_RIGHT, EnumKeyCode.ARROW_DOWN):
            # Next photo
            self.onPhotoChange(EnumPhotoCtrl.NEXT)
        if keyCode in (EnumKeyCode.ARROW_LEFT, EnumKeyCode.ARROW_UP):
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
            self.tagListPath = unicode('/Users/Jordan/Dropbox/Projects/photoDistributor/test/tagList標籤清單檔案範例_MAC')
            self.tagListSettingTxt.SetValue(self.tagListPath)
            self.genTagBtns()    
 
class EnumPhotoCtrl(Enum):
    PREV = 1 # previous photo
    NEXT = 2 # next photo
    CL_WISE = 3 # clockwise rotate photo
    C_CL_WISE = 4 # counter-clockwise rotate photo

class EnumKeyCode(Enum):
    ARROW_LEFT = 314
    ARROW_UP = 315
    ARROW_RIGHT = 316
    ARROW_DOWN = 317

class EnumEnv(Enum):
    MAC = 1
    WINDOWS = 2