# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 16:42:19 2022

@author: MengFt
"""

import easyocr
import cv2


reader = easyocr.Reader(['ch_sim','en'], gpu = False) # need to run only once to load model into memory
filePath="C:\\Users\\MengFt\\Desktop\\pictureOfPaper\\"
filePathList=[]
for i in range(1,19):
    tempFilePath=filePath+str(i)+".jpg"
    filePathList.append(tempFilePath)
#%%
#filePath=r"C:\Users\MengFt\Desktop\pictureOfPaper\2.jpg"
#img1=cv2.imread(filePath)
#cv2.imshow("first image",img1)
#cv2.waitKey(1000)
def ocrFromImage(inputImage):
    
    try:
        result = reader.readtext(inputImage, paragraph="False")
        resultSring="#"
        for i in result:
            resultSring+=i[1]
            resultSring+=" "
        #print(resultSring)
        resultSring+="#"
        return resultSring
    except Exception as e:
        tempEString="#"+str(e)+"#"
        print(tempEString)
        return tempEString
wordString=""
for img in filePathList:
    wordString+=ocrFromImage(img)
    wordString+="\n"
print(wordString)
#cv2.destroyAllWindows()


