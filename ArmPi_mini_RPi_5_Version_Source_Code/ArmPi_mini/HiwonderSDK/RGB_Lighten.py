#!/usr/bin/python3
# coding=utf8
import sys
import time
import Board
import signal

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

print('''
**********************************************************
***********功能:幻尔科技树莓派扩展板，RGB灯控制例程************
**********************************************************
----------------------------------------------------------
Official website:http://www.hiwonder.com
Online mall:https://huaner.tmall.com/
----------------------------------------------------------
Tips:
 * 按下Ctrl+C可关闭此次程序运行，若失败请多次尝试！
----------------------------------------------------------
''')

start = True
#关闭前处理函数
def stop(signum, frame):
    global start

    start = False
    print('关闭中...')

if __name__ == '__main__':

    #先将所有灯关闭
    Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))
    Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 0))
    Board.RGB.show()

    signal.signal(signal.SIGINT, stop) # 设置关闭前处理

    while True:
        #设置2个灯为红色
        Board.RGB.setPixelColor(0, Board.PixelColor(255, 0, 0))
        Board.RGB.setPixelColor(1, Board.PixelColor(255, 0, 0))
        Board.RGB.show()
        time.sleep(1) # 延时1秒
        
        if not start:
            #所有灯关闭
            Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))
            Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 0))
            Board.RGB.show()
            print('已关闭')
            break
