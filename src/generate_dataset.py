import sys
import os
import shutil
import time
import cv2
import numpy as np
import sim
from datetime import datetime

class dataset():
    def create_dataset(path):
        try:
            shutil.rmtree(path + "/mav0")
        except:
            print("Removed before")
        os.makedirs(path + "/mav0/cam0/data")
        os.makedirs(path + "/mav0/cam1/data")
        print('Argument List:', str(sys.argv[1]))

        sim.simxFinish(-1) # just in case, close all opened connections
        clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim

        print ('Connected to remote API server')
        #Now try to retrieve data in a blocking fashion (i.e. a service call):
        res,objs = sim.simxGetObjects(clientID,sim.sim_handle_all,sim.simx_opmode_blocking)
        er, t_rightWheel  = sim.simxGetObjectHandle(clientID, 'Pioneer_p3dx_rightMotor', sim.simx_opmode_blocking)
        er, t_leftWheel   = sim.simxGetObjectHandle(clientID, 'Pioneer_p3dx_leftMotor', sim.simx_opmode_blocking) 
        er , cam_handle_left   = sim.simxGetObjectHandle(clientID, 'anaglyphStereoSensor_leftSensor', sim.simx_opmode_blocking) 
        er , cam_handle_right   = sim.simxGetObjectHandle(clientID, 'anaglyphStereoSensor_rightSensor', sim.simx_opmode_blocking)
        i = 0
        fl = open(path + "/mav0/timestamps.txt","w") 


        while(True):
            err, resolution_left, colorCam_left  = sim.simxGetVisionSensorImage(clientID, cam_handle_left, 0, sim.simx_opmode_oneshot_wait)
            err, resolution_right, colorCam_right  = sim.simxGetVisionSensorImage(clientID, cam_handle_right, 0, sim.simx_opmode_oneshot_wait)
            img_left_1 = np.array(colorCam_left, dtype=np.uint8)
            img_right_1 = np.array(colorCam_right, dtype=np.uint8)
            img_left_1.resize([resolution_left[1], resolution_left[0], 3])
            img_right_1.resize([resolution_right[1], resolution_right[0], 3])
            img_left_2 = np.flipud(img_left_1)
            img_right_2 = np.flipud(img_right_1)
            img_left_3 = img_left_2[...,::-1].copy()
            img_right_3 = img_right_2[...,::-1].copy()
            milli_time = int(round(time.time() * 1000))*1000000000
            st = str(milli_time) + '\n'
            st_left = path + '/mav0/cam0/data/{}.png'.format(milli_time)
            st_right = path + '/mav0/cam1/data/{}.png'.format(milli_time)
            cv2.imwrite(st_left, img_left_3)
            cv2.imwrite(st_right, img_right_3)
            cv2.waitKey(1)
            i = i+1
            fl.write(st)
            sim.simxSetJointTargetVelocity(clientID, t_rightWheel, 1, sim.simx_opmode_streaming)
            sim.simxSetJointTargetVelocity(clientID, t_leftWheel, 1, sim.simx_opmode_streaming)

        fl.close()


if __name__ == '__main__':
    path = str(sys.argv[1])
    dataset.create_dataset(path)
