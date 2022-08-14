import os
from tkinter import Y
import cv2
import numpy as np
import time
import os
import GestureRecognitionModule as grm

#Putting Header images in a list
folderPath ="yomari-codecamp\Header"
myList = os.listdir(folderPath)
# print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
# print(len(overlayList))


header = overlayList[0] # default header
drawColor=(255,0,255) # default color
brushThickness = 5
xpw,ypw = 0,0
xpe,ype=0,0
eraserthickness = 100

cap = cv2.VideoCapture(0)
#Setting Height and Width of the video
cap.set(3,1280)
cap.set(4,720)

imgCanvas = np.zeros((720,1280,3),np.uint8)


while True:
    sucess,img = cap.read()

    #Find Hand Landmarks and draw handlandmarks and return mode i.e. write,erase,eraseall,idle
    # img= cv2.flip(img,1)
    mode,img,lmList = grm.class_return(img)
    img= cv2.flip(img,1)
    

    


    if len(lmList)!=0:
        # print(lmList)

        # tip of index finger and middle finger
        x1,y1= lmList[8][1:] # current position of index finger tip
        x1=1280-x1
        # print(x1,y1)
        # print(mode)

        num12y = lmList[12][2]
        num10y = lmList[10][2]

        if mode=="erase" or mode=="nothing": #or not (num12y>num10y):
            if y1<125:
                if 460<x1<720:
                    header = overlayList[0]
                    drawColor=(255,0,255)

                elif 830<x1<1030:
                    header = overlayList[1]
                    drawColor=(255,0,0)

                elif 1090<x1<1280:
                    header = overlayList[2]
                    drawColor=(0,255,0)

            xpe,ype = 0,0
            xpw,ypw=0,0

        if mode =="idle":
            eraserColor=(0,0,0)
            # cv2.circle(img,center=(x1,y1),radius=50,color=eraserColor,thickness=cv2.FILLED)
            if xpe== 0 and ype ==0:
                xpe,ype =x1,y1

            
            cv2.line(img,pt1=(xpe,ype),pt2=(x1,y1),color=eraserColor,thickness=eraserthickness)
            cv2.line(imgCanvas,pt1=(xpe,ype),pt2=(x1,y1),color=eraserColor,thickness=eraserthickness)
            


            xpe,ype = x1,y1
            xpw,ypw=0,0

        
        if mode=="eraseall":
            imgCanvas = np.zeros((720,1280,3),np.uint8)



        if mode == "write":
            cv2.circle(img,center=(x1,y1),radius=15,color=drawColor,thickness=cv2.FILLED)
            # print("Drawing Mode")


            if xpw== 0 and ypw ==0:
                xpw,ypw =x1,y1

            
            

            cv2.line(img,pt1=(xpw,ypw),pt2=(x1,y1),color=drawColor,thickness=brushThickness)
            cv2.line(imgCanvas,pt1=(xpw,ypw),pt2=(x1,y1),color=drawColor,thickness=brushThickness)

            xpw,ypw = x1,y1
            xpe,ype=0,0

       

        












    #Blending two images
    imgGray = cv2. cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV) #backgound is white and drawn doodle is black
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR) # needed to convert to three channel so it can be added with img
    img = cv2.bitwise_and(img,imgInv) # converts the area in the img to area drawn in canvas as black value is 0 and "AND" with 0 gives 0 i.e black 
    img = cv2.bitwise_or(img,imgCanvas)










    # Setting the header image
    # img=cv2.flip(img,1)
    # imgCanvas=cv2.flip(imgCanvas,1)
    img[0:125,0:1280]= header
    # img[595:720,0:1280]= header


    cv2.imshow("Image",img)
    # cv2.imshow("Canvas",imgCanvas)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()