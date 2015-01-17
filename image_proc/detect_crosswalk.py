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
#class Polygon(object):
#    def __init__(self, points):
        
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
im = cv2.imread('crosswalk.jpg')
img_raw = im.copy()
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127,255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
im_gray = imgray.copy()
im_gray2 = imgray.copy()
im_gray3 = imgray.copy()
im_gray4 = imgray.copy()
im_gray5 = imgray.copy()
im_gray6 = imgray.copy()
cv2.drawContours(imgray, contours, -1, (0, 255, 0), 3)
cv2.imshow('gray', imgray)
cv2.waitKey()
edges = cv2.Canny(im_gray, 50, 150, apertureSize = 3)
lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
for rho, theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0+1000*(-b))
    y1 = int(y0+1000*(a))
    x2 = int(x0-1000*(-b))
    y2 = int(y0-1000*(a))
    cv2.line(im_gray, (x1, y1), (x2, y2), (0, 0, 255), 2)
cv2.imshow('Hough', im_gray)
cv2.waitKey()

minLineLength = 50
maxLineGap = 5
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength, maxLineGap)
for x1, y1, x2, y2 in lines[0]:
    cv2.line(im_gray2, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imshow('HoughP', im_gray2)
cv2.waitKey()
ret, thresh1 = cv2.threshold(im_gray3, 175, 255, cv2.THRESH_BINARY)
cv2.imshow('Binary', thresh1)
cv2.waitKey()

ret, thresh = cv2.threshold(thresh1, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(im_gray3, contours, -1, (0, 255, 0), 3)

cv2.imshow('Contours', im_gray3)
cv2.waitKey()
edges = cv2.Canny(thresh1, 50, 150, apertureSize=3)
minLineLength = 2
maxLineGap = 1
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength, maxLineGap)
for x1, y1, x2, y2 in lines[0]:
    cv2.line(im_gray4, (x1, y1), (x2, y2), (0, 255, 0), 2)
cv2.imshow('HoughP', im_gray4)
cv2.waitKey()
lines = []
#for cnt in contours:
    # box smoother
#    lines.append(StraightLine(cnt[0][0][0], cnt[0][0][1], cnt[0][-1][0], cnt[0][-1][1]))
#boxes = findBoxes(lines)

# extract lines


kernel = np.ones((5,5), np.uint8)
dilation = cv2.dilate(thresh1, kernel, iterations=1)
cv2.imshow('Dilation', dilation)
cv2.waitKey()
ret, thresh = cv2.threshold(dilation, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#for i in range(len(contours)):
#    temp = im_gray6.copy()
#    cv2.drawContours(temp, contours, i, (0, 255, 0), 3)
#    cv2.imshow('cnt', temp)
#    cv2.waitKey()
minLength = 500
conts_fin = []
lines = []
left_points = [(0, 150), (100, 0)]
right_points = [(150, 150), (100, 0)]
xs = []
ys = []
x1s = []
for i in range(len(contours)):
    #print cv2.boundingRect(contours[0])    
    x, y, w, h = cv2.boundingRect(contours[i])
    #print x, y, w, h
    if w > minLength or h > minLength:
        min_x, _ = left_points[0]
        if min_x > x:
            left_points[0] = (x, y)
        max_x, _ = right_points[0]
        if max_x < x+w:
            right_points[0] = (x+w, y)
        max_left, _ = left_points[1]
        if max_left < x:
            left_points[1] = (max_left, y+h)
        min_right, _ = right_points[1]
        if min_right > x+w:
            right_points[1] = (x+w, y+h)
        conts_fin.append(contours[i])
        lines.append([
            StraightLine(x, y, x+w, y),
            StraightLine(x, y+h, x+w, y+h),
            StraightLine(x, y, x, y+h),
            StraightLine(x+w, y, x+w, y+h)
        ])
        xs.append(x)
        ys.append(y)
        x1s.append(x+w)
        #for l in lines[-1]:
        #cv2.line(img_raw, (x, y), (x, y+h), (255, 0, 0), 3)
        #cv2.line(img_raw, (x+w, y), (x+w, y+h), (255, 0, 0), 3)
        #print (x, y), (x+w, y+h)
#cv2.line(img_raw, left_points[0], left_points[1], (255, 0, 0), 3)
#cv2.line(img_raw, right_points[0], right_points[1], (255, 0, 0), 3)
#cv2.line(img_raw, (149, 1233), (719, 555), (0, 255, 0), 3)
cv2.line(img_raw, (min(xs), ys[xs.index(min(xs))]), (max(xs), ys[xs.index(max(xs))]), (0, 255, 0), 3)
cv2.line(img_raw, (max(x1s), ys[x1s.index(max(x1s))]), (min(x1s), ys[x1s.index(min(x1s))]), (0, 255, 0), 3)
cv2.line(img_raw, (avg([min(xs), max(x1s)]), avg([ys[xs.index(min(xs))], ys[x1s.index(max(x1s))]])), (avg([max(xs), min(x1s)]), avg([ys[xs.index(max(xs))], ys[x1s.index(min(x1s))]])), (0, 0, 255), 3)
cv2.drawContours(im_gray6, conts_fin, -1, (0, 255, 0), 3)
cv2.imshow('cmt', im_gray6)
cv2.waitKey()

# Determine best two lines

line0_0 = [i[0].slope for i in lines]
line1_0 = [i[1].slope for i in lines]
line2_0 = [i[2].slope for i in lines]
line3_0 = [i[2].slope for i in lines]
#print line0_0
#print line1_0
#print line2_0
#print line3_0
#print np.std(line0_0)
#print np.std(line1_0)
#print np.std(line2_0)
#print np.std(line3_0)
line0_1 = [i[0].intercept for i in lines]
line1_1 = [i[1].intercept for i in lines]
line2_1 = [i[2].intercept for i in lines]
line3_1 = [i[3].intercept for i in lines]
#print line0_1
#print line1_1
#print line2_1
#print line3_1

#print np.std(line0_1)
#print np.std(line1_1)
#print np.std(line2_1)
#print np.std(line3_1)

line_choices = [[np.std(line0_0), np.std(line0_1)],
                [np.std(line1_0), np.std(line1_1)],                
                [np.std(line2_0), np.std(line2_1)],
                [np.std(line3_0), np.std(line3_1)]
]
avgs = [avg(i) for i in line_choices]
line1 = avgs.index(min(avgs))
del avgs[line1]
del line_choices[line1]
line2 = avgs.index(min(avgs))
if line1 <= line2:
    line2+=1
#if line1 == 0 or line2 == 0:
#    print (avg(line0_0), avg(line0_1))
#    print (avg(line0_0)*1000, avg(line0_1)+avg(line0_0)*1000)
#    cv2.line(img_raw, (avg(line0_0), avg(line0_1)), (avg(line0_0)*1000, avg(line0_1)+avg(line0_0)*1000), (0, 255, 0), 3)
#if line1 == 1 or line2 == 1:
#    print (avg(line0_0), avg(line0_1))
#    print (avg(line0_0)*1000, avg(line0_1)+avg(line0_0)*1000)
#    cv2.line(img_raw, (avg(line1_0)*-10, avg(line1_1)), (avg(line1_0)*1000, avg(line1_1)+avg(line1_0)*1000), (0, 255, 0), 3)    
#if line1 == 2 or line2 == 2:
#    print (avg(line0_0), avg(line0_1))
#    print (avg(line0_0)*1000, avg(line0_1)+avg(line0_0)*1000)
#    cv2.line(img_raw, (avg(line2_0)*-10, avg(line2_1)), (avg(line2_0)*1000, avg(line2_1)+avg(line2_0)*1000), (0, 255, 0), 3)
#if line1 == 3 or line2 == 3:
#    print (avg(line0_0), avg(line0_1))
#    print (avg(line0_0)*1000, avg(line0_1)+avg(line0_0)*1000)
#    cv2.line(img_raw, (avg(line3_0)*-10, avg(line3_1)), (avg(line3_0)*1000, avg(line3_1)+avg(line3_0)*1000), (0, 255, 0), 3)
#cv2.line(img_raw, (100, 0), (100, 100), (0, 255, 0), 3)
cv2.imshow('Crosswalk', img_raw)

cv2.waitKey()
