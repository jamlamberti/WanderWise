import cv2
import numpy as np
SLOPE_MAX = 10000000000.0
class StraightLine(object):
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        try:
            self.slope = 1.0*(y2-y1)/(x2-x1)
        except:
            self.slope = SLOPE_MAX
        self.intercept = y1 - self.slope*x1
        #self.length = sqrt((x1-x2)**2 + (y1-y2)**2)
class MBLine(object):
    def __init__(self, m, b):
        self.slope = m
        self.intercept = b
    def get_min_x(self):
        if self.slope != SLOPE_MAX:
            return -10
        else:
            return intercept
class Box(object):
    def __init__(self, p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        
def inRange(a, b, delta):
    if abs(a-b) < delta:
        return True
    return False
def avg(l):
    return int(sum(l)/(1.0*len(l)))
def findBoxes(lines, tol=5):
    ag_matrix = [[0 for i in range(len(lines))] for i in range(len(lines))]
    #print len(ag_matrix)
    #print len(ag_matrix[0])
    counter = 0
    for i in range(len(lines)):
        for j in range(len(lines)):
            if i == j:
                pass
            elif i >j:
                pass
            elif inRange(lines[i].x1, lines[j].x1, tol) and inRange(lines[i].y1, lines[j].y1, tol):
                ag_matrix[i][j] = 1
            elif inRange(lines[i].x1, lines[j].x2, tol) and inRange(lines[i].y1, lines[j].y2, tol):
                ag_matrix[i][j] = 1
            elif inRange(lines[i].x2, lines[j].x1, tol) and inRange(lines[i].y2, lines[j].y1, tol):
                ag_matrix[i][j] = 1
            elif inRange(lines[i].x2, lines[j].x2, tol) and inRange(lines[i].y2, lines[j].y2, tol):
                ag_matrix[i][j] = 1
            if ag_matrix[i][j] == 1:
                counter+=1
    polys = {}
    for i in range(len(ag_matrix)):
        polys[i] = []
        for j in range(len(ag_matrix[0])):
            if ag_matrix[i][j] == 1:
                polys[i].append(j)
    conts = []
    #print polys
    for i in range(len(ag_matrix)):
        conts.append([i])
        needToParse = [j for j in polys[i]]
        while len(needToParse) != 0:
            if needToParse[0] not in polys:
                conts.append(needToParse[0])
                for k in polys[needToParse[0]]:
                    needToParse.append(k)
            #polys[needToParse[0]] = []
            del needToParse[0]
    #for i in conts:
        #print i
    return None
def process(im, minLength=500):
    img_raw = im.copy()
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127,255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    im_gray = imgray.copy()
    ret, thresh1 = cv2.threshold(im_gray, 210, 255, cv2.THRESH_BINARY)
    #cv2.imshow('Binary', thresh1)
    #cv2.waitKey()
    kernel = np.ones((5,5), np.uint8)
    dilation = cv2.dilate(thresh1, kernel, iterations=1)
    #cv2.imshow('Dilation', dilation)
    #cv2.waitKey()
    ret, thresh = cv2.threshold(dilation, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    conts_fin = []
    lines = []
    xs = []
    ys = []
    x1s = []
    status = 0
    if len(contours) < 3:
        status = 1
    elif len(contours) > 20:
        status = -5
    elif len(contours) > 6:
        status = -2
    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        if w > minLength or h > minLength:
            conts_fin.append(contours[i])
            lines.append([
                StraightLine(x, y, x+w, y),
                StraightLine(x, y+h, x+w, y+h),
                StraightLine(x, y, x, y+h),
                StraightLine(x+w, y, x+w, y+h)
            ])
            for i in lines[-1]:
                cv2.line(img_raw, (i.x1, i.y1), (i.x2, i.y2), (255, 0, 0), 3)
            xs.append(x)
            ys.append(y)
            x1s.append(x+w)
    cv2.line(img_raw, (min(xs), ys[xs.index(min(xs))]), (max(xs), ys[xs.index(max(xs))]), (0, 255, 0), 3)
    cv2.line(img_raw, (max(x1s), ys[x1s.index(max(x1s))]), (min(x1s), ys[x1s.index(min(x1s))]), (0, 255, 0), 3)
    cv2.line(img_raw, (avg([min(xs), max(x1s)]), avg([ys[xs.index(min(xs))], ys[x1s.index(max(x1s))]])), (avg([max(xs), min(x1s)]), avg([ys[xs.index(max(xs))], ys[x1s.index(min(x1s))]])), (0, 0, 255), 3)
    return img_raw, status

def test():
    im = cv2.imread('crosswalk.jpg')
    crosswalk, _ = process(im)
    cv2.imwrite('crosswalk_result.jpg', crosswalk)
    im = cv2.imread('crosswalk2.jpg')
    crosswalk, _ = process(im, 50)
    cv2.imwrite('crosswalk_result2.jpg', crosswalk)
    android = ['crosswalk1', 'crosswalk3']
    j = 50
    while j <= 1500:
        for i in android:
            im = cv2.imread(i+'.jpg')
            try:
                crosswalk, _ = process(im, j)
                cv2.imwrite(i + '_result_%d.jpg'%j, crosswalk)
            except:
                pass
        j+= 50
if __name__ == '__main__':
    test()
