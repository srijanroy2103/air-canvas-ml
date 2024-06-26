import cv2
import numpy as np
import mediapipe as mp
from collections import deque
from Color_boxes import color_boxes
from Geometry import make_circle , make_quadri , make_triangle , make_line , make_arrowed_line ,make_rhombus ,make_ellipse


bpoints = [deque(maxlen=2048)]
gpoints = [deque(maxlen=2048)]
rpoints = [deque(maxlen=2048)]
ypoints = [deque(maxlen=2048)]

#shapes coordinates
circle_points = []
quadri_points = []
triangle_points = []
line_points = []
arrowed_line_points =[]
rhombus_points = []
ellipse_points = []

makeline = False 
makearrowline = False
arrow_pt1 = ()
line_pt1 = ()

#used to indicate the current color changes
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

kernel = np.ones((5,5),np.uint8)


# specify the colors 
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

#initialize the mediapipe

mpHands = mp.solutions.hands.Hands(min_detection_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

### Set height and width of the camera 
wCam , hCam = 1280 , 720
#id for width is 3
cap.set(3,wCam)
#id for height is 3
cap.set(4,hCam)


####
# hand control flags
flag = 0
right = 0
left = 0


while True :
    # Read each frame from the webcam
    _, frame = cap.read()

    frame_height , frame_width , frame_depth = frame.shape

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)

    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    paintWindow = np.zeros((720,1280 , 3))+255
    
    # choose the hand screen
    if(flag == 0):
        frame = cv2.rectangle(frame , (int(0.25*wCam),int(0.25*hCam)) , (int(wCam*0.75) , int(hCam*0.75)) , (255,255,255),cv2.FILLED)
        paintWindow = cv2.rectangle(paintWindow , (int(0.25*wCam),int(0.25*hCam)) , (int(wCam*0.75) , int(hCam*0.75)) , (255,255,255),cv2.FILLED)

        frame = cv2.rectangle(frame , (int(0.25*wCam),int(0.25*hCam)) , (int(wCam*0.75) , int(hCam*0.75)) , (0,0,0),2)
        cv2.putText(frame , "CHOOSE THE HAND" , (350,300), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 0), 6, cv2.LINE_AA)
        paintWindow = cv2.rectangle(paintWindow , (int(0.25*wCam),int(0.25*hCam)) , (int(wCam*0.75) , int(hCam*0.75)) , (0,0,0),2)
        cv2.putText(paintWindow , "CHOOSE THE HAND" , (350,300), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 0), 6, cv2.LINE_AA)

        ## Two boxes
        frame = cv2.rectangle(frame , (int(0.25*wCam),390) , (int(0.5*wCam) , 540) , (0,0,0),2)
        cv2.putText(frame , "LEFT" , (400, 460), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 4, cv2.LINE_AA)
        paintWindow = cv2.rectangle(paintWindow , (int(0.25*wCam),390) , (int(0.5*wCam) , 540) , (0,0,0),2)
        cv2.putText(paintWindow , "LEFT" , (400, 460), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 4, cv2.LINE_AA)

        frame = cv2.rectangle(frame , (int(0.5*wCam),390) , (int(0.75*wCam) , 540) , (0,0,0),2)
        cv2.putText(frame , "RIGHT" , (740, 460), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 4, cv2.LINE_AA)
        paintWindow = cv2.rectangle(paintWindow , (int(0.5*wCam),390) , (int(0.75*wCam) , 540) , (0,0,0),2)
        cv2.putText(paintWindow , "RIGHT" , (740, 460), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 4, cv2.LINE_AA)

        result = mpHands.process(framergb)

        if result.multi_hand_landmarks :
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    # # print(id, lm)
                    # print(lm.x)
                    # print(lm.y)
                    lmx = int(lm.x * wCam)
                    lmy = int(lm.y * hCam)

                    landmarks.append([lmx, lmy])


                # Drawing landmarks on frames
                mpDraw.draw_landmarks(frame, handslms, mp.solutions.hands.HAND_CONNECTIONS)
                # in white board plotting the landmarks
                mpDraw.draw_landmarks(paintWindow, handslms, mp.solutions.hands.HAND_CONNECTIONS , mpDraw.DrawingSpec(color = (0,0,255)) ,mpDraw.DrawingSpec(color = (0,0,0)))


            index_finger = (landmarks[8][0],landmarks[8][1])
            center = index_finger
            thumb = (landmarks[4][0],landmarks[4][1])
            cv2.circle(frame, center, 7, (0,255,0),-1)
            cv2.circle(paintWindow, center, 7, (0,255,0),-1)
            #print(center[1]-thumb[1])

            if center[1] >=400 and center[1] <=530 :

                ##left hand
                if(thumb[1]-center[1] <=20 and 320<=center[0]<640) :
                    left = 1
                    flag = 1
                    print("LEFT IS CHOSEN")
                ## right hand
                elif(thumb[1]-center[1] <=20 and 640<center[0]<=960) :
                    right = 1
                    flag = 1
                    
                    print("RIGHT IS CHOSEN")

    else :

        if(right == 1):
            
            start_end = color_boxes(frame , paintWindow)
            ########
            # HAND DETECTION
            result = mpHands.process(framergb)

            
                
            if result.multi_hand_landmarks :
                landmarks = []
                wrong_and_landmarks_points = []
                for handslms in result.multi_hand_landmarks:
                    right_hand_landmarks = handslms.landmark
                    ## for left hand 
                    wrong_and_landmarks = handslms.landmark
                    if(wrong_and_landmarks[4].x > wrong_and_landmarks[20].x):
                        for lm in handslms.landmark:
                            # # print(id, lm)
                            # print(lm.x)
                            # print(lm.y)
                            lmx = int(lm.x * wCam)
                            lmy = int(lm.y * hCam)

                            wrong_and_landmarks_points.append([lmx, lmy])
                    
                    ## for RIGHT hand
                    if(right_hand_landmarks[4].x < right_hand_landmarks[20].x):
                        for lm in handslms.landmark:
                            # # print(id, lm)
                            # print(lm.x)
                            # print(lm.y)
                            lmx = int(lm.x * wCam)
                            lmy = int(lm.y * hCam)

                            landmarks.append([lmx, lmy])


                    # Drawing landmarks on frames
                    mpDraw.draw_landmarks(frame, handslms, mp.solutions.hands.HAND_CONNECTIONS)
                    mpDraw.draw_landmarks(paintWindow, handslms, mp.solutions.hands.HAND_CONNECTIONS , mpDraw.DrawingSpec(color = (0,0,255)) ,mpDraw.DrawingSpec(color = (0,0,0)))

                    try :
                        index_finger = (landmarks[8][0],landmarks[8][1])
                        center = index_finger
                        thumb = (landmarks[4][0],landmarks[4][1])
                        middle_finger = (landmarks[12][0] , landmarks[12][1])
                        ring_finger = (landmarks[16][0] , landmarks[16][1])
                        # cv2.circle(frame, ring_finger, 7, (0,0,0),-3)
                        cv2.circle(frame, center, 7, (0,255,0),-1)
                        cv2.circle(paintWindow, center, 7, (0,255,0),-1)
                        #print(center[1]-thumb[1])


                        #if the index finger tip is at the buttons space so don't draw
                        if center[1] <=100 :
                            # set the condition what to do

                            #clear button
                            if start_end[0] <= center[0] <start_end[1] and thumb[1]-center[1]<20:
                                #empty all the deques
                                    bpoints = [deque(maxlen=1024)]
                                    gpoints = [deque(maxlen=1024)]
                                    rpoints = [deque(maxlen=1024)]
                                    ypoints = [deque(maxlen=1024)]
                                    circle_points = []
                                    quadri_points = []
                                    triangle_points = []
                                    line_points = []
                                    arrowed_line_points =[]
                                    rhombus_points = []
                                    ellipse_points = []

                                    blue_index = 0
                                    green_index = 0
                                    red_index = 0
                                    yellow_index = 0

                            # pinch and choose the color
                            elif start_end[2] <= center[0] <= start_end[3] and start_end[2] <= thumb[0] <= start_end[3] and thumb[1]-center[1]<25: 
                                    colorIndex = 0
                            elif start_end[4] <= center[0] <= start_end[5] and start_end[4] <= thumb[0] <= start_end[5] and thumb[1]-center[1]<25: 
                                    colorIndex = 1
                            elif start_end[6] <= center[0] <= start_end[7] and start_end[6] <= thumb[0] <= start_end[7] and thumb[1]-center[1]<25: 
                                    colorIndex = 2
                            elif start_end[8] <= center[0] <= start_end[9] and start_end[8] <= thumb[0] <= start_end[9] and thumb[1]-center[1]<25: 
                                    colorIndex = 3
                            ##circle k liye
                            elif start_end[10] <= center[0] <= start_end[11] and start_end[10] <= thumb[0] <= start_end[11] and thumb[1]-center[1]<25:
                                 ## draw circle
                                 colorIndex = 4
                            ## quadrilateral banane k liye
                            elif start_end[12] <= center[0] <= start_end[13] and start_end[12] <= thumb[0] <= start_end[13] and thumb[1]-center[1]<25:
                                 colorIndex = 5
                            
                            ## triangle banane k liye 
                            elif start_end[14] <= center[0] <= start_end[15] and start_end[14] <= thumb[0] <= start_end[15] and thumb[1]-center[1]<25:
                                 print("-----------int ci 6---------------")
                                 colorIndex = 6

                            ## line banane k liye 
                            elif start_end[16] <= center[0] <= start_end[17] and start_end[16] <= thumb[0] <= start_end[17] and thumb[1]-center[1]<25:
                                
                                colorIndex = 7
                            
                            ## rhombus
                            elif start_end[18] <= center[0] <= start_end[19] and start_end[18] <= thumb[0] <= start_end[19] and thumb[1]-center[1]<25 :
                                 print("inside rhombus")
                                 colorIndex = 8

                            ##ellipse 
                            elif start_end[20] <= center[0] <= start_end[21] and start_end[20] <= thumb[0] <= start_end[21] and thumb[1]-center[1]<25 :
                                 print("inside ellipse")
                                 colorIndex = 9

                        ### when we pinch don't draw , so we are measuring the distance between the index finger and thumb tip if it comes below 20 then don't draw

                        elif (thumb[1]-center[1]<15) and colorIndex < 4 :
                            bpoints.append(deque(maxlen=1024))
                            blue_index += 1
                            gpoints.append(deque(maxlen=1024))
                            green_index += 1
                            rpoints.append(deque(maxlen=1024))
                            red_index += 1
                            ypoints.append(deque(maxlen=1024))
                            yellow_index += 1

                        ## DRAW Condition
                        else :
                            if colorIndex == 0:
                                bpoints[blue_index].appendleft(center)
                            elif colorIndex == 1:
                                gpoints[green_index].appendleft(center)
                            elif colorIndex == 2:
                                rpoints[red_index].appendleft(center)
                            elif colorIndex == 3:
                                ypoints[yellow_index].appendleft(center)
                            elif colorIndex == 4:
                                circle_arr = make_circle(frame , paintWindow ,center , thumb , middle_finger)
                                if(circle_arr[0] is not None) : 
                                    cv2.circle(frame , (circle_arr[0],circle_arr[1]),circle_arr[2],(0,0,0),2)
                                    cv2.circle(paintWindow , (circle_arr[0],circle_arr[1]),circle_arr[2],(0,0,0),2)
                                    circle_points.append(circle_arr)
                                    #print("oooooooooooooooooooo")
                                    colorIndex = 20

                            elif colorIndex == 5 :
                                quadri_arr = make_quadri(frame , paintWindow ,center , thumb , middle_finger)
                                if(quadri_arr[0] is not None) :
                                    cv2.rectangle(frame, (quadri_arr[0][0],quadri_arr[0][1]), (quadri_arr[1][0],quadri_arr[1][1]), (0,0,0), 2)
                                    cv2.rectangle(paintWindow, (quadri_arr[0][0],quadri_arr[0][1]), (quadri_arr[1][0],quadri_arr[1][1]), (0,0,0), 2)
                                    quadri_points.append(quadri_arr)
                                    #print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
                                    colorIndex = 20

                            elif colorIndex == 6 :
                                tri_arr = make_triangle(frame , paintWindow ,center , thumb , middle_finger , ring_finger)
                                if tri_arr[0] is not None:
                                    tri_pts = np.array(tri_arr,np.int32)
                                    tri_pts = tri_pts.reshape((-1,1,2))
                                    cv2.polylines(frame , [tri_pts],isClosed=True , color=(0,0,0) , thickness=2)
                                    #print("triangle displayed-1")
                                    cv2.polylines(paintWindow , [tri_pts],isClosed=True , color=(0,0,0) , thickness=2)
                                    #print("triangle displayed-2")
                                    triangle_points.append(tri_pts)
                                    colorIndex = 20
                            
                            elif colorIndex == 7 :
                                if(makeline == False and makearrowline == False):
                                    cv2.putText(frame , "Press l for line a for arrowed line" ,(int(0.4*wCam),90) , cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
                                    cv2.putText(paintWindow , "Press l for line a for arrowed line" ,(int(0.4*wCam),90) , cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
                                    k = cv2.waitKey(1)
                                    if(k == ord('l')) :
                                        makeline = True
                                        makearrowline = False
                                        #print(makeline , makearrowline)
                                    elif(k == ord('a')) :
                                         makeline = False 
                                         makearrowline = True  
                                         
                                
                                elif(makeline == True and makearrowline == False) :
                                    if(abs(center[0]-thumb[0])<10 or abs(center[1]-thumb[1])<10) :
                                        line_pt1 = center
                                    if(len(line_pt1) > 0):
                                        line_arr = make_line(frame , paintWindow , line_pt1 , center , middle_finger)
                                        if(line_arr[0] is not None) :
                                            frame = cv2.line(frame , line_arr[0] , line_arr[1] , (0,0,0) , 2 , cv2.LINE_AA)
                                            paintWindow = cv2.line(paintWindow , line_arr[0] , line_arr[1] , (0,0,0) , 2 ,cv2.LINE_AA)
                                            line_points.append(line_arr)
                                            
                                            makeline = False
                                            line_pt1 = ()
                                            colorIndex = 20                                        
                                
                                elif(makearrowline == True and makeline == False) :
                                    if(abs(center[0]-thumb[0])<10 or abs(center[1]-thumb[1])<10) :
                                        arrow_pt1 = center
                                    if(len(arrow_pt1) > 0) :
                                        arrowed_line_arr = make_arrowed_line(frame ,paintWindow , arrow_pt1 , center , middle_finger)
                                        if(arrowed_line_arr[0] is not None) :
                                            frame = cv2.arrowedLine(frame , arrowed_line_arr[0] , arrowed_line_arr[1] , (0,0,0) , 2 , cv2.LINE_AA)
                                            paintWindow = cv2.arrowedLine(paintWindow , arrowed_line_arr[0] , arrowed_line_arr[1] , (0,0,0) , 2 , cv2.LINE_AA)
                                            arrowed_line_points.append(arrowed_line_arr)
                                            
                                            makearrowline = False
                                            arrow_pt1 = ()
                                            colorIndex = 20

                            elif colorIndex == 8 :
                                
                                rhombus_arr = make_rhombus(frame , paintWindow , center , thumb , middle_finger)
                                if(rhombus_arr is not None) :                                     
                                    rhombus_pts = np.array(rhombus_arr)
                                    rhombus_pts = rhombus_pts.reshape((-1,1,2))
                                    cv2.polylines(frame , [rhombus_pts],True , (0,0,0) , 2,cv2.LINE_AA)
                                    cv2.polylines(paintWindow , [rhombus_pts],True , (0,0,0) , 2 , cv2.LINE_AA)
                                    rhombus_points.append(rhombus_pts)
                                    colorIndex = 20
                            
                            elif colorIndex == 9 :
                                ellipse_arr = make_ellipse (frame , paintWindow ,center , thumb , middle_finger)
                                if(ellipse_arr[0] is not None) :
                                    cv2.ellipse(frame , ellipse_arr[0] , (ellipse_arr[1]//2 , ellipse_arr[2]) , ellipse_arr[3] , 0,360,(0,0,0) , 2)
                                    cv2.ellipse(paintWindow , ellipse_arr[0] , (ellipse_arr[1]//2 , ellipse_arr[2]) , ellipse_arr[3] , 0,360,(0,0,0) , 2)
                                    ellipse_points.append(ellipse_arr)
                                    colorIndex = 20


                    except :
                        try :
                            p = (wrong_and_landmarks_points[9][0] , wrong_and_landmarks_points[9][1])
                            #cv2.putText(frame, "WRONG HAND", (int(0.4*wCam), 120), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 4, cv2.LINE_AA)
                            cv2.putText(frame, "WRONG HAND", (p[0]-50, p[1]+70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2, cv2.LINE_AA)
                            cv2.putText(paintWindow, "WRONG HAND", (p[0]-50, p[1]+70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2, cv2.LINE_AA)
                            print("Wrong hand")
                        except : 
                             print(KeyError)

            ## Append the next deques when nothing is detected to avoid messing up
            else:
                bpoints.append(deque(maxlen=1024))
                blue_index += 1
                gpoints.append(deque(maxlen=1024))
                green_index += 1
                rpoints.append(deque(maxlen=1024))
                red_index += 1
                ypoints.append(deque(maxlen=1024))
                yellow_index += 1
            
            if(len(ellipse_points) > 0) :
                for i in range(len(ellipse_points)) :
                    cv2.ellipse(frame , ellipse_points[i][0] , (ellipse_points[i][1]//2 , ellipse_points[i][2]) , ellipse_points[i][3] , 0,360,(0,0,0) , 2)
                    cv2.ellipse(paintWindow , ellipse_points[i][0] , (ellipse_points[i][1]//2 , ellipse_points[i][2]) , ellipse_points[i][3] , 0,360,(0,0,0) , 2 ,cv2.LINE_AA)

            if(len(line_points) > 0):
                 for i in range(len(line_points)) :
                      cv2.line(frame , line_points[i][0] , line_points[i][1] , (0,0,0) ,2 , cv2.LINE_AA)
                      cv2.line(paintWindow , line_points[i][0] , line_points[i][1] , (0,0,0) ,2,cv2.LINE_AA)

            if(len(arrowed_line_points) > 0):
                 for i in range(len(arrowed_line_points)) :
                      cv2.arrowedLine(frame , arrowed_line_points[i][0] , arrowed_line_points[i][1] , (0,0,0) ,2,cv2.LINE_AA)
                      cv2.arrowedLine(paintWindow , arrowed_line_points[i][0] , arrowed_line_points[i][1] , (0,0,0) ,2,cv2.LINE_AA)

            if(len(triangle_points)>0):
                 for i in range(len(triangle_points)):
                      cv2.polylines(frame , [triangle_points[i]],True,(0,0,0),2,cv2.LINE_AA)
                      cv2.polylines(paintWindow , [triangle_points[i]],True,(0,0,0),2,cv2.LINE_AA)

            if(len(quadri_points)>0):
                 for i in range(len(quadri_points)):
                      cv2.rectangle(frame , quadri_points[i][0] , quadri_points[i][1],(0,0,0) , 2,cv2.LINE_AA)
                      cv2.rectangle(paintWindow , quadri_points[i][0] , quadri_points[i][1],(0,0,0) , 2,cv2.LINE_AA)
                      
            if len(circle_points)>0 :
                for i in range(len(circle_points)):
                        list(circle_points[i])
                        a , b, radius = circle_points[i][0],circle_points[i][1],circle_points[i][2]
                        cv2.circle(frame , (a,b),radius,(0,0,0),2 ,cv2.LINE_AA)
                        cv2.circle(paintWindow , (a,b),radius,(0,0,0),2 ,cv2.LINE_AA)
            if len(rhombus_points) > 0 :
                 for i in range(len(rhombus_points)) :
                    #list(rhombus_points[i])
                    cv2.polylines(frame , [rhombus_points[i]] , True , (0,0,0) , 2 ,cv2.LINE_AA)
                    cv2.polylines(paintWindow , [rhombus_points[i]] , True , (0,0,0) , 2 ,cv2.LINE_AA)

                    
            points = [bpoints, gpoints, rpoints, ypoints]

            for i in range(len(points)):
                for j in range(len(points[i])):
                    for k in range(1, len(points[i][j])):
                        if points[i][j][k - 1] is None or points[i][j][k] is None:
                            continue
                        cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                        cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

            if cv2.waitKey(1) == ord('q'):
                break          
        elif(left == 1) :

            start_end = color_boxes(frame , paintWindow)

            ########
            # HAND DETECTION
            result = mpHands.process(framergb)


            if result.multi_hand_landmarks :
                landmarks = []
                wrong_and_landmarks_points = []
                for handslms in result.multi_hand_landmarks:
                    right_hand_landmarks = handslms.landmark
                    ## for right hand 
                    wrong_and_landmarks = handslms.landmark
                    if(wrong_and_landmarks[4].x < wrong_and_landmarks[20].x):
                        for lm in handslms.landmark:
                            # # print(id, lm)
                            # print(lm.x)
                            # print(lm.y)
                            lmx = int(lm.x * wCam)
                            lmy = int(lm.y * hCam)

                            wrong_and_landmarks_points.append([lmx, lmy])
                    
                    ## for LEFT hand
                    if(right_hand_landmarks[4].x > right_hand_landmarks[20].x):
                        for lm in handslms.landmark:
                            # # print(id, lm)
                            # print(lm.x)
                            # print(lm.y)
                            lmx = int(lm.x * wCam)
                            lmy = int(lm.y * hCam)

                            landmarks.append([lmx, lmy])


                    # Drawing landmarks on frames
                    mpDraw.draw_landmarks(frame, handslms, mp.solutions.hands.HAND_CONNECTIONS)
                    mpDraw.draw_landmarks(paintWindow, handslms, mp.solutions.hands.HAND_CONNECTIONS , mpDraw.DrawingSpec(color = (0,0,255)) ,mpDraw.DrawingSpec(color = (0,0,0)))

                    try :
                        index_finger = (landmarks[8][0],landmarks[8][1])
                        center = index_finger
                        thumb = (landmarks[4][0],landmarks[4][1])
                        middle_finger = (landmarks[12][0] , landmarks[12][1])
                        ring_finger = (landmarks[16][0] , landmarks[16][1])
                        # cv2.circle(frame, ring_finger, 7, (0,0,0),-3)
                        cv2.circle(frame, center, 7, (0,255,0),-1)
                        cv2.circle(paintWindow, center, 7, (0,255,0),-1)
                        #print(center[1]-thumb[1])


                        #if the index finger tip is at the buttons space so don't draw
                        if center[1] <=100 :
                            # set the condition what to do

                            #clear button
                            if start_end[0] <= center[0] <start_end[1] and thumb[1]-center[1]<20:
                                #empty all the deques
                                    bpoints = [deque(maxlen=1024)]
                                    gpoints = [deque(maxlen=1024)]
                                    rpoints = [deque(maxlen=1024)]
                                    ypoints = [deque(maxlen=1024)]
                                    circle_points = []
                                    quadri_points = []
                                    triangle_points = []
                                    line_points = []
                                    arrowed_line_points =[]
                                    rhombus_points = []
                                    ellipse_points = []

                                    blue_index = 0
                                    green_index = 0
                                    red_index = 0
                                    yellow_index = 0

                            # pinch and choose the color
                            elif start_end[2] <= center[0] <= start_end[3] and start_end[2] <= thumb[0] <= start_end[3] and thumb[1]-center[1]<25: 
                                    colorIndex = 0
                            elif start_end[4] <= center[0] <= start_end[5] and start_end[4] <= thumb[0] <= start_end[5] and thumb[1]-center[1]<25: 
                                    colorIndex = 1
                            elif start_end[6] <= center[0] <= start_end[7] and start_end[6] <= thumb[0] <= start_end[7] and thumb[1]-center[1]<25: 
                                    colorIndex = 2
                            elif start_end[8] <= center[0] <= start_end[9] and start_end[8] <= thumb[0] <= start_end[9] and thumb[1]-center[1]<25: 
                                    colorIndex = 3
                            ##circle k liye
                            elif start_end[10] <= center[0] <= start_end[11] and start_end[10] <= thumb[0] <= start_end[11] and thumb[1]-center[1]<25:
                                 ## draw circle
                                 colorIndex = 4
                            ## quadrilateral banane k liye
                            elif start_end[12] <= center[0] <= start_end[13] and start_end[12] <= thumb[0] <= start_end[13] and thumb[1]-center[1]<25:
                                 colorIndex = 5
                            
                            ## triangle banane k liye 
                            elif start_end[14] <= center[0] <= start_end[15] and start_end[14] <= thumb[0] <= start_end[15] and thumb[1]-center[1]<25:
                                 #print("-----------int ci 6---------------")
                                 colorIndex = 6

                            ## line banane k liye 
                            elif start_end[16] <= center[0] <= start_end[17] and start_end[16] <= thumb[0] <= start_end[17] and thumb[1]-center[1]<25:
                                 #print("****************** in ci *************")
                                 colorIndex = 7

                            ## rhombus
                            elif start_end[18] <= center[0] <= start_end[19] and start_end[18] <= thumb[0] <= start_end[19] and thumb[1]-center[1]<25 :
                                 print("inside rhombus")
                                 colorIndex = 8

                            ##ellipse 
                            elif start_end[20] <= center[0] <= start_end[21] and start_end[20] <= thumb[0] <= start_end[21] and thumb[1]-center[1]<25 :
                                 print("inside ellipse")
                                 colorIndex = 9

                        ### when we pinch don't draw , so we are measuring the distance between the index finger and thumb tip if it comes below 20 then don't draw

                        elif (thumb[1]-center[1]<20):
                            bpoints.append(deque(maxlen=1024))
                            blue_index += 1
                            gpoints.append(deque(maxlen=1024))
                            green_index += 1
                            rpoints.append(deque(maxlen=1024))
                            red_index += 1
                            ypoints.append(deque(maxlen=1024))
                            yellow_index += 1

                        ## DRAW Condition
                        else :
                            if colorIndex == 0:
                                bpoints[blue_index].appendleft(center)
                            elif colorIndex == 1:
                                gpoints[green_index].appendleft(center)
                            elif colorIndex == 2:
                                rpoints[red_index].appendleft(center)
                            elif colorIndex == 3:
                                ypoints[yellow_index].appendleft(center)
                            elif colorIndex == 4:
                                circle_arr = make_circle(frame , paintWindow ,center , thumb , middle_finger)
                                if(circle_arr[0] is not None) : 
                                    cv2.circle(frame , (circle_arr[0],circle_arr[1]),circle_arr[2],(0,0,0),2)
                                    cv2.circle(paintWindow , (circle_arr[0],circle_arr[1]),circle_arr[2],(0,0,0),2)
                                    circle_points.append(circle_arr)
                                    #print("oooooooooooooooooooo")
                                    colorIndex = 20

                            elif colorIndex == 5 :
                                quadri_arr = make_quadri(frame , paintWindow ,center , thumb , middle_finger)
                                if(quadri_arr[0] is not None) :
                                    cv2.rectangle(frame, (quadri_arr[0][0],quadri_arr[0][1]), (quadri_arr[1][0],quadri_arr[1][1]), (0,0,0), 2)
                                    cv2.rectangle(paintWindow, (quadri_arr[0][0],quadri_arr[0][1]), (quadri_arr[1][0],quadri_arr[1][1]), (0,0,0), 2)
                                    quadri_points.append(quadri_arr)
                                    #print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
                                    colorIndex = 20

                            elif colorIndex == 6 :
                                tri_arr = make_triangle(frame , paintWindow ,center , thumb , middle_finger , ring_finger)
                                if tri_arr[0] is not None:
                                    tri_pts = np.array(tri_arr,np.int32)
                                    tri_pts = tri_pts.reshape((-1,1,2))
                                    cv2.polylines(frame , [tri_pts],isClosed=True , color=(0,0,0) , thickness=2)
                                    #print("triangle displayed-1")
                                    cv2.polylines(paintWindow , [tri_pts],isClosed=True , color=(0,0,0) , thickness=2)
                                    #print("triangle displayed-2")
                                    triangle_points.append(tri_pts)
                                    colorIndex = 20
                            
                            elif colorIndex == 7 :
                                if(makeline == False and makearrowline == False):
                                    cv2.putText(frame , "Press l for line a for arrowed line" ,(int(0.4*wCam),90) , cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
                                    cv2.putText(paintWindow , "Press l for line a for arrowed line" ,(int(0.4*wCam),90) , cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
                                    k = cv2.waitKey(1)
                                    if(k == ord('l')) :
                                        makeline = True
                                        makearrowline = False
                                        #print(makeline , makearrowline)
                                    elif(k == ord('a')) :
                                         makeline = False 
                                         makearrowline = True  
                                         
                                
                                elif(makeline == True and makearrowline == False) :
                                    if(abs(center[0]-thumb[0])<10 or abs(center[1]-thumb[1])<10) :
                                        line_pt1 = center
                                    if(len(line_pt1) > 0):
                                        line_arr = make_line(frame , paintWindow , line_pt1 , center , middle_finger)
                                        if(line_arr[0] is not None) :
                                            frame = cv2.line(frame , line_arr[0] , line_arr[1] , (0,0,0) , 2 , cv2.LINE_AA)
                                            paintWindow = cv2.line(paintWindow , line_arr[0] , line_arr[1] , (0,0,0) , 2 ,cv2.LINE_AA)
                                            line_points.append(line_arr)
                                            
                                            makeline = False
                                            line_pt1 = ()
                                            colorIndex = 20                                        
                                
                                elif(makearrowline == True and makeline == False) :
                                    if(abs(center[0]-thumb[0])<10 or abs(center[1]-thumb[1])<10) :
                                        arrow_pt1 = center
                                    if(len(arrow_pt1) > 0) :
                                        arrowed_line_arr = make_arrowed_line(frame ,paintWindow , arrow_pt1 , center , middle_finger)
                                        if(arrowed_line_arr[0] is not None) :
                                            frame = cv2.arrowedLine(frame , arrowed_line_arr[0] , arrowed_line_arr[1] , (0,0,0) , 2 , cv2.LINE_AA)
                                            paintWindow = cv2.arrowedLine(paintWindow , arrowed_line_arr[0] , arrowed_line_arr[1] , (0,0,0) , 2 , cv2.LINE_AA)
                                            arrowed_line_points.append(arrowed_line_arr)
                                            
                                            makearrowline = False
                                            arrow_pt1 = ()
                                            colorIndex = 20

                            elif colorIndex == 8 :
                                
                                rhombus_arr = make_rhombus(frame , paintWindow , center , thumb , middle_finger)
                                if(rhombus_arr is not None) :                                     
                                    rhombus_pts = np.array(rhombus_arr)
                                    rhombus_pts = rhombus_pts.reshape((-1,1,2))
                                    cv2.polylines(frame , [rhombus_pts],True , (0,0,0) , 2,cv2.LINE_AA)
                                    cv2.polylines(paintWindow , [rhombus_pts],True , (0,0,0) , 2 , cv2.LINE_AA)
                                    rhombus_points.append(rhombus_pts)
                                    colorIndex = 20
                            
                            elif colorIndex == 9 :
                                ellipse_arr = make_ellipse (frame , paintWindow ,center , thumb , middle_finger)
                                if(ellipse_arr[0] is not None) :
                                    cv2.ellipse(frame , ellipse_arr[0] , (ellipse_arr[1]//2 , ellipse_arr[2]) , ellipse_arr[3] , 0,360,(0,0,0) , 2)
                                    cv2.ellipse(paintWindow , ellipse_arr[0] , (ellipse_arr[1]//2 , ellipse_arr[2]) , ellipse_arr[3] , 0,360,(0,0,0) , 2)
                                    ellipse_points.append(ellipse_arr)
                                    colorIndex = 20
                                                            

                    except :
                        try :
                            p = (wrong_and_landmarks_points[9][0] , wrong_and_landmarks_points[9][1])
                            #cv2.putText(frame, "WRONG HAND", (int(0.4*wCam), 120), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 4, cv2.LINE_AA)
                            cv2.putText(frame, "WRONG HAND", (p[0]-50, p[1]+70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2, cv2.LINE_AA)
                            cv2.putText(paintWindow, "WRONG HAND", (p[0]-50, p[1]+70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2, cv2.LINE_AA)
                            print("Wrong hand")
                        except : 
                             print(KeyError)
            ## Append the next deques when nothing is detected to avoid messing up
            else:
                bpoints.append(deque(maxlen=1024))
                blue_index += 1
                gpoints.append(deque(maxlen=1024))
                green_index += 1
                rpoints.append(deque(maxlen=1024))
                red_index += 1
                ypoints.append(deque(maxlen=1024))
                yellow_index += 1

            if(len(ellipse_points) > 0) :
                for i in range(len(ellipse_points)) :
                    cv2.ellipse(frame , ellipse_points[i][0] , (ellipse_points[i][1]//2 , ellipse_points[i][2]) , ellipse_points[i][3] , 0,360,(0,0,0) , 2)
                    cv2.ellipse(paintWindow , ellipse_points[i][0] , (ellipse_points[i][1]//2 , ellipse_points[i][2]) , ellipse_points[i][3] , 0,360,(0,0,0) , 2 , cv2.LINE_AA)

            if(len(line_points) > 0):
                 for i in range(len(line_points)) :
                      cv2.line(frame , line_points[i][0] , line_points[i][1] , (0,0,0) ,2 , cv2.LINE_AA)
                      cv2.line(paintWindow , line_points[i][0] , line_points[i][1] , (0,0,0) ,2,cv2.LINE_AA)

            if(len(arrowed_line_points) > 0):
                 for i in range(len(arrowed_line_points)) :
                      cv2.arrowedLine(frame , arrowed_line_points[i][0] , arrowed_line_points[i][1] , (0,0,0) ,2,cv2.LINE_AA)
                      cv2.arrowedLine(paintWindow , arrowed_line_points[i][0] , arrowed_line_points[i][1] , (0,0,0) ,2,cv2.LINE_AA)

            if(len(triangle_points)>0):
                 for i in range(len(triangle_points)):
                      cv2.polylines(frame , [triangle_points[i]],True,(0,0,0),2,cv2.LINE_AA)
                      cv2.polylines(paintWindow , [triangle_points[i]],True,(0,0,0),2,cv2.LINE_AA)

            if(len(quadri_points)>0):
                 for i in range(len(quadri_points)):
                      cv2.rectangle(frame , quadri_points[i][0] , quadri_points[i][1],(0,0,0) , 2,cv2.LINE_AA)
                      cv2.rectangle(paintWindow , quadri_points[i][0] , quadri_points[i][1],(0,0,0) , 2,cv2.LINE_AA)
                      
            if len(circle_points)>0 :
                for i in range(len(circle_points)):
                        list(circle_points[i])
                        a , b, radius = circle_points[i][0],circle_points[i][1],circle_points[i][2]
                        cv2.circle(frame , (a,b),radius,(0,0,0),2 ,cv2.LINE_AA)
                        cv2.circle(paintWindow , (a,b),radius,(0,0,0),2 ,cv2.LINE_AA)
            if len(rhombus_points) > 0 :
                 for i in range(len(rhombus_points)) :
                    #list(rhombus_points[i])
                    cv2.polylines(frame , [rhombus_points[i]] , True , (0,0,0) , 2 ,cv2.LINE_AA)
                    cv2.polylines(paintWindow , [rhombus_points[i]] , True , (0,0,0) , 2 ,cv2.LINE_AA)
        
            points = [bpoints, gpoints, rpoints, ypoints]

            for i in range(len(points)):
                for j in range(len(points[i])):
                    for k in range(1, len(points[i][j])):
                        if points[i][j][k - 1] is None or points[i][j][k] is None:
                            continue
                        cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                        cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

            if cv2.waitKey(1) == ord('q'):
                break    
                    


    cv2.imshow("GESTURE CONTROLLED AIR CANVAS", frame)
    cv2.imshow("PAINT WINDOW", paintWindow)

    if cv2.waitKey(1) == ord('q'):
        break

# release the webcam and destroy all active windows
cap.release()
cv2.destroyAllWindows()

