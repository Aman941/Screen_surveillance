import cv2
import numpy as np
import matplotlib.pyplot as plt
import pyautogui
import msvcrt
import time
import os

file = 0
prev_centre = [[12,45],[78,56]]
const_address = os.getcwd()
hue_low = int(input("lower value of hue"))
hue_hi  = int(input("higher value of hue"))
th_area = int(input("threshold area"))
path = str((input("address of surveillance folder")))

def comp(lst1, lst2):
    temp = []
    temp = intersection(lst1, lst2)
    temp = reqval(lst1, temp)
    return temp

def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 
def reqval(lst1, lst2):
    lst3 = [value for value in lst1 if value not in lst2] 
    return lst3

def imgAnalysis(image):
    global file
    global prev_centre
    y = 343
    h = 429
    x = 480
    w = 900
    # current centroid points
    curr_centre = []
    
    crop_img = image[y:y+h, x:x+w]
    crop_img = image
    #for colour detection

    hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV) 
    lower_red = np.array([hue_low,50,50]) 
    upper_red = np.array([hue_hi,255,255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(crop_img,crop_img, mask= mask)

    # getting countours

    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    length = len(contours)
    flag = 0
    for i in range(0,length,1):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        ## just collect the points first
        if(area > th_area):
            M = cv2.moments(cnt)
            cx= int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            curr_centre.append([cx,cy])
            #print ('alert')
            #print (cx , cy)
            #cv2.circle(crop_img,(cx,cy),40,(0,0,255))
            #flag = 1
    new_centre = []
    new_centre = comp(curr_centre,prev_centre)
    if(len(prev_centre) == 0):
        new_centre = curr_centre
    length = len(new_centre)
    print(length)
    if(len(new_centre)):
        # save image
        # print(os.getcwd())
        for i in range(0,length,1):
            x = new_centre[i][0]
            y = new_centre[i][1]
            cv2.circle(crop_img,(x,y),40,(0,0,255))
        #path = "C:\shree project\surveillance2"
        os.chdir( path )
        file = file+1
        cv2.imwrite(str(file)+".jpg",crop_img)
        prev_centre = curr_centre
        return True
        
    else:
        return False
        
##image = cv2.imread("dwt.jpg")
##imgAnalysis(image,file)
##i = 0
##while i<5:
##    image = pyautogui.screenshot()
##    image = cv2.cvtColor(np.array(image) , cv2.COLOR_RGB2BGR)
##    imgAnalysis(image,file)
##    if msvcrt.kbhit():
##        if ord(msvcrt.grtch()) == 27:
##            break
##    time.sleep(2)
##    i = i + 1

try:
    while True:
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image) , cv2.COLOR_RGB2BGR)
        imgAnalysis(image)
        time.sleep(10)
except KeyboardInterrupt:
    print('interrupted!')
    
