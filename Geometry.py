import cv2
import numpy as np
import mediapipe as mp
import math

def make_circle(frame , paintWindow , center , thumb , middle_finger):
    b = (center[1]+thumb[1])//2
    a = (center[0]+thumb[0])//2
    c = (thumb[1] - b)**2
    d = (thumb[0] - a)**2
    radius = int(np.sqrt(c+d))
    frame = cv2.circle(frame , (a,b),radius,(0,0,0),2)
    paintWindow = cv2.circle(paintWindow , (a,b),radius,(0,0,0),2)
    if abs(middle_finger[1]-center[1]) < 10 or abs(middle_finger[0] - center[0]) < 10:
        #print("--------------------",abs(middle_finger[1]-center[1]),"------------------------")
        return [a,b,radius]
    else : return [None]*3
    
def make_quadri(frame , paintWindow ,center , thumb , middle_finger) :
    frame = cv2.rectangle(frame, thumb, center, (0,0,0), 2)
    paintWindow = cv2.rectangle(paintWindow, thumb, center, (0,0,0), 2)
    if abs(middle_finger[1]-center[1]) <10 or  abs(middle_finger[0] - center[0]) < 10:
        return [thumb , center]
    else : return [None]*2
    
def make_triangle(frame ,paintWindow , center , thumb , middle_finger , ring_finger) :
    center  = list(center)
    thumb = list(thumb)
    middle_finger = list(middle_finger)
    tri_points = np.array([center,thumb,middle_finger],np.int32)
    tri_points = tri_points.reshape((-1,1,2))
    frame = cv2.polylines(frame , [tri_points],True , (0,0,0) , 2)
    paintWindow = cv2.polylines(paintWindow , [tri_points],True , (0,0,0) , 2)
    if abs(middle_finger[1] - ring_finger[1]) < 10 or  abs(middle_finger[0] - ring_finger[0]) < 10:
        return [center , thumb , middle_finger]
    else : return [None , None , None]

def make_line(frame , paintWindow ,pt1 ,center ,middle_finger) :
    #print("make line banao")
    frame = cv2.line(frame , pt1 , center , (0,0,0) , 2)
    paintWindow = cv2.line(paintWindow , pt1 , center , (0,0,0) , 2)
    if(abs(middle_finger[1] - center[1]) < 15 or abs(middle_finger[0] - center[0]) < 15) :
        return [pt1 , center]
    else : return [None , None]

def make_arrowed_line(frame , paintWindow ,pt1 ,center , middle_finger) :
    #print("make arrow line banao")
    
    frame = cv2.arrowedLine(frame , pt1 , center , (0,0,0) , 2)
    paintWindow = cv2.arrowedLine(paintWindow , pt1 , center , (0,0,0) , 2)
    if(abs(middle_finger[1] - center[1]) < 15 or abs(middle_finger[0] - center[0]) < 15) :
        return [pt1 , center]
    else : return [None , None]

def find_slope(a,b) :
    slope = (b[1] - a[1]) / (b[0] - a[0] + 1e-6)
    return slope
def make_rhombus(frame , paintWindow ,center , thumb , middle_finger) :
    rhm2 = np.array([thumb[0] , thumb[1]])
    rhm4 = np.array([center[0] , center[1]]) 

    m1 = 0
    if(center[1] == thumb[1]) :
       m1 = 0

    # find the mid point of the diag 1
    else :
        if(thumb[1] < center[1]) :
            diag1 = (
                int((center[0] + thumb[0])//2) , int((center[1] + thumb[1])//2)
            )
            m1 = find_slope(thumb , center)
            
        else :
            diag1 = (
                int((thumb[0] + center[0])//2) ,int((thumb[1] + center[1])//2)
            )
            m1 = find_slope(center , thumb)
    #print("............................................................") 
    #length of the other diagonal 
    diag1_len = np.sqrt(
        ((center[0] - thumb[0])**2) + ((center[1] - thumb[1])**2)
    )
    diag2_len = diag1_len * 0.8        
    
    m2 = -1 / m1
    
    ## diag1 point pe banayenge
    b_perp = diag1[1] - m2 * diag1[0]

    dist = 0.5 * diag2_len
    b_parallel = diag1[1] - m1 * diag1[0] + dist * np.sqrt(1 + m1**2)
    x = (b_parallel - b_perp) / (m2 - m1)
    y = m2 * x + b_perp
    #frame = cv2.circle(frame , (int(x),int(y)) , 4 , (0,0,0) , -1)
    x1 = 2 * diag1[0] - x
    y1 = 2 * diag1[1] - y
    #frame = cv2.circle(frame , (int(x1),int(y1)) , 4 , (0,0,0) , -1)
    rhm1 = np.array([x1,y1])
    rhm3 = np.array([x , y])

    
    rhombus_pts = np.array([rhm1,rhm2,rhm3,rhm4],np.int32)
    rhombus_pts = rhombus_pts.reshape((-1,1,2))
    frame = cv2.polylines(frame , [rhombus_pts] , True , (0,0,0) , 2)
    paintWindow = cv2.polylines(paintWindow , [rhombus_pts] , True , (0,0,0) , 2)
    if(abs(middle_finger[1] - center[1]) < 15 or abs(middle_finger[0] - center[0]) < 15) :
        return rhombus_pts
    

def make_ellipse (frame , paintWindow ,center , thumb , middle_finger) :
    #frame = cv2.line(frame , center , thumb , (0,0,0) , 2)
    major_axis_length = int(np.sqrt(
        ((center[0] - thumb[0])**2) + ((center[1] - thumb[1])**2)
    ))
    minor_axis_length = int(0.2 * major_axis_length)
    dx = thumb[0] - center[0]
    dy = thumb[1] - center[1]
    if dy == 0:
        if dx >= 0:
            angle = 0
        else:
            angle = 180
    else:
        angle = math.degrees(math.atan2(dy, dx))
    ellipse_center = (
            (center[0] + thumb[0])//2 , (center[1] + thumb[1])//2
        )
    frame = cv2.ellipse(frame, ellipse_center, (major_axis_length//2 , minor_axis_length), 
           angle , 0, 360, (0,0,0), 2) 
    paintWindow = cv2.ellipse(paintWindow, ellipse_center, (major_axis_length//2 , minor_axis_length), 
           angle , 0, 360, (0,0,0), 2)
    print("after frame")
    if(abs(middle_finger[1] - center[1]) < 8 or abs(middle_finger[0] - center[0]) < 8) :
        return [ellipse_center , major_axis_length , minor_axis_length , angle]
    else : return [None]*4
