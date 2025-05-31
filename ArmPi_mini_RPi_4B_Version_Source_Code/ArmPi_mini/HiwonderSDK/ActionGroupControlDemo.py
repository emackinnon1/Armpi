#!/usr/bin/python3
# coding=utf8
import time
import Board
import ActionGroupControl as AGC

print('''
**********************************************************
************Function: Action group control routine************
**********************************************************
----------------------------------------------------------
Official website:http://www.hiwonder.com
Online mall:https://huaner.tmall.com/
----------------------------------------------------------
Tips:
 * Press "Ctrl+C" to stop running program. If fail to exit, please try few more times!
----------------------------------------------------------
''')

# Action group needs to be stored in /home/emackinnon1/Projects/Armpi/ArmPi_mini_RPi_4B_Version_Source_Code/ArmPi_mini/ActionGroups
AGC.runAction('1')  # Parameter is the name of action group. suffix is not included 
AGC.runAction('2')
