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
********Funtion: Buzzer Control Routine*********
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
    Board.setBuzzer(0) # close 
    time.sleep(0.1) # delay 0.1s 
    Board.setBuzzer(1) # open 
    time.sleep(0.1) # delay 0.1s
    Board.setBuzzer(0) #close

    time.sleep(1) # delay 0.1s

    Board.setBuzzer(1)
    time.sleep(0.5)
    Board.setBuzzer(0)
