#!/usr/bin/python3
# coding=utf8
import time
import Board
import ActionGroupControl as AGC

print('''
**********************************************************
************功能:幻尔科技树莓派扩展板，动作组控制例程************
**********************************************************
----------------------------------------------------------
Official website:http://www.hiwonder.com
Online mall:https://huaner.tmall.com/
----------------------------------------------------------
Tips:
 * 按下Ctrl+C可关闭此次程序运行，若失败请多次尝试！
----------------------------------------------------------
''')

# 动作组需要保存在路径/home/pi/ArmPi_mini/ActionGroups下
AGC.runAction('1')  # 参数为动作组的名称，不包含后缀，以字符形式传入
AGC.runAction('2')
