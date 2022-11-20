# 202110060 ohseohyun

import numpy as np
import cv2

height , width = 1000, 1500


def getline(x0,y0,x1,y1):
    points = []
    if abs(x1-x0)>=abs(y1-y0):
        n = abs(x1-x0)
    else:
        n = abs(y1-y0)
    dx = (x1-x0)/n
    dy = (y1-y0)/n
    x,y = x0,y0
    for k in range(n):
        points.append((int(x),int(y),1))
        x = x+dx
        y = y+dy
    return points

def drawLine(canvas, x0, y0, x1, y1, color=(255, 255, 255)):
    xys = getline(x0, y0, x1, y1)
    for xy in xys:
        x, y, a= xy
        canvas[y, x, :] = color
    return


def deg2rad(deg):
    rad = deg * np.pi / 180.
    return rad 

def drawPolygon(canvas, pts, color, axis=False):
    n = pts.shape[0]
    # print(type(shape))
    for k in range(n):
        drawLine(canvas, pts[int(k%n),0], pts[int(k%n),1], 
                        pts[int((k+1)%n),0], pts[int((k+1)%n),1], color)
    
    if axis == True: # center - pts[0]
        center = np.array([0., 0,0])
        for p in pts:
            center += p 
        center = center / pts.shape[0]
        center = center.astype('int') 
        # print(center)
        drawLine(canvas, center[0],center[1], pts[0][0],pts[0][1], color=(255, 128, 128))
    #
    return 

def makeTmat(a,b):
    T = np.eye(3,3)
    T[0,2] = a
    T[1,2] = b
    # print(T)
    return T

def makeRmat(deg):
    rad = deg2rad(deg)
    c = np.cos(rad)
    s = np.sin(rad)
    R =  np.eye(3,3)
    R[0,0] = c
    R[0,1] = -s
    R[1,0] = s
    R[1,1] = c
    # print(R)
    return R

def getrectangle(len):
    points = []
    points.append((0,0,1))
    points.append((3*len,0,1))
    points.append((3*len,len,1))
    points.append((0,len,1))

    points = np.array(points)
    # print(points)
    return points

def gettriangle(wid,hgt):
    points = []
    points.append((hgt,0,1))
    points.append((0,-wid/2,1))
    points.append((0,wid/2,1))

    points = np.array(points)
    return points

def drawColored(canvas,points,color):
    n = points.shape[0]
    pts = []

    for k in range(n):
        a = getline(points[int(k%n),0], points[int(k%n),1],points[int((k+1)%n),0], points[int((k+1)%n),1])
        pts.extend(a)
    pts = np.array(pts)
    xs = pts[:,0]
    ys = pts[:,1]
    xmin = min(xs)
    xmax = max(xs)
    ymin = min(ys)
    ymax = max(ys)

    if xmax-xmin > ymax-ymin: # y 기준으로 하기
        for y in range(ymin,ymax+1,1):
            some_xs = []
            for p in pts:
                if p[1]==y:
                    some_xs.append(p[0])
            some_xmin = min(some_xs)
            some_xmax = max(some_xs)
            for x in range(some_xmin,some_xmax+1,1):
                canvas[y,x,:] = color

    else: # x 기준으로 하기
        for x in range(xmin,xmax+1,1):
            some_ys = []
            for p in pts:
                if p[0]==x:
                    some_ys.append(p[1])
            some_ymin = min(some_ys)
            some_ymax = max(some_ys)
            for y in range(some_ymin,some_ymax+1,1):
                canvas[y,x,:] = color
    return

def main():
    canvas = np.zeros( (height, width, 3), dtype='uint8') 
    vhr = 0
    theta = -90

    a,b = width/2,height/2
    w,h = 200, 100

    while True:
    # get ngon points
        rect = getrectangle(h)
        tri1 = gettriangle(100,200)
        tri2 = gettriangle(100,200)
        tri3 = gettriangle(100,200)
        tri4 = gettriangle(100,200)
        tri5 = gettriangle(100,200)
        
    # rotating, translating points
        H1 = makeTmat(a,b) @ makeRmat(90) @ makeTmat(0,-h/2)

    # drawing rect1
        rect = H1 @ rect.T
        rect = rect.T
        rect = rect.astype('int')
        # drawPolygon(canvas,rect,(0,0,255),axis = False)
        drawColored(canvas,rect,(0,255,247))
        
        tri1 = makeTmat(a,b) @ makeRmat(theta) @ makeTmat(-200,0) @ tri1.T
        tri1 = tri1.T
        tri1 = tri1.astype('int')
        # drawPolygon(canvas,tri1,(255,255,0),axis= False)
        drawColored(canvas,tri1,(235,149,37))
        
        tri2 = makeTmat(a,b) @ makeRmat(theta+72) @ makeTmat(-200,0) @ tri2.T
        tri2 = tri2.T
        tri2 = tri2.astype('int')
        # drawPolygon(canvas,tri2,(255,255,50),axis= False)
        drawColored(canvas,tri2,(235,149,37))
        
        
        tri3 = makeTmat(a,b) @ makeRmat(theta+(72*2)) @ makeTmat(-200,0) @ tri3.T
        tri3 = tri3.T
        tri3 = tri3.astype('int')
        # drawPolygon(canvas,tri3,(255,255,100),axis= False)
        drawColored(canvas,tri3,(235,149,37))
        
        
        tri4 = makeTmat(a,b) @ makeRmat(theta+(72*3)) @ makeTmat(-200,0) @ tri4.T
        tri4 = tri4.T
        tri4 = tri4.astype('int')
        # drawPolygon(canvas,tri4,(0,255,150),axis= False)
        drawColored(canvas,tri4,(235,149,37))

        tri5 = makeTmat(a,b) @ makeRmat(theta+(72*4)) @ makeTmat(-200,0) @ tri5.T
        tri5 = tri5.T
        tri5 = tri5.astype('int')
        # drawPolygon(canvas,tri4,(0,255,150),axis= False)
        drawColored(canvas,tri5,(235,149,37))
        

        theta +=15
        cv2.imshow("window", canvas)
        canvas[:, :, :] = 0
        if cv2.waitKey(20) == 27: break
#     
if __name__ == "__main__": # __ 
    main()
