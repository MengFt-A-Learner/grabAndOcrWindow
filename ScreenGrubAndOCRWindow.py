# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 17:16:45 2022
#整体工作流程：
1.开启一个窗口
2.点击“截图拾取”按钮-->隐藏窗口，截图保存-->用ocr功能识别图片-->恢复窗口，显示结果
3.点击“导入图片”按钮-->子窗口，选取图片-->用用ocr功能识别图片-->显示结果

@author: MengFt
"""
from GrubAndCutScreen import GrubAndCutScreen
import easyocr
import cv2
import PySimpleGUI as sg
from PIL import ImageGrab
import time

class ScreenGrabAndOCRWindow(object):
    def __init__(self):
        print("初始化了一个截屏和OCR的窗口工具")
        self.imagePathList=[]
        self.imagePathHead=r'.\imgLib'
        self.grubWindowTool=GrubAndCutScreen()
        self.ocrReader=easyocr.Reader(['ch_sim','en'], gpu = False) # need to run only once to load model into memory

    #读取屏幕尺寸，用于设置窗口大小和位置
    def getScreenSize(self):
        image = ImageGrab.grab()

        height=image.height
        width=image.width
        return (width,height)
    
    def createNewImgPath(self):
        imgNumber=len(self.imagePathList)
        tempImgPath=self.imagePathHead+"\\"+str(imgNumber)+".png"
        self.imagePathList.append(tempImgPath)
        return tempImgPath
    #读取当前时间
    def currentTime(self):
        currentTime=time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime( int(time.time())))
        return currentTime
    #OCR识别函数
    def ocrFromImage(self,inputImage):        
        try:
            result = self.ocrReader.readtext(inputImage, paragraph="False")
            resultSring=""
            #resultSring="#"
            for i in result:
                resultSring+=i[1]
                resultSring+=" "
            #print(resultSring)
            #resultSring+="#"
            return resultSring
        except Exception as e:
            tempEString="#"+str(e)+"#"
            print(tempEString)
            return None

    #截图并识别函数
    def grabAndRead(self):
        self.ocrWindow.hide()
        #更新图片
        self.grubWindowTool.imagePath=self.createNewImgPath()
        currentImgPath=self.grubWindowTool.imageCutWithMouse()
        print("截取图片，并保存入：",currentImgPath)
        self.ocrWindow.UnHide()
        #调用easyocr，识别图片
        ocrResult=self.ocrFromImage(currentImgPath)
        #如识别失败，返回None
        if ocrResult==None:    
            return 0
        #如识别成功，在窗口中换行并显式
        else:
            tempResult=self.ocrWindow["ocrResult"].get()
            tempResult+=ocrResult
            tempResult+="\n"
            self.ocrWindow["ocrResult"].update(tempResult)
        #显示图像,按任意键关闭
        try:
            currentImg=cv2.imread(self.imagePathList[-1])                    
            cv2.imshow("showCurrentImg",currentImg)
        except Exception as e:
            print("图像显示流程出错，",e)
        cv2.waitKey(1000)
        cv2.destroyWindow("showCurrentImg")

        return 1
    
    #导入图像并识别函数
    def inputAndRead(self):
        imgPath=sg.popup_get_file("选取待读取图片",keep_on_top=True)
        if imgPath==None:
            print("读取失败")
            return 0
        #print(imgPath)
        try:
            currentImg=cv2.imread(imgPath)
            currentImgPath=self.createNewImgPath()
            cv2.imwrite(currentImgPath, currentImg)
        except Exception as e:
            print("载入图片流程失败:",e)
            return 0

        #调用easyocr，识别图片    
        ocrResult=self.ocrFromImage(currentImgPath)
        #如识别失败，返回None
        if ocrResult==None:    
            return 0
            
        #如识别成功，在窗口中换行并显式
        else:
            tempResult=self.ocrWindow["ocrResult"].get()
            tempResult+="/n"
            tempResult+=ocrResult
            self.ocrWindow["ocrResult"].update(tempResult)
        #显示图像,按任意键关闭
        try:
            currentImg=cv2.imread(self.imagePathList[-1])                    
            cv2.imshow("showCurrentImg",currentImg)
        except Exception as e:
            print("图像显示流程出错，",e)
        cv2.waitKey(0)
        cv2.destroyWindow("showCurrentImg")
        return 1

    #初始化一个窗口布局
    def layoutInit(self):
        self.layout=[[sg.Button("截取图片",key="grubImg",font='Times 15'),
                      sg.Button("导入图片",key="inputImg",font='Times 15'),
                      sg.Button("清空窗口",key="clearResult",font='Times 15'),
                      sg.Button("显示原图",key="showCurrentImg",font='Times 15'),],
                     [sg.Text('识别结果',font='Times 15',size=(10,1)),],
                     [sg.Multiline(size=(10,20),font='Times 16', expand_x=True, expand_y=True,key="ocrResult",enable_events=True),],
                     ]
        windowSize=self.getScreenSize()
        self.ocrWindowSize=(400,windowSize[1]-100)
        self.ocrWindowLocation=(windowSize[0]-self.ocrWindowSize[0]-50,0)        

    def windowInit(self):
        self.layoutInit()
        self.ocrWindow=sg.Window("图片文字识别工具",
                                self.layout,
                                resizable=True, 
                                grab_anywhere=True,
                                keep_on_top=True,
                                finalize=True, 
                                location=(self.ocrWindowLocation),
                                margins=(0,0), 
                                )
        
        self.ocrWindow.set_min_size(self.ocrWindowSize)
        while True:
            event,values=self.ocrWindow.read(timeout=1000)       
            if not event in (None,"__TIMEOUT__"):    
                print("当前时间为：{}，子窗口1激活事件{}".format(self.currentTime(),event))
            if event in (sg.WIN_CLOSED,'关闭'):
                self.ocrWindow.close()
                break
        
            if event in ("grubImg"):
                self.grabAndRead()
                
            if event in ("inputImg"):
                self.inputAndRead()
        
            if event in ("clearResult"):
                self.ocrWindow["ocrResult"].update("")
            if event in ("showCurrentImg"):
                if len(self.imagePathList)==0:
                    sg.popup_auto_close("尚无识别图片",keep_on_top=True,auto_close_duration=1)
                    continue
                try:
                    currentImg=cv2.imread(self.imagePathList[-1])                    
                    cv2.imshow("showCurrentImg",currentImg)
                except Exception as e:
                    print("图像显示流程出错，",e)
        
if __name__ == '__main__':
    OCRWindow=ScreenGrabAndOCRWindow()
    OCRWindow.windowInit()
    
    
    
    
    
    
    
    
    
    