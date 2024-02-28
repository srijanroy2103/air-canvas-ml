import cv2
import numpy as np
import mediapipe as mp
from collections import deque
from Color_boxes import color_boxes


bpoints = [deque(maxlen=2048)]
gpoints = [deque(maxlen=2048)]
rpoints = [deque(maxlen=2048)]
ypoints = [deque(maxlen=2048)]


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

    
    # choose the hand screen
    if(flag == 0):
        frame = cv2.rectangle(frame , (int(0.25*wCam),int(0.25*hCam)) , (int(wCam*0.75) , int(hCam*0.75)) , (255,255,255),cv2.FILLED)

        frame = cv2.rectangle(frame , (int(0.25*wCam),int(0.25*hCam)) , (int(wCam*0.75) , int(hCam*0.75)) , (0,0,0),2)
        cv2.putText(frame , "CHOOSE THE HAND" , (350,300), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 0), 6, cv2.LINE_AA)

        ## Two boxes
        frame = cv2.rectangle(frame , (int(0.25*wCam),390) , (int(0.5*wCam) , 540) , (0,0,0),2)
        cv2.putText(frame , "LEFT" , (400, 460), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 4, cv2.LINE_AA)

        frame = cv2.rectangle(frame , (int(0.5*wCam),390) , (int(0.75*wCam) , 540) , (0,0,0),2)
        cv2.putText(frame , "RIGHT" , (740, 460), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 4, cv2.LINE_AA)

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
            index_finger = (landmarks[8][0],landmarks[8][1])
            center = index_finger
            thumb = (landmarks[4][0],landmarks[4][1])
            cv2.circle(frame, center, 7, (0,255,0),-1)
            print(center[1]-thumb[1])

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
            
            start_end = color_boxes(frame)
            ########
            # HAND DETECTION
            result = mpHands.process(framergb)

            
                
            if result.multi_hand_landmarks :
                landmarks = []
                for handslms in result.multi_hand_landmarks:
                    right_hand_landmarks = handslms.landmark
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

                    try :
                        index_finger = (landmarks[8][0],landmarks[8][1])
                        center = index_finger
                        thumb = (landmarks[4][0],landmarks[4][1])
                        cv2.circle(frame, center, 7, (0,255,0),-1)
                        print(center[1]-thumb[1])


                        #if the index finger tip is at the buttons space so don't draw
                        if center[1] <=65 :
                            # set the condition what to do

                            #clear button
                            if start_end[0] <= center[0] <start_end[1] and thumb[1]-center[1]<25:
                                #empty all the deques
                                    bpoints = [deque(maxlen=1024)]
                                    gpoints = [deque(maxlen=1024)]
                                    rpoints = [deque(maxlen=1024)]
                                    ypoints = [deque(maxlen=1024)]

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


                        ### whenb we pinch don't draw , so we are measuring the distance between the index finger and thumb tip if it comes below 20 then don't draw

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
                    except :
                        cv2.putText(frame, "WRONG HAND", (int(0.4*wCam), 120), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 4, cv2.LINE_AA)
                        print("Wrong hand")
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
                    
            points = [bpoints, gpoints, rpoints, ypoints]

            for i in range(len(points)):
                for j in range(len(points[i])):
                    for k in range(1, len(points[i][j])):
                        if points[i][j][k - 1] is None or points[i][j][k] is None:
                            continue
                        cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)

            if cv2.waitKey(1) == ord('q'):
                break          
        elif(left == 1) :
            start_end = color_boxes(frame)

            ########
            # HAND DETECTION
            result = mpHands.process(framergb)


            if result.multi_hand_landmarks :
                landmarks = []
                for handslms in result.multi_hand_landmarks:
                    left_hand_landmarks = handslms.landmark
                    if(left_hand_landmarks[4].x > left_hand_landmarks[20].x):
                        for lm in handslms.landmark:
                            # # print(id, lm)
                            # print(lm.x)
                            # print(lm.y)
                            lmx = int(lm.x * wCam)
                            lmy = int(lm.y * hCam)

                            landmarks.append([lmx, lmy])


                    # Drawing landmarks on frames
                    mpDraw.draw_landmarks(frame, handslms, mp.solutions.hands.HAND_CONNECTIONS)

                    try :
                        index_finger = (landmarks[8][0],landmarks[8][1])
                        center = index_finger
                        thumb = (landmarks[4][0],landmarks[4][1])
                        cv2.circle(frame, center, 7, (0,255,0),-1)
                        print(center[1]-thumb[1])


                        #if the index finger tip is at the buttons space so don't draw
                        if center[1] <=65 :
                            # set the condition what to do

                            #clear button
                            if start_end[0] <= center[0] <start_end[1] and thumb[1]-center[1]<25:
                                #empty all the deques
                                    bpoints = [deque(maxlen=1024)]
                                    gpoints = [deque(maxlen=1024)]
                                    rpoints = [deque(maxlen=1024)]
                                    ypoints = [deque(maxlen=1024)]

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


                        ### whenb we pinch don't draw , so we are measuring the distance between the index finger and thumb tip if it comes below 20 then don't draw

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
                    except :
                        cv2.putText(frame, "WRONG HAND", (int(0.4*wCam), 120), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 4, cv2.LINE_AA)
                        print("Wrong hand")
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
                    
            points = [bpoints, gpoints, rpoints, ypoints]

            for i in range(len(points)):
                for j in range(len(points[i])):
                    for k in range(1, len(points[i][j])):
                        if points[i][j][k - 1] is None or points[i][j][k] is None:
                            continue
                        cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)

            if cv2.waitKey(1) == ord('q'):
                break    
                    


    cv2.imshow("GESTURE CONTROLLED AIR CANVAS", frame)
    if cv2.waitKey(1) == ord('q'):
        break

# release the webcam and destroy all active windows
cap.release()
cv2.destroyAllWindows()

