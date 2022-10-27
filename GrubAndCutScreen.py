# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 13:58:53 2022

@author: MengFt
"""
#定义一个类对象，用于抓取一块屏幕
from PIL import ImageGrab ,Image
import cv2
import os
import time
class GrubAndCutScreen(object):
    def __init__(self,imagePath=None,):
        #初始化图片存储位置,如果未定义或格式非法，则直接命名为".\screenCut.png"
        if  not imagePath == None: 
            if imagePath.endswith("png"):                
                self.imagePath=imagePath  
            else:       
                self.imagePath=".\screenCut.png"
        else:
            self.imagePath=".\screenCut.png"
        print("self.imagePath=",self.imagePath)
    #一个子函数，用于抓取整块显示屏内容     
    def grabScreen(self,savePath=".\screen.png"):
        image = ImageGrab.grab()
        image.save(savePath) 
        return savePath
    
    #鼠标反馈子函数，不会直接调用，而是作为cv2.setMouseCallback()的回调函数
    def onMouse(self,event, x, y,flags,param):
        #左键点击
        global point1,point2
        tempImg=self.currentImg.copy()
        if event == cv2.EVENT_LBUTTONDOWN:        
            point1 = (x, y)
            cv2.circle(tempImg, point1, 10, (0,255,0), 5)
            cv2.imshow('image', tempImg)
        elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):               #按住左键拖曳
            cv2.rectangle(tempImg, point1, (x, y), (255,0,0), 5)         
            cv2.imshow('image', tempImg)
        elif event == cv2.EVENT_LBUTTONUP:         #左键释放
            point2 = (x, y)
            cv2.rectangle(tempImg, point1, point2, (0,0,255), 5)
            cv2.imshow('image', tempImg)
            min_x = min(point1[0], point2[0])
            min_y = min(point1[1], point2[1])
            width = abs(point1[0] - point2[0])
            height = abs(point1[1] -point2[1])
            cut_img = self.currentImg[min_y:min_y+height, min_x:min_x+width]
            cv2.imwrite(self.imagePath, cut_img)
    #截图的流程
    def imageCutWithMouse(self):
        self.currentImgPath=self.grabScreen()
        self.currentImg=cv2.imread(self.currentImgPath)
        cv2.namedWindow('image')
        #cv2.moveWindow('image',-1,-1)
        cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN,
                         cv2.WINDOW_FULLSCREEN)
        cv2.setMouseCallback('image', self.onMouse)
        cv2.imshow('image', self.currentImg)     
        cv2.waitKey(0)
        print("self.currentImgPath=",self.currentImgPath)
        try:
            os.remove(self.currentImgPath)
        except Exception as e:
            print(e)
        cv2.destroyAllWindows()
        return self.imagePath
        
if __name__ == '__main__':
    imgPath=r"screenCut1501.png"
    time.sleep(1)
    cutScreen=GrubAndCutScreen(imgPath)
    imagePath=cutScreen.grabScreen()
    img=Image.open(imagePath)
    a=img.height
    b=img.width
    print(a,b)
    cutScreen.imageCutWithMouse()
    
    
            
            
            