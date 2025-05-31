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
import HiwonderSDK.Board as Board
import HiwonderSDK.Misc as Misc

# 智能码垛

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

# 实例化逆运动学库
AK = ArmIK()

# 读取夹取坐标
Coordinates_data = yaml_handle.get_yaml_data(yaml_handle.PickingCoordinates_file_path)

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

# 设置检测的目标颜色
__target_color = ('red', 'green', 'blue')
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
    area_max_contour = None

    for c in contours:  # 历遍所有轮廓
        contour_area_temp = math.fabs(cv2.contourArea(c))  # 计算轮廓面积
        if contour_area_temp > contour_area_max:
            contour_area_max = contour_area_temp
            if contour_area_temp > 300:  # 只有在面积大于300时，最大面积的轮廓才是有效的，以过滤干扰
                area_max_contour = c

    return area_max_contour, contour_area_max  # 返回最大的轮廓

# 夹持器夹取时闭合的角度
servo1 = 1500

# 初始位置
def initMove():
    Board.setPWMServoPulse(1, servo1 - 50, 300)
    AK.setPitchRangeMoving((0, 8, 10), -90,-90, 90, 1500)

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
_stop = False
color_list = []
get_roi = False
__isRunning = False
detect_color = 'None'
start_pick_up = False
start_count_t1 = True

# 变量重置
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

# 初始化
def init():
    global number
    number = 0
    print("ColorPalletizing Init")
    load_config()
    initMove()

# APP开启玩法
def start():
    global __isRunning
    reset()
    __isRunning = True
    print("ColorPalletizing Start")

# APP关闭玩法
def stop():
    global _stop
    global __isRunning
    _stop = True
    __isRunning = False
    set_rgb('None')
    print("ColorPalletizing Stop")

# APP退出玩法
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
# 机械臂移动函数
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
        'capture': (x, y, z),       # 夹取坐标
        'place': (11, 0, 0.5), # 放置坐标
        }
    
    while True:
        if __isRunning:
            if detect_color != 'None' and start_pick_up:  # 如果检测到方块没有移动一段时间后，开始夹取
                set_rgb(detect_color) # 设置扩展板上的RGB灯亮对应的颜色
                setBuzzer(0.1) # 蜂鸣器响0.1秒
                
                Board.setPWMServoPulse(1, 2000, 500) # 张开爪子
                time.sleep(0.6)
                if not __isRunning: # 检测是否停止玩法
                    continue
                AK.setPitchRangeMoving((coordinate['capture']), -90,-90, 90, 1000) # 机械臂运行到夹取位置
                time.sleep(1) # 延时1秒
                if not __isRunning:
                    continue
                Board.setPWMServoPulse(1, 1550, 500) # 闭合爪子
                time.sleep(0.6)
                if not __isRunning:
                    continue
                AK.setPitchRangeMoving((0, 6, 18), 0,-90, 90, 1500) # 抬起机械臂
                time.sleep(1.5)
                if not __isRunning:
                    continue
                Board.setPWMServoPulse(6, 500, 1500) # 先把机械臂转过去
                time.sleep(1.5)
                if not __isRunning:
                    continue
                if not __isRunning:
                    continue
                AK.setPitchRangeMoving((coordinate['place'][0], coordinate['place'][1],12), -90,-90, 90, 800) # 机械臂运行到夹取位置上方
                time.sleep(0.8)
                if not __isRunning:
                    continue
                
                AK.setPitchRangeMoving((coordinate['place'][0], coordinate['place'][1],(coordinate['place'][2]+number*3)), -90,-90, 90, 800) # 机械臂运行到放置位置,根据码垛的数量计算放置坐标的高度
                time.sleep(0.8)
                if not __isRunning: 
                    continue
                Board.setPWMServoPulse(1, 1800, 500) # 张开爪子,放下木块
                time.sleep(0.6)
                if not __isRunning:
                    continue
                AK.setPitchRangeMoving((6, 0, 18), 0,-90, 90, 1500) # 抬起机械臂
                time.sleep(1.5)
                if not __isRunning:
                    continue
                Board.setPWMServoPulse(6, 1500, 1500) # 机械臂转回中间
                time.sleep(1.5)
                
                if not __isRunning:
                    continue
                AK.setPitchRangeMoving((0, 8, 10), -90,-90, 90, 800) # 机械臂复位
                time.sleep(0.8)
                 
                number += 1 # 码垛数量累加
                if number == 3: # 如果等于3，进行计数重置
                    number = 0
                    setBuzzer(0.1)
                    set_rgb('white')
                    time.sleep(0.5)
                    
                if not __isRunning:
                    continue
                # 对应变量进行重置
                detect_color = 'None'
                get_roi = False
                start_pick_up = False
                set_rgb(detect_color)
            else:
                time.sleep(0.01)
        else:
            if _stop:
                _stop = False
                initMove()  # 回到初始位置  
            time.sleep(0.01)

# 运行子线程
th = threading.Thread(target=move)
th.setDaemon(True)
th.start()

t1 = 0
roi = ()
center_list = []
last_x, last_y = 0, 0
draw_color = range_rgb["black"]
# 图像处理
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
        
        frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)  # 将图像转换到LAB空间

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
                                                  lab_data[i]['max'][2]))  #对原图像和掩模进行位运算
                    opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))  # 开运算
                    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))  # 闭运算
                    closed[0:80, :] = 0
                    closed[:, 0:120] = 0
                    contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # 找出轮廓
                    areaMaxContour, area_max = getAreaMaxContour(contours)  # 找出最大轮廓
                    if areaMaxContour is not None:
                        if area_max > max_area:  # 找最大面积
                            max_area = area_max
                            color_area_max = i
                            areaMaxContour_max = areaMaxContour
            if max_area > 500:  # 有找到最大面积
                (center_x, center_y), radius = cv2.minEnclosingCircle(areaMaxContour_max)  # 获取最小外接圆
                center_x = int(Misc.map(center_x, 0, size[0], 0, img_w))
                center_y = int(Misc.map(center_y, 0, size[1], 0, img_h))
                radius = int(Misc.map(radius, 0, size[0], 0, img_w))
                cv2.circle(img, (int(center_x), int(center_y)), int(radius), range_rgb[color_area_max], 2)
                
                if not start_pick_up:
                    if color_area_max == 'red':  # 红色最大
                        color = 1
                    elif color_area_max == 'green':  # 绿色最大
                        color = 2
                    elif color_area_max == 'blue':  # 蓝色最大
                        color = 3
                    else:
                        color = 0
                    color_list.append(color)
                    if len(color_list) == 3:  # 多次判断
                        # 取平均值
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
