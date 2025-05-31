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
********PWM servo control routine*********
**********************************************************
----------------------------------------------------------
Official website:http://www.hiwonder.com
Online mall:https://huaner.tmall.com/
----------------------------------------------------------
Tips:
 * Press Ctrl+C to exit the program. If fail to exit, please try few more times.
----------------------------------------------------------
''')
    
if __name__ == '__main__':
    for i in range(3):
        Board.setPWMServoPulse(1, 1500, 1000) # ID1 servo is set to run to 1500 pulse width, and the running time is 1000ms. 
        time.sleep(1) # delay 0.1s
        Board.setPWMServoPulse(1, 2500, 1000) # ID1 servo is set to run to 2500 pulse width, and the running time is 1000ms. 
        time.sleep(1) # delay 0.1s 
        Board.setPWMServoPulse(1, 1500, 1000) # ID1 servo is set to run to 1500 pulse width, and the running time is 1000ms. 
