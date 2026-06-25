from curses.ascii import alt
from fileinput import filename
from pdb import main
from platform import node
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, LaserScan, NavSatFix
from geometry_msgs.msg import Vector3, Twist, PoseStamped
from std_msgs.msg import Float32, Float64MultiArray
import message_filters
import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation as R
import time
import sys
from ament_index_python.packages import get_package_share_directory
from asv_localization_interfaces.msg import BiasStateEstimate
import os
import threading
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy

class echo_state_estimate(Node):
    def __init__(self):
        super().__init__('echo_state_estimate')
        self.declare_parameter('log_data', False)
        self.log_data = self.get_parameter('log_data').get_parameter_value().bool_value

        self.create_subscription(BiasStateEstimate, 'asv/gz_sim/bias_state_estimate', self.echo_state_estimate_callback, 10)

        self.mu = np.array([])
        self.sigma = np.array([])



    def echo_state_estimate_callback(self, msg):
        self.mu = np.array(msg.mu)
        self.sigma = np.array(msg.sigma).reshape(9,9)

        pose = np.array([self.mu[0], self.mu[1], self.mu[2]])
        output = f"Estimated Pose: x={pose[0]:.8f}, y={pose[1]:.8f}, theta={pose[2]:.8f}"

        sys.stdout.write(f"\r\033[K{output}")
        sys.stdout.flush()

        print()

def main(args=None):
    rclpy.init(args=args)
    node  = echo_state_estimate()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down echo state estimate node...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()