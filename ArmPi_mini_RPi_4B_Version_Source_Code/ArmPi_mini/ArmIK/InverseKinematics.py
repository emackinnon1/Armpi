#!/usr/bin/env python3
# encoding: utf-8
# 4 DOF robot arm inverse kinematics：given the corresponding coordinate（X,Y,Z）and the pitch angle, calculate the rotation angle of each joint
# 2022/09/26 
import logging
from math import *

# CRITICAL, ERROR, WARNING, INFO, DEBUG
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class IK:
    # The servos is counted from bottom
    # Command parameters, e,i., the linkage parameter of 4DOF robot arm
    l1 = 8.80    #The distance between the base center of the first robot arm and the central axis of the second servo. 
    l2 = 5.80    #The distance between the second servo and the third servo and the unit is cm
    l3 = 6.20    #The distance between the third servo and the fourth servo and the unit is cm
    l4 = 9.50    #The distance between the fourth servo and the end effector, the unit is cm. The status of the end effector is completely closing.
    
    def setLinkLength(self, L1=l1, L2=l2, L3=l3, L4=l4):
        # Change the linkage length to adpat to the different length robot arm with the same structure.
        self.l1 = L1
        self.l2 = L2
        self.l3 = L3
        self.l4 = L4

    def getLinkLength(self):
        # Get the current set linkage length
        return {"L1":self.l1, "L2":self.l2, "L3":self.l3, "L4":self.l4}

    def getRotationAngle(self, coordinate_data, Alpha):
		# Given the specific coordinate and the pitch angle, the rotation angle of each joint will be returned. If no soulution, return False.
		# coordinate_data is the coordinate of the end effector and its unit is cm. It is imported by tuple, for example (0, 5, 10).
		# Alpha is the angle between the end effector and the horizontal plane and the unit is degree
		# Suppose the coordinate of the end effector is P(X, Y, Z), the origin of the coordinate is O, which is the projection of the center of the pan-tilt on ground. And the project of point P on ground is P_.
		# The intersection of 11 and 12 is A; The intersection of 12 and 13 is B; The intersection of 13 and 14 is CAF
		# CD is perpendicular to PD;CD is perpendicular to z axis. The pitch angle Alpha is the angle between DC and PC. AE is perpendicular to DP_, and E on DP_. CF is perpendicular to AE, and F is on AE.
		# The presentation of the included angle: for exmple, the angle between AB and BC is ABC 
        X, Y, Z = coordinate_data
        #Get the solution of the rotation angle of the base
        theta6 = degrees(atan2(Y, X))
 
        P_O = sqrt(X*X + Y*Y) #The distance between P_ and O
        CD = self.l4 * cos(radians(Alpha))
        PD = self.l4 * sin(radians(Alpha)) #When the pitch angle is positive, PD is positive. When the picth angle is negative, PD is negative
        AF = P_O - CD
        CF = Z - self.l1 - PD
        AC = sqrt(pow(AF, 2) + pow(CF, 2))
        if round(CF, 4) < -self.l1:
            logger.debug('the height is less than 0, CF(%s)<l1(%s)', CF, -self.l1)
            return False
        if self.l2 + self.l3 < round(AC, 4): #The sum of the lengths of two sides is less than the length of the third side
            logger.debug('Can not form linkage structure, l2(%s) + l3(%s) < AC(%s)', self.l2, self.l3, AC)
            return False
        #Get theat4
        cos_ABC = round((pow(self.l2, 2) + pow(self.l3, 2) - pow(AC, 2))/(2*self.l2*self.l3), 4) #cosine law
        if abs(cos_ABC) > 1:
            logger.debug('Can not form linkage structure, abs(cos_ABC(%s)) > 1', cos_ABC)
            return False
        ABC = acos(cos_ABC) #use the inverse trigonometric function to get the length
        theta4 = 180.0 - degrees(ABC)
        #Get theta5
        CAF = acos(AF / AC)
        cos_BAC = round((pow(AC, 2) + pow(self.l2, 2) - pow(self.l3, 2))/(2*self.l2*AC), 4) #cosine law
        if abs(cos_BAC) > 1:
            logger.debug('Can not form linkage structure, abs(cos_BAC(%s)) > 1', cos_BAC)
            return False
        if CF < 0:
            zf_flag = -1
        else:
            zf_flag = 1
        theta5 = degrees(CAF * zf_flag + acos(cos_BAC))
        #Get theta3
        theta3 = Alpha - theta5 + theta4
       
        return {"theta3":theta3, "theta4":theta4, "theta5":theta5, "theta6":theta6} # If there is a solution, return angle dictionary
            
if __name__ == '__main__':
    ik = IK()
    ik.setLinkLength(L1=ik.l1 + 1.3)
    print('the length of the link：', ik.getLinkLength())
    print(ik.getRotationAngle((0, ik.l4, ik.l1 + ik.l2 + ik.l3), 0))
