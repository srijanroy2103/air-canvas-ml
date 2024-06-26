import cv2
import numpy as np

def color_boxes (frame , paintWindow):
     ######
    #width of each box
    wBox = 90
    # space between each box
    spBox = 30
    # start point of the box
    start_box = 50
    ######

    # CLEAR button
    frame = cv2.rectangle(frame, (start_box,4), (start_box+wBox,65), (0,0,0), 2)
    cv2.putText(frame, "CLEAR", (start_box+9, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
    paintWindow = cv2.rectangle(paintWindow, (start_box,4), (start_box+wBox,65), (0,0,0), 2)
    cv2.putText(paintWindow, "CLEAR", (start_box+9, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
    clear_start , clear_end = start_box , start_box + wBox   
    start_box = start_box + wBox + spBox

    # BLUE button
    frame = cv2.rectangle(frame, (start_box,4), (start_box+wBox,65), (255,0,0), 2)
    cv2.putText(frame, "BLUE", (start_box+9, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
    paintWindow = cv2.rectangle(paintWindow, (start_box,4), (start_box+wBox,65), (255,0,0), 2)
    cv2.putText(paintWindow, "BLUE", (start_box+9, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
    blue_start , blue_end = start_box , start_box + wBox
    #cv2.line(frame , (blue_start ,80) , (blue_end , 80),(255,0,0),2)
    #cv2.circle(frame , (track_bar[0] , 80) , 4 , (0,0,0) , -4)
    start_box = start_box + wBox + spBox

    # GREEN button
    frame = cv2.rectangle(frame, (start_box,4), (start_box+wBox,65), (0,255,0), 2)
    cv2.putText(frame, "GREEN", (start_box+9, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    paintWindow = cv2.rectangle(paintWindow, (start_box,4), (start_box+wBox,65), (0,255,0), 2)
    cv2.putText(paintWindow, "GREEN", (start_box+9, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    green_start , green_end = start_box , start_box + wBox
    #cv2.line(frame , (green_start ,80) , (green_end , 80),(0,255,0),2)
    #cv2.circle(frame , (track_bar[1] , 80) , 4 , (0,0,0) , -4)
    start_box = start_box + wBox + spBox

    # RED button
    frame = cv2.rectangle(frame, (start_box,4), (start_box+wBox,65), (0,0,255), 2)
    cv2.putText(frame, "RED", (start_box+9, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
    paintWindow = cv2.rectangle(paintWindow, (start_box,4), (start_box+wBox,65), (0,0,255), 2)
    cv2.putText(paintWindow, "RED", (start_box+9, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
    red_start , red_end = start_box , start_box + wBox
    #cv2.line(frame , (red_start ,80) , (red_end , 80),(0,0,255),2)
    #cv2.circle(frame , (track_bar[2] , 80) , 4 , (0,0,0) , -4)
    start_box = start_box + wBox + spBox

    # YELLOW button
    frame = cv2.rectangle(frame, (start_box,4), (start_box+wBox+20,65), (0,255,255), 2)
    cv2.putText(frame, "YELLOW", (start_box+9, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
    paintWindow = cv2.rectangle(paintWindow, (start_box,4), (start_box+wBox+20,65), (0,255,255), 2)
    cv2.putText(paintWindow, "YELLOW", (start_box+9, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
    yellow_start , yellow_end = start_box , start_box + wBox
    start_box = start_box + wBox + spBox

    #circle button
    frame = cv2.circle(frame, (start_box+40,40) , 25 ,(0,0,0),2)
    paintWindow = cv2.circle(paintWindow, (start_box+40,40) , 25 ,(0,0,0),2)
    circle_st , circle_end = start_box , start_box+50
    start_box = start_box + 70

    ## rectangle button
    rec_width = 50
    frame = cv2.rectangle(frame, (start_box,6), (start_box+rec_width,65), (0,0,0), 2)
    paintWindow = cv2.rectangle(paintWindow, (start_box,6), (start_box+rec_width,65), (0,0,0), 2)
    quadri_start , quadri_end = start_box , start_box+rec_width
    start_box = start_box + rec_width +10
    

    ##triangle
    p1 = [start_box , 65]
    p2 = [start_box+80 , 65]
    tri_start , tri_end = p1[0] , p2[0]
    tri_height = int((np.sqrt(3)/4)*(p2[0] - p1[0]))
    #print("*************",tri_height)
    p3 = [start_box+(p2[0] - p1[0])//2 , 75 - tri_height]
    triangle_pts = np.array([p1,p2,p3],np.int32)
    triangle_pts = triangle_pts.reshape((-1,1,2))
    frame = cv2.polylines(frame , [triangle_pts],isClosed=True , color=(0,0,0),thickness=2 , lineType=cv2.LINE_AA)
    paintWindow = cv2.polylines(paintWindow , [triangle_pts],isClosed=True , color=(0,0,0),thickness=2 ,lineType=cv2.LINE_AA)

    #line button
    frame = cv2.rectangle(frame, (tri_end+15,4), (tri_end+80,65), (0,0,0), 2)
    paintWindow = cv2.rectangle(paintWindow, (tri_end+15,4), (tri_end+80,65), (0,0,0), 2)
    frame = cv2.line(frame , (tri_end+30,30) , (tri_end+80-10,30) , (0,0,0) , 2,cv2.LINE_AA)
    paintWindow = cv2.line(paintWindow , (tri_end+30,30) , (tri_end+80-10,30) , (0,0,0) , 2,cv2.LINE_AA)
    line_start , line_end = tri_end+20 ,tri_end+80

    # rhombus 
    rhm2 = np.array([line_end+15 , 35])
    rhm4 = np.array([rhm2[0]+70 , 35]) 

    #calculate rhm0 & rhm2
    rhm1 = np.array([(rhm2[0]+rhm4[0])//2, rhm2[1]-(rhm4[0]-rhm2[0])//2])
    rhm3 = np.array([(rhm2[0]+rhm4[0])//2, rhm2[1]+(rhm4[0]-rhm2[0])//2])
    rhombus_pts = np.array([rhm1,rhm2,rhm3,rhm4],np.int32)
    rhombus_pts = rhombus_pts.reshape((-1,1,2))
    frame = cv2.polylines(frame , [rhombus_pts] , True , (0,0,0) , 2)
    paintWindow = cv2.polylines(paintWindow , [rhombus_pts] , True , (0,0,0) , 2)

    ### ellipse button
    center_coordinates = (rhm4[0]+80, 35)
    cv2.circle(frame , center_coordinates , 4 , (0,0,0) , -1)
    major_axis_length = 60
    minor_axis_length = 30
    angle = 0
    start_angle = 0
    end_angle = 360
    
    frame = cv2.ellipse(frame, center_coordinates, (major_axis_length, minor_axis_length),
            angle, start_angle, end_angle, (0,0,0), 2) 
    paintWindow = cv2.ellipse(paintWindow, center_coordinates, (major_axis_length, minor_axis_length),
            angle, start_angle, end_angle, (0,0,0), 2)
    ## dividing line
    cv2.line(frame , (0,100) , (1280,100) , (0,0,0) , 2,cv2.LINE_AA)
    cv2.line(paintWindow , (0,100) , (1280,100) , (0,0,0) , 2,cv2.LINE_AA)
    
    ## to keep a track of the color boxes indices
    return [clear_start , clear_end , blue_start , blue_end , green_start , green_end , red_start , red_end , yellow_start , yellow_end,circle_st , circle_end ,quadri_start , quadri_end , tri_start , tri_end , line_start , line_end ,rhm2[0] ,rhm4[0] , center_coordinates[0]-60 , center_coordinates[0]+60]