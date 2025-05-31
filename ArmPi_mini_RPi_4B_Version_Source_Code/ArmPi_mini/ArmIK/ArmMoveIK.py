#!/usr/bin/env python3
# encoding:utf-8
import sys
sys.path.append('/home/emackinnon1/Projects/Armpi/ArmPi_mini_RPi_4B_Version_Source_Code/ArmPi_mini/')
import time
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
from ArmIK.InverseKinematics import *
from mpl_toolkits.mplot3d import Axes3D
from HiwonderSDK.Board import getPWMServoPulse, setPWMServosPulse

#Robot arm moves according to the angle calculated by inverse kinematics.
ik = IK()

class ArmIK:
    servo3Range = (500, 2500.0, 0, 180.0) #Pulse width, angle
    servo4Range = (500, 2500.0, 0, 180.0)
    servo5Range = (500, 2500.0, 0, 180.0)
    servo6Range = (500, 2500.0, 0, 180.0)

    def __init__(self):
        self.setServoRange()

    def setServoRange(self, servo3_Range=servo3Range, servo4_Range=servo4Range, servo5_Range=servo5Range, servo6_Range=servo6Range):
        # Compatible with different servo 
        self.servo3Range = servo3_Range
        self.servo4Range = servo4_Range
        self.servo5Range = servo5_Range
        self.servo6Range = servo6_Range
        self.servo3Param = (self.servo3Range[1] - self.servo3Range[0]) / (self.servo3Range[3] - self.servo3Range[2])
        self.servo4Param = (self.servo4Range[1] - self.servo4Range[0]) / (self.servo4Range[3] - self.servo4Range[2])
        self.servo5Param = (self.servo5Range[1] - self.servo5Range[0]) / (self.servo5Range[3] - self.servo5Range[2])
        self.servo6Param = (self.servo6Range[1] - self.servo6Range[0]) / (self.servo6Range[3] - self.servo6Range[2])

    def transformAngelAdaptArm(self, theta3, theta4, theta5, theta6):
        #Convert the angle calculated by inverse kinematics into the corresponding pulse width of the servo.
        servo3 = int(round(theta3 * self.servo3Param + (self.servo3Range[1] + self.servo3Range[0])/2))
        if servo3 > self.servo3Range[1] or servo3 < self.servo3Range[0]:
            logger.info('servo3(%s)exceed range (%s, %s)', servo3, self.servo3Range[0], self.servo3Range[1])
            return False

        servo4 = int(round(theta4 * self.servo4Param + (self.servo4Range[1] + self.servo4Range[0])/2))
        if servo4 > self.servo4Range[1] or servo4 < self.servo4Range[0]:
            logger.info('servo4(%s)exceed range(%s, %s)', servo4, self.servo4Range[0], self.servo4Range[1])
            return False

        servo5 = int(round((self.servo5Range[1] + self.servo5Range[0])/2 + (90.0 - theta5) * self.servo5Param)) 
        if servo5 > ((self.servo5Range[1] + self.servo5Range[0])/2 + 90*self.servo5Param) or servo5 < ((self.servo5Range[1] + self.servo5Range[0])/2 - 90*self.servo5Param):
            logger.info('servo5(%s)exceed range(%s, %s)', servo5, self.servo5Range[0], self.servo5Range[1])
            return False

        if theta6 < -(self.servo6Range[3] - self.servo6Range[2])/2:
            servo6 = int(round(((self.servo6Range[3] - self.servo6Range[2])/2 + (90 + (180 + theta6))) * self.servo6Param))
        else:
            servo6 = int(round(((self.servo6Range[3] - self.servo6Range[2])/2 - (90 - theta6)) * self.servo6Param)) + self.servo6Range[0]
        if servo6 > self.servo6Range[1] or servo6 < self.servo6Range[0]:
            logger.info('servo6(%s)exceed range(%s, %s)', servo6, self.servo6Range[0], self.servo6Range[1])
            return False
        return {"servo3": servo3, "servo4": servo4, "servo5": servo5, "servo6": servo6}

    def servosMove(self, servos, movetime=None):
        #Drive ID3, ID4, ID5, ID6 servos to rotate
        time.sleep(0.02)
        if movetime is None:
            max_d = 0
            for i in  range(0, 4):
                d = abs(getPWMServoPulse(i + 3) - servos[i])
                if d > max_d:
                    max_d = d
            movetime = int(max_d*1)
        setPWMServosPulse([movetime, 4, 3,servos[0], 4,servos[1], 5,servos[2], 6,servos[3]])

        return movetime

    def setPitchRange(self, coordinate_data, alpha1, alpha2, da = 1):
        #Given the coordinate_data the range of pitch angle alpha1，alpha2, and then automatically find the solution within the range
        #If no solution, return False. Otherwise, return the corresponding servo angle and the pitch angle.
        #The unit of coordinate is cm and input in the form of tuple, for example, (0, 5, 10).
        #ad is the increased pitch angle while travsersing.
        x, y, z = coordinate_data
        if alpha1 >= alpha2:
            da = -da
        for alpha in np.arange(alpha1, alpha2, da):#Get the solution through traversing
            result = ik.getRotationAngle((x, y, z), alpha)
            if result:
                theta3, theta4, theta5, theta6 = result['theta3'], result['theta4'], result['theta5'], result['theta6']               
                servos = self.transformAngelAdaptArm(theta3, theta4, theta5, theta6)
                if servos != False:
                    return servos, alpha

        return False

    def setPitchRanges(self, coordinate_data, alpha, alpha1, alpha2, d = 0.01):
        #Given the coordinate_data the range of pitch angle alpha1，alpha2, and then automatically get the solution.
        #If no solution, return False. Otherwise, return the corresponding servo angle and the pitch angle.
        #The unit of coordinate is cm and input in the form of tuple, for example, (0, 5, 10).
        #alpha is the given pitch angle the unit is degree.
        #alpha is the given pitch angle the unit is degree.
        #The alpha1 and alpha2 is the value range of the picth angle.

        x, y, z = coordinate_data
        a_range = abs(int(abs(alpha1 - alpha2)/d)) + 1
        for i in range(a_range):
            if i % 2:
                alpha_ = alpha + (i + 1)/2*d
            else:                
                alpha_ = alpha - i/2*d
                if alpha_ < alpha1:
                    alpha_ = alpha2 - i/2*d
            result = ik.getRotationAngle((x, y, z), alpha_)
            if result:
                theta3, theta4, theta5, theta6 = result['theta3'], result['theta4'], result['theta5'], result['theta6']
                servos = self.transformAngelAdaptArm(theta3, theta4, theta5, theta6)
                return servos, alpha_
        
        return False
    
    def setPitchRangeMoving(self, coordinate_data, alpha, alpha1, alpha2, movetime = None):
        #Given the coordinate_data (coordinate), alpha (angle), alpha1，alpha2 (pitch angle), automatically find the solution closest to the given pictch angle, and move to the target position.
        #If no solution, return False. Otherwise, return the corresponding servo angle, pitch angle and running time.
        #The unit of coordinate is cm and imported in the form of tuple, for example, (0, 5, 10).
        #alpha is the given pitch angle the unit is degree.
        #alpha1 and alpha2 the range of the picth angle.
        #movetime is the rotation time of servo and the unit is ms. if the time is not given, it will be calculated  automatically.
        x, y, z = coordinate_data
        result1 = self.setPitchRange((x, y, z), alpha, alpha1)
        result2 = self.setPitchRange((x, y, z), alpha, alpha2)
        if result1 != False:
            data = result1
            if result2 != False:
                if abs(result2[1] - alpha) < abs(result1[1] - alpha):
                    data = result2
        else:
            if result2 != False:
                data = result2
            else:
                return False
        servos, alpha = data[0], data[1]
        movetime = self.servosMove((servos["servo3"], servos["servo4"], servos["servo5"], servos["servo6"]), movetime)
        return servos, alpha, movetime
 
if __name__ == "__main__":
    AK = ArmIK()
    print(AK.setPitchRange((0, 8, 10),-90,90))
