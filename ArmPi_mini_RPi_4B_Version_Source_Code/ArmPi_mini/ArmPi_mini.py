#!/usr/bin/python3
# coding=utf8
import sys
import os
import cv2
import time
import queue
import Camera
import logging
import threading
import RPCServer
import MjpgServer
import numpy as np
import Functions.Running as Running

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

QUEUE_RPC = queue.Queue(10)

def startMiniPi():
    global HWEXT, HWSONIC

    RPCServer.QUEUE = QUEUE_RPC

    threading.Thread(target=RPCServer.startRPCServer,
                     daemon=True).start()  # rpc server
    threading.Thread(target=MjpgServer.startMjpgServer,
                     daemon=True).start()  # mjpg streaming server
    
    loading_picture = cv2.imread('/home/pi/ArmPi_mini/CameraCalibration/loading.jpg')
    cam = Camera.Camera()  # camera read 
    cam.camera_open()
    Running.cam = cam

    while True:
        time.sleep(0.03)
        # execute RPC command required to execute in thread 
        while True:
            try:
                req, ret = QUEUE_RPC.get(False)
                event, params, *_ = ret
                ret[2] = req(params)  # execute RPC command 
                event.set()
            except:
                break

        # execute game programs:
        try:
            if Running.RunningFunc > 0 and Running.RunningFunc <= 9:
                if cam.frame is not None:
                    frame = cam.frame.copy()
                    img = Running.CurrentEXE().run(frame)
                    if Running.RunningFunc == 9:
                        MjpgServer.img_show = np.vstack((img, frame))
                    else:                       
                        MjpgServer.img_show = img
                else:
                    MjpgServer.img_show = loading_picture
            else:
                MjpgServer.img_show = cam.frame
                #cam.frame = None
        except KeyboardInterrupt:
            print('RunningFunc1', Running.RunningFunc)
            break

if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    startMiniPi()
