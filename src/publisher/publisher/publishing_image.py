import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time
import cv2
import numpy as np
from std_msgs.msg import Header
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from .simConst import *
from .sim import *


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        bridge = CvBridge()
        self.left = self.create_publisher(Image,'/left/image_raw', 1)
        self.right = self.create_publisher(Image,'/right/image_raw', 1)
        #msg = Image()

        # V-Rep related
        clientID = simxStart('127.0.0.1',19999,True,True,5000,5)
        res,objs = simxGetObjects(clientID,sim_handle_all,simx_opmode_blocking)
        er , left   = simxGetObjectHandle(clientID, 'anaglyphStereoSensor_leftSensor', simx_opmode_blocking) 
        er , right   = simxGetObjectHandle(clientID, 'anaglyphStereoSensor_rightSensor', simx_opmode_blocking)
        # take pioneer control
        # er, t_rightWheel  = simxGetObjectHandle(clientID, 'wheel_right_joint', simx_opmode_blocking)
        # er, t_leftWheel   = simxGetObjectHandle(clientID, 'wheel_left_joint', simx_opmode_blocking) 
        # simxSetJointTargetVelocity(clientID, t_rightWheel, 1, simx_opmode_streaming)
        # simxSetJointTargetVelocity(clientID, t_leftWheel, 1, simx_opmode_streaming)

        while(True):
            # testing with an image
            #img = cv2.imread('/home/mirellameelo/simulator/src/simulation/simulation/OGM.png')
            err, resolution_left, left_image  = simxGetVisionSensorImage(clientID, left, 0, simx_opmode_oneshot_wait)
            err, resolution_right, right_image  = simxGetVisionSensorImage(clientID, right, 0, simx_opmode_oneshot_wait)
            left_img = np.array(left_image, dtype=np.uint8)
            left_img.resize([resolution_left[1], resolution_left[0], 3])
            right_img = np.array(right_image, dtype=np.uint8)
            right_img.resize([resolution_right[1], resolution_right[0], 3])
            self.left.publish(bridge.cv2_to_imgmsg(np.flipud(left_img), encoding="rgb8"))
            self.right.publish(bridge.cv2_to_imgmsg(np.flipud(right_img), encoding="rgb8"))


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()