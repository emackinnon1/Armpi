#!/usr/bin/env python3
# encoding:utf-8
import sys
import time
sys.path.append('/home/emackinnon1/Projects/Armpi/ArmPi_mini_RPi_4B_Version_Source_Code/ArmPi_mini/')
from ArmIK.ArmMoveIK import *

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)
    
print('''
**********************************************************
****************Function: Inverse kinematics controls robot arm to move up and down********************
**********************************************************
----------------------------------------------------------
Official website:http://www.hiwonder.com
Online mall:https://huaner.tmall.com/
----------------------------------------------------------
Tips:
 * Press Ctrl+C to exit the program. If fail to close, please try multiple times.
----------------------------------------------------------
''')

# Instantiate inverse kinematics library
AK = ArmIK()
 
if __name__ == "__main__":
    '''
    AK.setPitchRangeMoving(coordinate_data, alpha, alpha1, alpha2, movetime):
    Given the coordinate_data (coordinate), alpha (angle), alpha1，alpha2 (pitch angle), automatically find the solution closest to the given pictch angle, and move to the target position.
    If no solution, return False. Otherwise, return the corresponding servo angle, pitch angle and running time.
    The coordinate unit is cm and inported in the form of tuple, for example (0, 5, 10).
    alpha: the given picth angle 
    alpha1 and alpha2: the range of the pitch angle
    movetime is the rotation time of servo and the unit is ms. if the time is not given, it will be calculated  automatically.   
    '''
    AK.setPitchRangeMoving((0, 6, 18), 0,-90, 90, 1500) # Set the initial position of robot ram as (x:0, y:6, z:18), and the running time as 1500ms.
    time.sleep(1.5) # Delay 1.5s
    
    for i in range(6): # Run for cycle two times 
        AK.setPitchRangeMoving((0, 6, 22), 0,-90, 90, 1000) # The robot arm is set to move up to the position (x:0, y:6, z:22) and the running time is set as 1000ms 
        time.sleep(1.2) # Delay 1.2s 
        
        AK.setPitchRangeMoving((0, 6, 18), 0,-90, 90, 1000) # The robot arm is set to move down to the initial poition and the running time is set as 1000ms
        time.sleep(1.2) # Delay 1.2s 
    