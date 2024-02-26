import cv2

def color_boxes (frame):
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

    ## to keep a track of the color boxes indices
    return [clear_start , clear_end , blue_start , blue_end , green_start , green_end , red_start , red_end , yellow_start , yellow_end]