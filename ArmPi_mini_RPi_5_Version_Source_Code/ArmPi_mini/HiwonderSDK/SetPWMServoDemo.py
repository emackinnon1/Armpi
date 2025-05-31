#!/usr/bin/python3
# coding=utf8
import sys
import time
import Board

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

print('''
**********************************************************
********功能:幻尔科技树莓派扩展板，PWM舵机控制例程*********
**********************************************************
----------------------------------------------------------
Official website:http://www.hiwonder.com
Online mall:https://huaner.tmall.com/
----------------------------------------------------------
Tips:
 * 按下Ctrl+C可关闭此次程序运行，若失败请多次尝试！
----------------------------------------------------------
''')
    
if __name__ == '__main__':
    for i in range(3):
        Board.setPWMServoPulse(1, 1500, 1000) # 设置1号PWM舵机运行到1500脉宽处，运行时间1000毫秒
        time.sleep(1) # 延时1秒
        Board.setPWMServoPulse(1, 2500, 1000) # 设置1号PWM舵机运行到2500脉宽处，运行时间1000毫秒
        time.sleep(1) # 延时1秒
        Board.setPWMServoPulse(1, 1500, 1000) # 设置1号舵机运行到1500脉宽处，运行时间1000毫秒 
