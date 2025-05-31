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
import HiwonderSDK.PID as PID
import HiwonderSDK.Misc as Misc
import HiwonderSDK.Board as Board

# Target Tracking

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

# Instantiate inverse kinematics library
AK = ArmIK()

range_rgb = {
    'red': (0, 0, 255),
    'blue': (255, 0, 0),
    'green': (0, 255, 0),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
}

# read the color threshold file
lab_data = None
def load_config():
    global lab_data, servo_data
    
    lab_data = yaml_handle.get_yaml_data(yaml_handle.lab_file_path)

__target_color = ('red',)
# set the target color to be detected
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
    areaMaxContour = None

    for c in contours:  # traverse all contours 
        contour_area_temp = math.fabs(cv2.contourArea(c))  # calculate the contour area
        if contour_area_temp > contour_area_max:
            contour_area_max = contour_area_temp
            if contour_area_temp > 300:  # Only when the area is greater than 300, the largest area will take effect to filter the interference
                areaMaxContour = c

    return areaMaxContour, contour_area_max  # return the largest contour

# the closing angle of the gripper 
servo1 = 1500
x_dis = 1500
y_dis = 6
Z_DIS = 18
z_dis = Z_DIS
x_pid = PID.PID(P=0.26, I=0.05, D=0.008)  # pid initialization
y_pid = PID.PID(P=0.012, I=0, D=0.000)
z_pid = PID.PID(P=0.003, I=0, D=0)

# Initial position 
def initMove():
    Board.setPWMServoPulse(1, servo1-50, 800)
    AK.setPitchRangeMoving((0, y_dis, z_dis), 0,-90, 90, 1500)

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
track = False
_stop = False
get_roi = False
center_list = []
__isRunning = False
detect_color = 'None'
action_finish = True
start_pick_up = False
start_count_t1 = True
# Reset variable
def reset():
    global count
    global track
    global _stop
    global get_roi
    global center_list
    global __isRunning
    global detect_color
    global action_finish
    global start_pick_up
    global __target_color
    global start_count_t1
    global x_dis,z_dis
    
    x_dis = 1500
    y_dis = 6
    z_dis = 18
    count = 0
    _stop = False
    track = False
    get_roi = False
    center_list = []
    __target_color = ()
    detect_color = 'None'
    action_finish = True
    start_pick_up = False
    start_count_t1 = True

# Initialization
def init():
    print("ColorTracking Init")
    load_config()
    initMove()

# start game in app
def start():
    global __isRunning
    reset()
    __isRunning = True
    print("ColorTracking Start")

# stop game in app
def stop():
    global _stop 
    global __isRunning
    _stop = True
    __isRunning = False
    set_rgb('None')
    print("ColorTracking Stop")

# exit game in app
def exit():
    global _stop
    global __isRunning
    _stop = True
    __isRunning = False
    set_rgb('None')
    print("ColorTracking Exit")

rect = None
size = (320, 240)
rotation_angle = 0
unreachable = False


t1 = 0
roi = ()
# image processing and tracking control
def run(img):
    global roi
    global rect
    global count
    global track
    global get_roi
    global center_list
    global __isRunning
    global unreachable
    global detect_color
    global action_finish
    global rotation_angle
    global start_count_t1, t1
    global start_pick_up
    global img_h, img_w
    global x_dis, y_dis, z_dis
    
    img_copy = img.copy()
    img_h, img_w = img.shape[:2]
    
    if not __isRunning:
        return img
     
    frame_resize = cv2.resize(img_copy, size, interpolation=cv2.INTER_NEAREST)
    frame_gb = cv2.GaussianBlur(frame_resize, (3, 3), 3)
    #If an area is detected with a recognized object, the area is detected until there are none
    if get_roi and start_pick_up:
        get_roi = False
        frame_gb = getMaskROI(frame_gb, roi, size)    
    
    frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)  # Convert the image into LAB space
    
    area_max = 0
    areaMaxContour = 0
    if not start_pick_up:
        for i in lab_data:
            if i in __target_color:
                detect_color = i
                frame_mask = cv2.inRange(frame_lab,
                                             (lab_data[detect_color]['min'][0],
                                              lab_data[detect_color]['min'][1],
                                              lab_data[detect_color]['min'][2]),
                                             (lab_data[detect_color]['max'][0],
                                              lab_data[detect_color]['max'][1],
                                              lab_data[detect_color]['max'][2]))  # Perform bitwise operations on the original image and mask
                opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))  # Opening
                closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))  # Closing
                contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # Find contour
                areaMaxContour, area_max = getAreaMaxContour(contours)  # Find the largest contour
        if area_max > 500:  # Find the largest area
            (center_x, center_y), radius = cv2.minEnclosingCircle(areaMaxContour)  # Get the minimum enclosing circle
            center_x = int(Misc.map(center_x, 0, size[0], 0, img_w))
            center_y = int(Misc.map(center_y, 0, size[1], 0, img_h))
            radius = int(Misc.map(radius, 0, size[0], 0, img_w))     
            
            rect = cv2.minAreaRect(areaMaxContour)
            box = np.int0(cv2.boxPoints(rect))
            cv2.circle(img, (int(center_x), int(center_y)), int(radius), range_rgb[detect_color], 2)
            
            
            if __isRunning:
                # Use PID algorithm to track x axis based on the comparison of the screen pixel coordinates of the target with the screen center coordinates
                x_pid.SetPoint = img_w / 2.0  # set
                x_pid.update(center_x)  # current 
                dx = x_pid.output
                x_dis += int(dx)  # output
                # Limit on both sides
                x_dis = 500 if x_dis < 500 else x_dis
                x_dis = 2500 if x_dis > 2500 else x_dis
                    
                # Use PID algorithm to track y axis based on the comparison of the screen pixel area of the target with the set value.
                y_pid.SetPoint = 80  # set
                if abs(radius - 80) < 10:
                    radius = 80
                else:
                    if radius > 80:
                        radius = radius * 0.85
                y_pid.update(radius)  # current 
                dy = y_pid.output
                y_dis += dy  # output
                # the limit of robot arm
                y_dis = 5.00 if y_dis < 5.00 else y_dis
                y_dis = 10.00 if y_dis > 10.00 else y_dis
                
                # Use PID algorithm to track y axis based on the comparison of the screen pixel area of the target with the set value.
                if abs(center_y - img_h/2.0) < 20:
                    z_pid.SetPoint = center_y
                else:
                    z_pid.SetPoint = img_h / 2.0
                    
                z_pid.update(center_y)
                dy = z_pid.output
                z_dis += dy
                # the limit of robot arm
                z_dis = 32.00 if z_dis > 32.00 else z_dis
                z_dis = 10.00 if z_dis < 10.00 else z_dis
                
                target = AK.setPitchRange((0, round(y_dis, 2), round(z_dis, 2)), -90, 90) # use inverse kinematics to get solution
                if target: # If there is a solution, drive the servo according to the requirement
                    servo_data = target[0]                  
                    Board.setPWMServosPulse([20, 4, 3,servo_data['servo3'], 4,servo_data['servo4'], 5,servo_data['servo5'], 6,int(x_dis)])
                    
    return img

if __name__ == '__main__':
    init()
    start()
    __isRunning = True
    __target_color = ('red')
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
