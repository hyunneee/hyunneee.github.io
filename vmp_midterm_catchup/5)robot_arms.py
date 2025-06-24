#20211060 ohseohyun
import numpy as np
import cv2

height , width = 1000, 1500

def getline(x0,y0,x1,y1):
    points = []
    if (x0==x1):
        x = x0
        if y0>y1:
            for y in range(y0,y1+1,-1):
                points.append((x,y,1))
        else:
            for y in range(y0,y1+1):
                points.append((x,y,1))
        # print(points)
    elif abs((y1-y0)/(x1-x0)) < 1:    
        for x in range(x0,x1+1,1 if x0<x1 else -1):
            if x0 == x1:
                y = y0
            else:
                y = (x - x0) * (y1 - y0) / (x1 - x0) + y0
            yint = int(y)
            points.append((x,yint,1))   
    else: 
       for y in range(y0,y1+1,1 if y0<y1 else -1):
            if y0 == y1:
                x = x0
            else:
                x = (y   - y0) * (x1 - x0) / (y1 - y0) + x0
            xint = int(x)    
            points.append((xint,y,1))
                
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
    # print(type(shape)
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
    points.append((2*len,0,1))
    points.append((2*len,len,1))
    points.append((0,len,1))

    points = np.array(points)
    # print(points)
    return points

def main():
    canvas = np.zeros( (height, width, 3), dtype='uint8') 
    
    deg1 = 0
    deg2 = 0
    deg3 = 0   
    v1 = 1
    v2 = 2
    v3 = 3  

    a, b = width/2, height*2/3
    w,h = 140, 70

    while True:
        R1 = makeRmat(deg1)
        R2 = makeRmat(deg2)
        R3 = makeRmat(deg3)
        
    # get ngon points
        rect = getrectangle(h)
        rect2 = getrectangle(h)
        rect3 = getrectangle(h)
        rect4 = getrectangle(h)
       
    # drawing rect1    
        H1 = makeTmat(a,b) @ makeRmat(-90) @ makeTmat(0,-h/2)
        rect = H1 @ rect.T
        rect = rect.T
        rect = rect.astype('int')
        drawPolygon(canvas,rect,(0,0,255),axis = False)
    
    # drawing rect2 
        H2 = makeTmat(w,0) @ makeTmat(0,h/2) @ makeRmat(deg1) @ makeTmat(0,-h/2)
        rect2 = H1 @ H2 @ rect2.T
        rect2 = rect2.T
        rect2 = rect2.astype('int')
        drawPolygon(canvas,rect2,(255,0,255),axis = False)
        
    # drawing rect3
        H3 = makeTmat(w,0) @ makeTmat(0,h/2) @ makeRmat(deg2) @ makeTmat(0,-h/2)
        rect3 = H1 @ H2 @ H3 @ rect3.T
        rect3 = rect3.T
        rect3 = rect3.astype('int')
        drawPolygon(canvas,rect3,(255,255,255),axis = False)

    # drawing rect4
        H4 = makeTmat(w,0) @ makeTmat(0,h/2) @ makeRmat(deg3) @ makeTmat(0,-h/2)
        rect4 = H1 @ H2 @ H3 @ H4 @ rect4.T
        rect4 = rect4.T
        rect4 = rect4.astype('int')
        drawPolygon(canvas,rect4,(0,255,255),axis = False)
        
        if deg1 >= 15 or deg1<= -15:
            v1 = -v1
        if deg2 >= 30 or deg2 <= -30:
            v2 = -v2
        if deg3 >= 45 or deg3 <= -45:
            v3 = -v3
        
        deg1 += v1
        deg2 += v2
        deg3 += v3
        cv2.imshow("window", canvas)
        canvas[:, :, :] = 0
        
        if cv2.waitKey(20) == 27: break
#     
if __name__ == "__main__": # __ 
    main()
