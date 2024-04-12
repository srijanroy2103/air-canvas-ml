import cv2
import numpy as np

def color_boxes (frame):
     ######
    #width of each box
    wBox = 90
    # space between each box
    spBox = 30
    # start point of the box
    start_box = 60
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
    #cv2.line(frame , (blue_start ,80) , (blue_end , 80),(255,0,0),2)
    #cv2.circle(frame , (track_bar[0] , 80) , 4 , (0,0,0) , -4)
    start_box = start_box + wBox + spBox

    # GREEN button
    frame = cv2.rectangle(frame, (start_box,4), (start_box+wBox,65), (0,255,0), 2)
    cv2.putText(frame, "GREEN", (start_box+9, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    green_start , green_end = start_box , start_box + wBox
    #cv2.line(frame , (green_start ,80) , (green_end , 80),(0,255,0),2)
    #cv2.circle(frame , (track_bar[1] , 80) , 4 , (0,0,0) , -4)
    start_box = start_box + wBox + spBox

    # RED button
    frame = cv2.rectangle(frame, (start_box,4), (start_box+wBox,65), (0,0,255), 2)
    cv2.putText(frame, "RED", (start_box+9, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
    red_start , red_end = start_box , start_box + wBox
    #cv2.line(frame , (red_start ,80) , (red_end , 80),(0,0,255),2)
    #cv2.circle(frame , (track_bar[2] , 80) , 4 , (0,0,0) , -4)
    start_box = start_box + wBox + spBox

    # YELLOW button
    frame = cv2.rectangle(frame, (start_box,4), (start_box+wBox+20,65), (0,255,255), 2)
    cv2.putText(frame, "YELLOW", (start_box+9, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
    yellow_start , yellow_end = start_box , start_box + wBox
    start_box = start_box + wBox + spBox

    #circle button
    frame = cv2.circle(frame, (start_box+40,40) , 35 ,(0,0,0),2)
    circle_st , circle_end = start_box , start_box+80
    start_box = start_box + 100

    ## rectangle button
    frame = cv2.rectangle(frame, (start_box,6), (start_box+70,65), (0,0,0), 2)
    quadri_start , quadri_end = start_box , start_box+70
    start_box = start_box + 100
    

    ##triangle
    p1 = [start_box , 65]
    p2 = [start_box+150 , 65]
    tri_start , tri_end = p1[0] , p2[0]
    tri_height = int((np.sqrt(3)/4)*(p2[0] - p1[0]))
    #print("*************",tri_height)
    p3 = [start_box+(p2[0] - p1[0])//2 , 75 - tri_height]
    triangle_pts = np.array([p1,p2,p3],np.int32)
    triangle_pts = triangle_pts.reshape((-1,1,2))
    frame = cv2.polylines(frame , [triangle_pts],isClosed=True , color=(0,0,0),thickness=2)

    #line button
    frame = cv2.rectangle(frame, (tri_end+20,4), (tri_end+90,65), (0,0,0), 2)
    frame = cv2.line(frame , (tri_end+30,30) , (tri_end+90-10,30) , (0,0,0) , 2,cv2.LINE_AA)
    line_start , line_end = tri_end+20 ,tri_end+90
    ## dividing line
    cv2.line(frame , (0,100) , (1280,100) , (0,0,0) , 2,cv2.LINE_AA)
    ## to keep a track of the color boxes indices
    return [clear_start , clear_end , blue_start , blue_end , green_start , green_end , red_start , red_end , yellow_start , yellow_end,circle_st , circle_end ,quadri_start , quadri_end , tri_start , tri_end , line_start , line_end]