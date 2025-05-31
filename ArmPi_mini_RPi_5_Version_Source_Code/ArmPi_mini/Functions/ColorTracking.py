#!/usr/bin/python3
# coding=utf8
import sys
sys.path.append('/home/pi/ArmPi_mini/')
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

# 目标追踪

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

# 实例化逆运动学库
AK = ArmIK()

range_rgb = {
    'red': (0, 0, 255),
    'blue': (255, 0, 0),
    'green': (0, 255, 0),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
}

# 读取颜色阈值文件
lab_data = None
def load_config():
    global lab_data, servo_data
    
    lab_data = yaml_handle.get_yaml_data(yaml_handle.lab_file_path)

__target_color = ('red',)
# 设置检测颜色
def setTargetColor(target_color):
    global __target_color

    print("COLOR", target_color)
    __target_color = target_color
    return (True, ())

# 找出面积最大的轮廓
# 参数为要比较的轮廓的列表
def getAreaMaxContour(contours):
    contour_area_temp = 0
    contour_area_max = 0
    areaMaxContour = None

    for c in contours:  # 历遍所有轮廓
        contour_area_temp = math.fabs(cv2.contourArea(c))  # 计算轮廓面积
        if contour_area_temp > contour_area_max:
            contour_area_max = contour_area_temp
            if contour_area_temp > 300:  # 只有在面积大于300时，最大面积的轮廓才是有效的，以过滤干扰
                areaMaxContour = c

    return areaMaxContour, contour_area_max  # 返回最大的轮廓

# 夹持器夹取时闭合的角度
servo1 = 1500
x_dis = 1500
y_dis = 6
Z_DIS = 18
z_dis = Z_DIS
x_pid = PID.PID(P=0.26, I=0.05, D=0.008)  # pid初始化
y_pid = PID.PID(P=0.012, I=0, D=0.000)
z_pid = PID.PID(P=0.003, I=0, D=0)

# 初始位置
def initMove():
    Board.setPWMServoPulse(1, servo1-50, 800)
    AK.setPitchRangeMoving((0, y_dis, z_dis), 0,-90, 90, 1500)

# 驱动蜂鸣器,响的时间/秒
def setBuzzer(timer):
    Board.setBuzzer(0)
    Board.setBuzzer(1)
    time.sleep(timer)
    Board.setBuzzer(0)

#设置扩展板的RGB灯颜色使其跟要追踪的颜色一致
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
# 变量重置
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

# app初始化调用
def init():
    print("ColorTracking Init")
    load_config()
    initMove()

# app开始玩法调用
def start():
    global __isRunning
    reset()
    __isRunning = True
    print("ColorTracking Start")

# app停止玩法调用
def stop():
    global _stop 
    global __isRunning
    _stop = True
    __isRunning = False
    set_rgb('None')
    print("ColorTracking Stop")

# app退出玩法调用
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
# 图像处理及追踪控制
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
    #如果检测到某个区域有识别到的物体，则一直检测该区域直到没有为止
    if get_roi and start_pick_up:
        get_roi = False
        frame_gb = getMaskROI(frame_gb, roi, size)    
    
    frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)  # 将图像转换到LAB空间
    
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
                                              lab_data[detect_color]['max'][2]))  #对原图像和掩模进行位运算 
                opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))  # 开运算
                closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))  # 闭运算
                contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # 找出轮廓
                areaMaxContour, area_max = getAreaMaxContour(contours)  # 找出最大轮廓
        if area_max > 500:  # 有找到最大面积
            (center_x, center_y), radius = cv2.minEnclosingCircle(areaMaxContour)  # 获取最小外接圆
            center_x = int(Misc.map(center_x, 0, size[0], 0, img_w))
            center_y = int(Misc.map(center_y, 0, size[1], 0, img_h))
            radius = int(Misc.map(radius, 0, size[0], 0, img_w))     
            
            rect = cv2.minAreaRect(areaMaxContour)
            box = np.int0(cv2.boxPoints(rect))
            cv2.circle(img, (int(center_x), int(center_y)), int(radius), range_rgb[detect_color], 2)
            
            
            if __isRunning:
                # 通过PID算法进行X轴追踪,根据目标的画面像素坐标与画面中心坐标比较进行追踪
                x_pid.SetPoint = img_w / 2.0  # 设定
                x_pid.update(center_x)  # 当前
                dx = x_pid.output
                x_dis += int(dx)  # 输出
                # 两边限位
                x_dis = 500 if x_dis < 500 else x_dis
                x_dis = 2500 if x_dis > 2500 else x_dis
                    
                # 通过PID算法进行Y轴追踪,根据目标的画面像素面积和设定值比较进行追踪
                y_pid.SetPoint = 80  # 设定
                if abs(radius - 80) < 10:
                    radius = 80
                else:
                    if radius > 80:
                        radius = radius * 0.85
                y_pid.update(radius)  # 当前
                dy = y_pid.output
                y_dis += dy  # 输出
                # 机械臂限位
                y_dis = 5.00 if y_dis < 5.00 else y_dis
                y_dis = 10.00 if y_dis > 10.00 else y_dis
                
                # 通过PID算法进行Z轴追踪,根据目标的画面像素坐标与画面中心坐标比较进行追踪
                if abs(center_y - img_h/2.0) < 20:
                    z_pid.SetPoint = center_y
                else:
                    z_pid.SetPoint = img_h / 2.0
                    
                z_pid.update(center_y)
                dy = z_pid.output
                z_dis += dy
                # 机械臂限位
                z_dis = 32.00 if z_dis > 32.00 else z_dis
                z_dis = 10.00 if z_dis < 10.00 else z_dis
                
                target = AK.setPitchRange((0, round(y_dis, 2), round(z_dis, 2)), -90, 90) # 逆运动学求解
                if target: # 如果有解，则按照求出的解驱动舵机
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
