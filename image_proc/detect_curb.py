import cv2
import numpy as np
im = cv2.imread('curb1.jpg')
img_raw = im.copy()
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 50, 255, cv2.THRESH_BINARY_INV)
#cv2.imshow('Binary', thresh)
#cv2.waitKey()
kernel = np.ones((5,5), np.uint8)
dilation = cv2.dilate(thresh, kernel, iterations=5)
#cv2.imshow('Dilation', dilation)
#cv2.waitKey()
minLength = 300
conts_fin = []
ret, thresh = cv2.threshold(dilation, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for i in range(len(contours)):
    x, y, w, h = cv2.boundingRect(contours[i])
    if w > minLength or h > minLength:
        conts_fin.append(contours[i])

cv2.drawContours(img_raw, conts_fin, -1, (0, 255, 0), 3)
#cv2.imshow('Contours', img_raw)
#cv2.waitKey()
x = len(img_raw[0])/2
y=len(img_raw)
cv2.line(img_raw, (x, 0), (x, y), (0, 0, 255), 3)
for cnt in contours:
    cv2.fillPoly(img_raw, cnt, (0, 255, 0))
cv2.imwrite('curb1_out.jpg', img_raw)
