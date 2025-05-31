#!/usr/bin/python3
# coding=utf8
import sys
sys.path.append('/home/emackinnon1/Projects/Armpi/ArmPi_mini_RPi_4B_Version_Source_Code/ArmPi_mini/')
import cv2
import time
import math
import Camera
import threading
import yaml_handle
from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board
import HiwonderSDK.Misc as Misc

# Intelligent stacking

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

# Instantiate inverse kinematics libaray
AK = ArmIK()

# Read the coordinate of the picking position
Coordinates_data = yaml_handle.get_yaml_data(yaml_handle.PickingCoordinates_file_path)

range_rgb = {
    'red': (0, 0, 255),
    'blue': (255, 0, 0),
    'green': (0, 255, 0),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
}

# Read the color threshold file
lab_data = None
def load_config():
    global lab_data, servo_data
    
    lab_data = yaml_handle.get_yaml_data(yaml_handle.lab_file_path)

# Set the target color 
__target_color = ('red', 'green', 'blue')
def setTargetColor(target_color):
    global __target_color

    print("COLOR", target_color)
    __target_color = target_color
    return (True, ())

# Find the largest contour
# The parameters are the list of the contour to be compared
def getAreaMaxContour(contours):
    contour_area_temp = 0
    contour_area_max = 0
    area_max_contour = None

    for c in contours:  # traverse all contours 
        contour_area_temp = math.fabs(cv2.contourArea(c))  # calculate the contour area
        if contour_area_temp > contour_area_max:
            contour_area_max = contour_area_temp
            if contour_area_temp > 300:  # Only when the area is greater than 300, the largest area will take effect to filter the interference
                area_max_contour = c

    return area_max_contour, contour_area_max  # return the largest contour

# the closing angle of the gripper 
servo1 = 1500

# Initial position
def initMove():
    Board.setPWMServoPulse(1, servo1 - 50, 300)
    AK.setPitchRangeMoving((0, 8, 10), -90,-90, 90, 1500)

# Drive buzzer, the duration of sounding 
def setBuzzer(timer):
    Board.setBuzzer(0)
    Board.setBuzzer(1)
    time.sleep(timer)
    Board.setBuzzer(0)
   

# The tracked color is set to consistent with the color of RGB light on expansion board.
def set_rgb(color):
    if color == "red":
        Board.RGB.setPixelColor(0, Board.PixelColor(255, 0, 0))
        Board.RGB.setPixelColor(1, Board.PixelColor(255, 0, 0))
        Board.RGB.show()
    elif color == "green":
        Board.RGB.setPixelColor(0, Board.PixelColor(0, 255, 0))
        Board.RGB.setPixelColor(1, Board.PixelColor(0, 255, 0))
        Board.RGB.show()
    elif color == "blue":
        Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 255))
        Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 255))
        Board.RGB.show()
    else:
        Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))
        Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 0))
        Board.RGB.show()

count = 0
_stop = False
color_list = []
get_roi = False
__isRunning = False
detect_color = 'None'
start_pick_up = False
start_count_t1 = True

# Reset variable
def reset(): 
    global _stop
    global count
    global get_roi
    global color_list
    global detect_color
    global start_pick_up
    global start_count_t1
    
    count = 0
    _stop = False
    color_list = []
    get_roi = False
    detect_color = 'None'
    start_pick_up = False
    start_count_t1 = True

# Initialization
def init():
    global number
    number = 0
    print("ColorPalletizing Init")
    load_config()
    initMove()

# start game in app
def start():
    global __isRunning
    reset()
    __isRunning = True
    print("ColorPalletizing Start")

# stop game in app
def stop():
    global _stop
    global __isRunning
    _stop = True
    __isRunning = False
    set_rgb('None')
    print("ColorPalletizing Stop")

# exit game in app
def exit():
    global _stop
    global __isRunning
    _stop = True
    __isRunning = False
    set_rgb('None')
    print("ColorPalletizing Exit")

