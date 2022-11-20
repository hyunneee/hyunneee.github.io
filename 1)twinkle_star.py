# 20211060 ohseohyun
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
        x, y, a = xy
        canvas[y, x, :] = color
    return

def drawPolygon(canvas, pts, color, axis=False):
    n = pts.shape[0]
    for k in range(n):
        drawLine(canvas, pts[int(k%n),0], pts[int(k%n),1], 
                        pts[int((k+1)%n),0], pts[int((k+1)%n),1], color)
    
    if axis == True: # center - pts[0]
        center = np.array([0., 0, 0])
        for p in pts:
            center += p 
        center = center / pts.shape[0]
        center = center.astype('int') 
        # print(center)
        drawLine(canvas, center[0],center[1], pts[0][0],pts[0][1], color=(255, 128, 128))
    #
    return 

def getstar(canvas, pts, color,axis=False):
    drawLine(canvas, pts[0,0], pts[0,1], 
                        pts[2,0], pts[2,1], color)
    drawLine(canvas, pts[0,0], pts[0,1], 
                        pts[3,0], pts[3,1], color)
    drawLine(canvas, pts[1,0], pts[1,1], 
                        pts[3,0], pts[3,1], color)
    drawLine(canvas, pts[1,0], pts[1,1], 
                        pts[4,0], pts[4,1], color)
    drawLine(canvas, pts[2,0], pts[2,1], 
                        pts[4,0], pts[4,1], color)
    if axis == True: # center - pts[0]
        center = np.array([0., 0, 0])
        for p in pts:
            center += p 
        center = center / pts.shape[0]
        center = center.astype('int') 
        # print(center)
        drawLine(canvas, center[0],center[1], pts[0][0],pts[0][1], color=(255, 128, 128))
    return pts

def deg2rad(deg):
    rad = deg * np.pi / 180.
    return rad 

def getRegularNGon(ngon):
    delta = 360. / ngon
    points = []
    for i in range(ngon):
        degree = i * delta 
        radian = deg2rad(degree)
        x =   np.cos(radian)
        y =   np.sin(radian)
        points.append( (x, y,1) )
    #
    points = np.array(points)
    return points 

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

    theta = 0
    seconds = 0
    while True:
        a,b = np.random.randint(0,1300), np.random.randint(0,700)
    
        # get ngon points
        star1 = getRegularNGon(5) # vertices of the N-gon
        
        # scale up
        sc1 = np.random.randint(10,150)
        
        star1[:,0] *= sc1
        star1[:,1] *= sc1
        
        # rotating, translating points
        P = makeTmat(a,b) @ makeRmat(theta)
        
        r = np.random.randint(0,255)
        g = np.random.randint(0,255)
        b = np.random.randint(0,255)
        
        star1 = P @ star1.T
        star1 = star1.T
        star1 = star1.astype('int')
        getstar(canvas, star1,(b,g,r),axis = False) # yellow
        
        cv2.imshow("window", canvas)
        seconds+=1
        if seconds % 8==0:
            canvas[:, :, :] = 0

        if cv2.waitKey(20) == 27: break
        
#     
if __name__ == "__main__": # __ 
    main()
