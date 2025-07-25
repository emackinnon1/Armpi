#!/usr/bin/python3
# coding=utf8
import sys
import time
import threading
import Functions.lab_adjust as lab_adjust
import Functions.ColorDetect as ColorDetect
import Functions.ColorSorting as ColorSorting
import Functions.RemoteControl as RemoteControl
import Functions.ColorTracking as ColorTracking
import Functions.ColorPalletizing as ColorPalletizing

RunningFunc = 0
LastHeartbeat = 0
cam = None

FUNCTIONS = {
    0: None,
    1: RemoteControl,    # Motion control 
    2: ColorDetect,      # Color recognition
    3: ColorSorting,     # Color sorting
    4: ColorTracking,    # Color tracking
    5: ColorPalletizing, # Intelligent stacking
    6: None,
    7: None,
    8: None,
    9: lab_adjust        # lab calibration
}

def doHeartbeat(tmp=()):
    global LastHeartbeat
    LastHeartbeat = time.time() + 17
    return (True, ())

def CurrentEXE():
    global RunningFunc
    
    if RunningFunc == 0:
        print('RunningFunc2', RunningFunc)
        return FUNCTIONS[1]
    else:
        return FUNCTIONS[RunningFunc]

def loadFunc(newf):
    global RunningFunc
    new_func = newf[0]

    doHeartbeat()

    if new_func < 1 or new_func > 9:
        return (False,  sys._getframe().f_code.co_name + ": Invalid argument")
    else:
        try:
            if RunningFunc > 1:
                FUNCTIONS[RunningFunc].exit()
            RunningFunc = newf[0]
            #cam.camera_close()
            #cam.camera_open()
            print('RunningFunc', RunningFunc)
            if RunningFunc > 0:
                FUNCTIONS[RunningFunc].init()
        except Exception as e:
            print('error2', RunningFunc, e)
    return (True, (RunningFunc,))

def unloadFunc(tmp = ()):
    global RunningFunc
    if RunningFunc != 0:
        FUNCTIONS[RunningFunc].exit()
        RunningFunc = 0
    #cam.camera_close()
    return (True, (0,))

def getLoadedFunc(newf):
    global RunningFunc
    return (True, (RunningFunc,))

def startFunc(tmp):
    global RunningFunc
    FUNCTIONS[RunningFunc].start()
    return (True, (RunningFunc,))

def stopFunc(tmp):
    global RunningFunc
    FUNCTIONS[RunningFunc].stop()
    return (True, (RunningFunc,))

def heartbeatTask():
    global LastHeartbeat
    global RunningFunc
    while True:
        try:
            if LastHeartbeat < time.time():
                if RunningFunc != 0:
                    unloadFunc()
            time.sleep(0.1)
        except KeyboardInterrupt:
            print('error1')
            break

threading.Thread(target=heartbeatTask, daemon=True).start()