rect = None
size = (320, 240)
rotation_angle = 0
unreachable = False
world_X, world_Y = 0, 0
# robot arm movement function
def move():
    global rect
    global _stop
    global get_roi
    global number
    global __isRunning
    global unreachable
    global detect_color
    global start_pick_up
    global rotation_angle
    global world_X, world_Y
    
    x = Coordinates_data['X']
    y = Coordinates_data['Y']
    z = Coordinates_data['Z']
    
    coordinate = {
        'capture': (x, y, z),       # the picking coordinate 
        'place': (11, 0, 0.5), # the placement coordinate
        }
    
    while True:
        if __isRunning:
            if detect_color != 'None' and start_pick_up:  # After the detected block does not move for a while, start girpping.
                set_rgb(detect_color) # The RGB light of expansion board is set to light up corresponding color
                setBuzzer(0.1) # The buzzer sounds for 0.1s
                
                Board.setPWMServoPulse(1, 2000, 500) # the gripper opens
                time.sleep(0.6)
                if not __isRunning: # detect whether to stop game
                    continue
                AK.setPitchRangeMoving((coordinate['capture']), -90,-90, 90, 1000) # Robot arm moves to the pickig position
                time.sleep(1) # delay 0.1s
                if not __isRunning:
                    continue
                Board.setPWMServoPulse(1, 1550, 500) # the gripper closes 
                time.sleep(0.6)
                if not __isRunning:
                    continue
                AK.setPitchRangeMoving((0, 6, 18), 0,-90, 90, 1500) # the robot arm raises up
                time.sleep(1.5)
                if not __isRunning:
                    continue
                Board.setPWMServoPulse(6, 500, 1500) # robot arm rotates
                time.sleep(1.5)
                if not __isRunning:
                    continue
                if not __isRunning:
                    continue
                AK.setPitchRangeMoving((coordinate['place'][0], coordinate['place'][1],12), -90,-90, 90, 800) # Robot arm moves above the gripping position
                time.sleep(0.8)
                if not __isRunning:
                    continue
                
                AK.setPitchRangeMoving((coordinate['place'][0], coordinate['place'][1],(coordinate['place'][2]+number*3)), -90,-90, 90, 800) # Robot arm moves to the placement position and calculate the height of the placement coordinate based on the number of the blocks
                time.sleep(0.8)
                if not __isRunning: 
                    continue
                Board.setPWMServoPulse(1, 1800, 500) # the gripper opens and put down the block
                time.sleep(0.6)
                if not __isRunning:
                    continue
                AK.setPitchRangeMoving((6, 0, 18), 0,-90, 90, 1500) # the robot arm raises up
                time.sleep(1.5)
                if not __isRunning:
                    continue
                Board.setPWMServoPulse(6, 1500, 1500) # the robot arm turns to the middle position
                time.sleep(1.5)
                
                if not __isRunning:
                    continue
                AK.setPitchRangeMoving((0, 8, 10), -90,-90, 90, 800) # Robot arm returns to the initial position
                time.sleep(0.8)
                 
                number += 1 # Block Quantity Accumulation
                if number == 3: # If it equals to 3, reset the calculation.
                    number = 0
                    setBuzzer(0.1)
                    set_rgb('white')
                    time.sleep(0.5)
                    
                if not __isRunning:
                    continue
                # reset the corresponding variable
                detect_color = 'None'
                get_roi = False
                start_pick_up = False
                set_rgb(detect_color)
            else:
                time.sleep(0.01)
        else:
            if _stop:
                _stop = False
                initMove()  # back to the initial position
            time.sleep(0.01)

# run the child thread 
th = threading.Thread(target=move)
th.setDaemon(True)
th.start()

