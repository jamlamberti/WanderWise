import cv2
from matplotlib import pyplot as plt
import crosswalk
import curb
import time
vid = cv2.VideoCapture(0)
length = 500
l_sum = [0]
r_sum = [0]
while True:
    success, img = vid.read()
    img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
    if not success:
        break
    w = len(img[0])
    h = len(img)
    center = (w/2, h/2)
    M = cv2.getRotationMatrix2D(center, 180, 1.0)
    img = cv2.warpAffine(img, M, (w, h))
    try:
        img, left, right, status = curb.process(img, l_old=sum(l_sum)/len(l_sum), r_old=sum(r_sum)/len(r_sum))
        l_sum.append(left)
        r_sum.append(right)
        if len(l_sum) >= 8:
            del l_sum[0]
        if len(r_sum) >= 8:
            del r_sum[0]
    except:
        import traceback
        traceback.print_exc()
        pass
    #cv2.imshow('My Video', img)
    #cv2.waitKey(10)
    time.sleep(1)
