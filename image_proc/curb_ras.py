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
    kernel = np.ones((5,5), np.uint8)
    dilation = cv2.dilate(thresh, kernel, iterations=iters)
    minLength = 300
    conts_fin = []
    ret, thresh = cv2.threshold(dilation, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        if w > minLength or h > minLength:
            conts_fin.append(contours[i])
    
    #cv2.drawContours(img_raw, conts_fin, -1, (0, 255, 0), 3)
    points = []
    for cnt in conts_fin:
        for pnt in cnt:
            points.append(pnt[0])
    x = len(img_raw[0])/2
    y=len(img_raw)
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
    left_final = leftEdge
    right_final = rightEdge
    if l_old is not None:
        left_final = l_old
    if r_old is not None:
        right_final = r_old
    center = (w/2, h/2)
    M = cv2.getRotationMatrix2D(center, 180, 1.0)
    rotated = cv2.warpAffine(img_raw, M, (w, h))
    status = 0
    try:
        average = (right_final + left_final)/2
        sign = (average - len(img_raw[0])/2)/abs(average - len(img_raw[0])/2)
        if len(img_raw[0])/2 < average:
            status = average - len(img_raw[0])/2
            #cv2.putText(rotated, 'Veere right', (0, h/2), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 0))
            pass
        else:
            status = len(img_raw[0])/2 - average
            #cv2.putText(rotated, 'Veere Left', (0, h/2), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 0))
            pass
    except:
        power = 0
    if smoothLines:
        return rotated, leftEdge, rightEdge, status
    return rotated, status
def test():
    im = cv2.imread('curb1.jpg')
    im = cv2.resize(im, (0,0), fx=0.5, fy=0.5)
    curb = process(im, smoothLines=False)
    cv2.imwrite('curb1_result.jpg', curb)
    android = ['curb2', 'curb3', 'curb4', 'curb5', 'curb6', 'curb7', 'curb8', 'curb9', 'curb10', 'curb11', 'curb12', 'curb14', 'curb15']
    for i in android:
        im = cv2.imread(i+'.jpg')
        im = cv2.resize(im, (0,0), fx=0.5, fy=0.5)
        try:
            curb = process(im, smoothLines=False)
            cv2.imwrite(i+'_result.jpg', curb)
        except:
            import traceback
            traceback.print_exc()
if __name__ == '__main__':
    test()
