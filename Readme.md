# Air Canvas using machine learning

## Description

In this project the user can draw in the screen itself on a real time using their hand gestures and finger movements.
If we want to use it on a live meeting or virtual conference we can use this to draw and showcase our thiughts on a real time basis just by using your hand gestures.
We have implemented this project using the mediapipe to track the hand movements of the user and used OpenCV library for implementing the computer vision requirements.
The language used in this project is python.

## Requirements (to be installed in your system):

python3 , numpy , opencv, mediapipe

## file contents

# air_canvas.py

Main file where the project is to start the execution

# Color_boxes.py

Draw the options to make various selections

# Geometry.py

Draw various figures and geometric shapes

## Algorithm

1. Start reading the frames from the webcam of the system
2. Now prepare the frame based on the required conditions and space to draw and options to display and the orientation
3. Initialize mediapipe to read the hand movements
4. Detect the hand landmarks from the RGB frame to the mediapipe hand detector
5. Only draw using the hand selected by the user at the starting to avoid any kind of mishaps
6. Set the conditions when the user decides to skip the draw and move to other part of the window to draw over there
7. Store the points where the drawing conditions are satisfied in an array
8. Draw the points on the frame
