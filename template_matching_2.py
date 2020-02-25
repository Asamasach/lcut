# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 09:31:48 2020

@author: Mahdi_Sadat
"""

from picamera.array import PiRGBArray
from picamera import PiCamera
from matplotlib import pyplot as plt


import capture_label #another file beside this file
import time
import cv2
import numpy as np

import scipy

from gpiozero import LED
led = LED(16)

font = cv2.FONT_HERSHEY_SIMPLEX 
  
# org 
org = (50, 50) 
  
# fontScale 
fontScale = 1
   
# Blue color in BGR 
color = (255, 0, 0) 
  
# Line thickness of 2 px 
thickness = 2

# initialize the camera and grab a reference to the raw camera capture

camera = PiCamera()
camera.resolution = (256, 176)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(256, 176))



template = cv2.imread('/home/pi/capture.jpg')
template = template[60:120, 88:168]



#show template!!!!
#plt.ion()
#fig = plt.figure()
#plt.imshow(template, cmap = 'gray')
#plt.show(block=False)
#cv2.imwrite('show_template.jpg',template)
#cv2.imshow("cut_area",show_template.jpg)
cv2.line(template,(40,10),(40,49),(5,255,100),1)

cv2.imshow("cut_area",template)
cv2.moveWindow("cut_area", 0,0)
template = cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)

#time.sleep(5)
#cv2.destroyAllWindows()
#plt.close(fig)



# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr",
                                       use_video_port=True):
    # grab the raw NumPy array representing the image,
    # then initialize t
    
    # and occupied/unoccupied text
    image = frame.array

    # we do something here
    # we get the image or something then run some matching
    # if we get a match, we draw a square on it or something

    

    img_rgb = image

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)


    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    #print(str(res))
    threshold = 0.7
    
    loc = np.where( res >= threshold)
    for pt_1 in zip(*loc[::-1]):
    #
    #show frames
        
        cv2.rectangle(img_rgb, pt_1, (pt_1[0] + w, pt_1[1] + h), (0,0,255), 2)
    #'''   
        if ( pt_1[0] < 90 and pt_1[0] > 75):
            led.on()
        else:
            led.off()
    
    #for pt_1 in zip(*loc[::-1]):
     #   cv2.rectangle(image, (pt_1[1], pt_1[0]), (pt_1[1] + w, pt_1[0] + h),(127,127,255), 2)

    # show the frame


#show frames
        img_rgb = cv2.putText(img_rgb, "pos:"+str(pt_1[0]), org, font,  fontScale, color, thickness, cv2.LINE_AA)
        cv2.line(img_rgb,(127,40),(127,140),(0,255,255),1)
    led.off()
    cv2.imshow("Frame", img_rgb)

    #    GPIO.cleanup()
    #time.sleep(0.1)
    
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        led.off()
        break
    elif key == ord("c"):
        led.off()
        import os
        camera.close()
        capture_label.capture()
        cv2.destroyAllWindows()
        os.system("python3 /home/pi/template_matching_2.py")
        quit()
        break
