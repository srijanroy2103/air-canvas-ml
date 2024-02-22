import cv2
import numpy as np
import mediapipe as mp
from collections import deque

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


while True :
    # Read each frame from the webcam
    _, frame = cap.read()

    frame_height , frame_width , frame_depth = frame.shape

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)

    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    ######
    #width of each box
    wBox = 150
    # space between each box
    spBox = 50
    # start point of the box
    start_box = 40
    ######

    # CLEAR button
    frame = cv2.rectangle(frame, (start_box,4), (start_box+wBox,65), (0,0,0), 2)
    cv2.putText(frame, "CLEAR", (start_box+9, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
    clear_start , clear_end = start_box , start_box + wBox
    start_box = start_box + wBox + spBox

    # BLUE button
    frame = cv2.rectangle(frame, (start_box,4), (start_box+wBox,65), (255,0,0), 2)
    cv2.putText(frame, "BLUE", (start_box+9, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
    blue_start , blue_end = start_box , start_box + wBox
    start_box = start_box + wBox + spBox

    # GREEN button
    frame = cv2.rectangle(frame, (start_box,4), (start_box+wBox,65), (0,255,0), 2)
    cv2.putText(frame, "GREEN", (start_box+9, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    green_start , green_end = start_box , start_box + wBox
    start_box = start_box + wBox + spBox

    # RED button
    frame = cv2.rectangle(frame, (start_box,4), (start_box+wBox,65), (0,0,255), 2)
    cv2.putText(frame, "RED", (start_box+9, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
    red_start , red_end = start_box , start_box + wBox
    start_box = start_box + wBox + spBox

    # YELLOW button
    frame = cv2.rectangle(frame, (start_box,4), (start_box+wBox+20,65), (0,255,255), 2)
    cv2.putText(frame, "YELLOW", (start_box+9, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
    yellow_start , yellow_end = start_box , start_box + wBox
    start_box = start_box + wBox + spBox


    ########
    # HAND DETECTION
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

        #if the index finger tip is at the buttons space so don't draw
        if center[1] <=65 :
            # set the condition what to do
        
            #clear button
            if clear_start <= center[0] <= clear_end and thumb[1]-center[1]<25:
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
            elif blue_start <= center[0] <= blue_end and blue_start <= thumb[0] <= blue_end and thumb[1]-center[1]<25: 
                    colorIndex = 0
            elif green_start <= center[0] <= green_end and green_start <= thumb[0] <= green_end and thumb[1]-center[1]<25: 
                    colorIndex = 1
            elif red_start <= center[0] <= red_end and red_start <= thumb[0] <= red_end and thumb[1]-center[1]<25: 
                    colorIndex = 2
            elif yellow_start <= center[0] <= yellow_end and yellow_start <= thumb[0] <= yellow_end and thumb[1]-center[1]<25: 
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

    ## Append the next deques when nothing is detected to avois messing up
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

    cv2.imshow("GESTURE CONTROLLED AIR CANVAS", frame)
    if cv2.waitKey(1) == ord('q'):
        break

# release the webcam and destroy all active windows
cap.release()
cv2.destroyAllWindows()

