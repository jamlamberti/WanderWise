import cv2
import numpy as np
def arrComp(a, b, delta=10):
    for i in range(min(len(a),len(b))):
        if abs(a[i] - b[i]) > delta:
            return False
        return True

def process(im, iters=5, smoothLines=True, l_old=None, r_old=None):
    img_raw = im.copy()
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 50, 255, cv2.THRESH_BINARY_INV)
    #cv2.imshow('Binary', thresh)
    #cv2.waitKey()
    kernel = np.ones((5,5), np.uint8)
    dilation = cv2.dilate(thresh, kernel, iterations=iters)
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
    points = []
    for cnt in conts_fin:
        for pnt in cnt:
            points.append(pnt[0])
    x = len(img_raw[0])/2
    y=len(img_raw)
    cv2.line(img_raw, (x, 0), (x, y), (0, 0, 255), 3)
    for cnt in contours:
        cv2.fillPoly(img_raw, cnt, (0, 255, 0))
    w = len(img_raw[0])
    h = len(img_raw)
    boxHeight=150
    x=w/2
    deltax = 0
    rightEdge = w
    leftEdge = 0
    for pnt in points:
        if pnt[1] > h-boxHeight and pnt[1] < h-50:
            if pnt[0] < x and pnt[0] > leftEdge:
                leftEdge = pnt[0]
            elif pnt[0] > x and pnt[0] < rightEdge:
                rightEdge = pnt[0]
    if l_old is None:
        cv2.line(img_raw, (leftEdge, 0), (leftEdge, h), (255, 0, 0), thickness=3)
    else:
        cv2.line(img_raw, (l_old, 0), (l_old, h), (255, 0, 0), thickness=3)
    if r_old is None:
        cv2.line(img_raw, (rightEdge, 0), (rightEdge, h), (255, 0, 0), thickness=3)
    else:
        cv2.line(img_raw, (r_old, 0), (r_old, h), (255, 0, 0), thickness=3)
    center = (w/2, h/2)
    M = cv2.getRotationMatrix2D(center, 180, 1.0)
    rotated = cv2.warpAffine(img_raw, M, (w, h))
    if smoothLines:
        return rotated, leftEdge, rightEdge
    return rotated
def test():
    im = cv2.imread('curb1.jpg')
    curb = process(im, smoothLines=False)
    cv2.imwrite('curb1_result.jpg', curb)
    android = ['curb2', 'curb3', 'curb4', 'curb5', 'curb6', 'curb7', 'curb8', 'curb9', 'curb10', 'curb11', 'curb12', 'curb14', 'curb15']
    for i in android:
        im = cv2.imread(i+'.jpg')
        try:
            curb = process(im, smoothLines=False)
            cv2.imwrite(i+'_result.jpg', curb)
        except:
            import traceback
            traceback.print_exc()
if __name__ == '__main__':
    test()
