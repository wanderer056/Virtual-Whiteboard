import os
from tkinter import Y
import cv2
import numpy as np
import time
import os
import GestureRecognitionModule as grm
import pyautogui

def mainprog():


    drawColor=(0,0,255) # default color
    brushThickness = 5
    xpw,ypw = 0,0
    xpe,ype=0,0
    eraserthickness = 100

    # cap = cv2.VideoCapture(0)
    # #Setting Height and Width of the video
    # cap.set(3,1280)
    # cap.set(4,720)

    myscr = pyautogui.screenshot()
    cap = cv2.VideoCapture(0)
    # codec = cv2.VideoWriter_fourcc(	'M', 'J', 'P', 'G'	)
    # cap.set(6, codec)
    # cap.set(5, 30)
    cap.set(3, 1920)
    cap.set(4, 1080)
    myscr_array = np.array(myscr)
    myscr_array= cv2.cvtColor(myscr_array,cv2.COLOR_RGB2BGR)
    imgCanvas = np.zeros((1080,1920,3),np.uint8)
    # pointer_img = np.zeroes((1080,1920,3),dtype=np.uint8)


    cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)



    while True:
        pointer_img = np.zeros((1080,1920,3),dtype=np.uint8)
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

                xpe,ype = 0,0
                xpw,ypw=0,0
                cv2.circle(pointer_img,center=(x1,y1),radius=15,color=drawColor,thickness=cv2.FILLED)


            if mode =="idle":
                eraserColor=(0,0,0)
                # cv2.circle(img,center=(x1,y1),radius=50,color=eraserColor,thickness=cv2.FILLED)
                if xpe== 0 and ype ==0:
                    xpe,ype =x1,y1

                
                cv2.line(img,pt1=(xpe,ype),pt2=(x1,y1),color=eraserColor,thickness=eraserthickness)
                cv2.line(imgCanvas,pt1=(xpe,ype),pt2=(x1,y1),color=eraserColor,thickness=eraserthickness)

                cv2.circle(pointer_img,center=(x1,y1),radius=15,color=drawColor,thickness=cv2.FILLED)

                


                xpe,ype = x1,y1
                xpw,ypw=0,0

            
            if mode=="eraseall":
                imgCanvas = np.zeros((1080,1920,3),np.uint8)



            if mode == "write":
                cv2.circle(img,center=(x1,y1),radius=15,color=drawColor,thickness=cv2.FILLED)
                cv2.circle(pointer_img,center=(x1,y1),radius=15,color=drawColor,thickness=cv2.FILLED)

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
        img1 = cv2.bitwise_and(myscr_array,imgInv) # converts the area in the img to area drawn in canvas as black value is 0 and "AND" with 0 gives 0 i.e black 
        img1 = cv2.bitwise_or(myscr_array,imgCanvas)


        imgGray1 = cv2. cvtColor(pointer_img, cv2.COLOR_BGR2GRAY)
        _, imgInv1 = cv2.threshold(imgGray1,50,255,cv2.THRESH_BINARY_INV) #backgound is white and drawn doodle is black
        imgInv1 = cv2.cvtColor(imgInv1,cv2.COLOR_GRAY2BGR) # needed to convert to three channel so it can be added with img
        img2 = cv2.bitwise_and(img1,imgInv1) # converts the area in the img to area drawn in canvas as black value is 0 and "AND" with 0 gives 0 i.e black 
        img2 = cv2.bitwise_or(img1,pointer_img)










        # Setting the header image
        # img=cv2.flip(img,1)
        # imgCanvas=cv2.flip(imgCanvas,1)
        # img[0:125,0:1280]= header
        # img[595:720,0:1280]= header


        # cv2.imshow("window",img)
        cv2.imshow("window",img2)
        # cv2.imshow("pointer",pointer_img)
        # cv2.imshow("Canvas",imgCanvas)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()