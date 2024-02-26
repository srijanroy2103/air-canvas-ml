import cv2
from collections import deque

def drawing(landmarks , start_end , frame , colors , colorIndex , bpoints ,gpoints , rpoints , ypoints , blue_index , green_index , red_index , yellow_index):
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