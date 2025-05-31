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
***********RGB light control routine************
**********************************************************
----------------------------------------------------------
Official website:http://www.hiwonder.com
Online mall:https://huaner.tmall.com/
----------------------------------------------------------
Tips:
 * Press Ctrl+C to exit the program. If fail to exit, please try few more times.
----------------------------------------------------------
''')

start = True
#Process function before closing
def stop(signum, frame):
    global start

    start = False
    print('closing...')

if __name__ == '__main__':

    #Turn off all lights
    Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))
    Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 0))
    Board.RGB.show()

    signal.signal(signal.SIGINT, stop) # set a processing before closing

    while True:
        #set two lights as red
        Board.RGB.setPixelColor(0, Board.PixelColor(255, 0, 0))
        Board.RGB.setPixelColor(1, Board.PixelColor(255, 0, 0))
        Board.RGB.show()
        time.sleep(1) # delay 0.1s
        
        #set two lights as green 
        Board.RGB.setPixelColor(0, Board.PixelColor(0, 255, 0))
        Board.RGB.setPixelColor(1, Board.PixelColor(0, 255, 0))
        Board.RGB.show()
        time.sleep(1)
        
        #set two lights as blue
        Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 255))
        Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 255))
        Board.RGB.show()
        time.sleep(1) 
        
        if not start:
            #turn off all lights
            Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))
            Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 0))
            Board.RGB.show()
            print('closed')
            break
