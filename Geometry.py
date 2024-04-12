import cv2
import numpy as np
import mediapipe as mp

def make_circle(frame , center , thumb , middle_finger):
    b = (center[1]+thumb[1])//2
    a = (center[0]+thumb[0])//2
    c = (thumb[1] - b)**2
    d = (thumb[0] - a)**2
    radius = int(np.sqrt(c+d))
    frame = cv2.circle(frame , (a,b),radius,(0,0,0),2)
    if abs(middle_finger[1]-center[1]) <10 :
        #print("--------------------",abs(middle_finger[1]-center[1]),"------------------------")
        return (a,b,radius)
    
def make_quadri(frame , center , thumb , middle_finger) :
    frame = cv2.rectangle(frame, thumb, center, (0,0,0), 2)
    if abs(middle_finger[1]-center[1]) <10 :
        return [thumb , center]
    
def make_triangle(frame , center , thumb , middle_finger , ring_finger) :
    center  = list(center)
    thumb = list(thumb)
    middle_finger = list(middle_finger)
    tri_points = np.array([center,thumb,middle_finger],np.int32)
    tri_points = tri_points.reshape((-1,1,2))
    frame = cv2.polylines(frame , [tri_points],True , (0,0,0) , 2)
    if abs(middle_finger[1] - ring_finger[1]) < 10 :
        return [center , thumb , middle_finger]
    
def make_line(frame , center , thumb ,middle_finger) :
    frame = cv2.line(frame , center , thumb , (0,0,0) , 2)
    if(abs(middle_finger[1] - center[1]) < 10) :
        return [center , thumb]