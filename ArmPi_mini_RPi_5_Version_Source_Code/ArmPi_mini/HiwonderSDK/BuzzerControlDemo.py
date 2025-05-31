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
********功能:幻尔科技树莓派扩展板，蜂鸣器控制例程*********
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
    Board.setBuzzer(0) # 关闭
    time.sleep(0.1) # 延时0.1秒
    Board.setBuzzer(1) # 打开
    time.sleep(0.1) # 延时0.1秒
    Board.setBuzzer(0) #关闭

    time.sleep(1) # 延时1秒

    Board.setBuzzer(1)
    time.sleep(0.5)
    Board.setBuzzer(0)