t1 = 0
roi = ()
center_list = []
last_x, last_y = 0, 0
draw_color = range_rgb["black"]
# Image processing
def run(img):
    global roi
    global rect
    global count
    global get_roi
    global center_list
    global unreachable
    global __isRunning
    global start_pick_up
    global last_x, last_y
    global rotation_angle
    global world_X, world_Y
    global start_count_t1, t1
    global detect_color, draw_color, color_list
    
    if not __isRunning:
        return img
    else:
        img_copy = img.copy()
        img_h, img_w = img.shape[:2]

        frame_resize = cv2.resize(img_copy, size, interpolation=cv2.INTER_NEAREST)
        frame_gb = cv2.GaussianBlur(frame_resize, (3, 3), 3)
        
        frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)  # Convert the image into LAB space

        color_area_max = None
        max_area = 0
        areaMaxContour_max = 0
        if not start_pick_up:
            for i in lab_data:
                if i in __target_color:
                    frame_mask = cv2.inRange(frame_lab,
                                                 (lab_data[i]['min'][0],
                                                  lab_data[i]['min'][1],
                                                  lab_data[i]['min'][2]),
                                                 (lab_data[i]['max'][0],
                                                  lab_data[i]['max'][1],
                                                  lab_data[i]['max'][2]))  #Perform bitwise operations on the original image and mask
                    opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))  # Opening
                    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))  # Closing
                    closed[0:80, :] = 0
                    closed[:, 0:120] = 0
                    contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # Find contour
                    areaMaxContour, area_max = getAreaMaxContour(contours)  # Find the largest contour
                    if areaMaxContour is not None:
                        if area_max > max_area:  # Find the largest area
                            max_area = area_max
                            color_area_max = i
                            areaMaxContour_max = areaMaxContour
            if max_area > 500:  # Have found the maximum area
                (center_x, center_y), radius = cv2.minEnclosingCircle(areaMaxContour_max)  # Get the minimum enclosing circle
                center_x = int(Misc.map(center_x, 0, size[0], 0, img_w))
                center_y = int(Misc.map(center_y, 0, size[1], 0, img_h))
                radius = int(Misc.map(radius, 0, size[0], 0, img_w))
                cv2.circle(img, (int(center_x), int(center_y)), int(radius), range_rgb[color_area_max], 2)
                
                if not start_pick_up:
                    if color_area_max == 'red':  # red is the largeat area
                        color = 1
                    elif color_area_max == 'green':  # green is the largeat area
                        color = 2
                    elif color_area_max == 'blue':  # blue is the largeat area
                        color = 3
                    else:
                        color = 0
                    color_list.append(color)
                    if len(color_list) == 3:  # Determine mutiple time
                        # take the average
                        color = int(round(np.mean(np.array(color_list))))
                        color_list = []
                        if color == 1:
                            detect_color = 'red'
                            draw_color = range_rgb["red"]
                            start_pick_up = True
                        elif color == 2:
                            detect_color = 'green'
                            draw_color = range_rgb["green"]
                            start_pick_up = True
                        elif color == 3:
                            start_pick_up = True
                            detect_color = 'blue'
                            draw_color = range_rgb["blue"]
                        else:
                            start_pick_up = False
                            detect_color = 'None'
                            draw_color = range_rgb["black"]
            else:
                if not start_pick_up:
                    draw_color = (0, 0, 0)
                    detect_color = "None"
                 
        cv2.putText(img, "Color: " + detect_color, (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, draw_color, 2)
        
        return img

if __name__ == '__main__':
    init()
    start()
    __target_color = ('red', 'green', 'blue')
    cap = cv2.VideoCapture('http://127.0.0.1:8080?action=stream')
    while True:
        ret,img = cap.read()
        if ret:
            frame = img.copy()
            Frame = run(frame)  
            frame_resize = cv2.resize(Frame, (320, 240))
            cv2.imshow('frame', frame_resize)
            key = cv2.waitKey(1)
            if key == 27:
                break
        else:
            time.sleep(0.01)
    cv2.destroyAllWindows()
