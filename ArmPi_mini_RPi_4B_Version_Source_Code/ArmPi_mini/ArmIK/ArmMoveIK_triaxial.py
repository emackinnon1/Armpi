#!/usr/bin/env python3
# encoding:utf-8
import sys
import time
sys.path.append('/home/emackinnon1/Projects/Armpi/ArmPi_mini_RPi_4B_Version_Source_Code//ArmPi_mini/')
from ArmIK.ArmMoveIK import *

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)
    
print('''
**********************************************************
****************Function: Control robot arm to move on XYZ axis********************
**********************************************************
----------------------------------------------------------
Official website:http://www.hiwonder.com
Online mall:https://huaner.tmall.com/
----------------------------------------------------------
Tips:
 * Press Ctrl+C to exit the program. If failt to exit, please try few more times.
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
    # Set the initial position of robot ram as (x:0, y:6, z:18), and the running time as 1500ms.
    AK.setPitchRangeMoving((0, 6, 18), 0,-90, 90, 1500) 
    time.sleep(1.5) # Delay 1.5s
    


    AK.setPitchRangeMoving((5, 6, 18), 0,-90, 90, 1000)  # set the robot arm to move to the right along x axis and the running time to 1000ms
    time.sleep(1.2) # Delay 1.2s
    AK.setPitchRangeMoving((5, 13, 11), 0,-90, 90, 1000) # set robot arm to simutaneously move alone y and z axes and the running time to 1000ms.
    time.sleep(1.2) # Delay 1.2s
    AK.setPitchRangeMoving((-5, 13, 11), 0,-90, 90, 1000) # set the robot arm to move to the right along x axis and the running time to 1000ms
    time.sleep(1.2) # Delay 1.2s
    AK.setPitchRangeMoving((-5, 6, 18), 0,-90, 90, 1000)  # set robot arm to simutaneously move alone y and z axes and the running time to 1000ms.
    time.sleep(1.2) # Delay 1.2s
    AK.setPitchRangeMoving((0, 6, 18), 0,-90, 90, 1000) # set the robot arm to move to the right along x axis and the running time to 1000ms
    time.sleep(1.2) # Delay 1.2s
    
    
    
    
        
    