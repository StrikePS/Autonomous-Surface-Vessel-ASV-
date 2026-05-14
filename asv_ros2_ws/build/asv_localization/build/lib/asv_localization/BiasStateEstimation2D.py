from curses.ascii import alt
from fileinput import filename
from pdb import main
from platform import node
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, LaserScan, NavSatFix
from geometry_msgs.msg import Vector3, Twist
from std_msgs.msg import Float32, Float64MultiArray
import message_filters
import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation as R
import time
import sys
from ament_index_python.packages import get_package_share_directory
import os
import csv
from asv_localization_interfaces.msg import BiasStateEstimate
import threading

class BiasStateEstimation2D(Node):
    def __init__(self):
        super().__init__('asv_state_estimate')
        self.declare_parameter('log_data', False)
        self.log_data = self.get_parameter('log_data').get_parameter_value().bool_value

        self.data = {'imu': np.zeros(10),
                     'gnss': np.zeros(3)}
        
        self.initialize = False

        self.EarthA = 6378137.0 # semi-major axis of the Earth
        self.EarthE = 8.1819190842622e-2 # eccentricity of the Earth
        self.EarthB = 6356752.3 # semi-minor axis of the Earth

        self.ref_lat = None
        self.ref_lon = None
        self.ref_alt = None
        self.ref_ecef = None
        self.magnetic_declination = -0.7

        self.mu = np.array([])
        self.sigma = np.array([])

        self.dt = 0.1 # time step

        # uncomment and use for logging or diagnostic purposes
        # self.Q = np.array([]) # covariance of motion model noise
        # self.H = np.array([]) # jacobian of sensor model
        # self.R = np.array([]) # covariance of sensor model noise
        # self.S = np.array([]) # innovation covariance

        self.m = 25.0 # mass of the ASV
        self.I = 10.0 # moment of inertia of the ASV
        self.d = 1.0 # distance between two propellers

        # frame charaxteristics.
        # for body frame, xb piints forward, yb points left, zb points down. origin is at the center of the ASV
        # for NED frame, xn points north, yn points east, zn points down. origin is at the initial position of the ASV

        self.thrust_table = None
        self.csv_data_read('T100-PWM-Thrust-raw.csv')
        self.pwml = 1500.0
        self.pwmr = 1500.0
        self.pwm_lock = threading.Lock()

        # Subscribers
        imu_sub = message_filters.Subscriber(self, Imu, 'xsens/imu/data')
        gnss_sub = message_filters.Subscriber(self, NavSatFix, 'gnss/fix')
        self.create_subscription(Float32, 'esc1_cmd', self.esc1_callback, 10)
        self.create_subscription(Float32, 'esc2_cmd', self.esc2_callback, 10)

        # synchronized IMU + GNSS subscribers
        self.sync = message_filters.ApproximateTimeSynchronizer(fs = [imu_sub, gnss_sub], queue_size=10, slop=0.1)
        self.sync.registerCallback(self.ekf_callback)

        # Publishers
        self.state_pub = self.create_publisher(BiasStateEstimate, 'asv/bias_state_estimate', 10)
        self.state_pub_frequency = 10
        self.state_pub_timer = self.create_timer(1.0 / self.state_pub_frequency, self.publish_state_estimate)

    # ---- Callbacks ----
    def imu_callback(self, msg: Imu):
        self.data['imu'][:4] = [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w]
        self.data['imu'][4:7] = [msg.angular_velocity.x, msg.angular_velocity.y, msg.angular_velocity.z]
        self.data['imu'][7:] = [msg.linear_acceleration.x, msg.linear_acceleration.y, msg.linear_acceleration.z]
        self.last_imu_time = self.get_clock().now()

    def gnss_callback(self, msg: NavSatFix):
        self.data['gnss'] = [msg.latitude, msg.longitude, msg.altitude]
        self.last_gps_time = self.get_clock().now()

    def esc1_callback(self, msg):
        with self.pwm_lock:
            self.pwml = float(msg.data)

    def esc2_callback(self, msg):
        with self.pwm_lock:
            self.pwmr = float(msg.data)

    # ---- Publishers ----
    def publish_state_estimate(self):
        msg = BiasStateEstimate()
        if self.initialize:
            msg.mu = self.mu.tolist()
            msg.sigma = self.sigma.flatten().tolist()
            self.state_pub.publish(msg)

        # unpack the message for logging or other purposes
        # mu = np.array(msg.mu)                      # shape (9,)
        # sigma = np.array(msg.sigma).reshape(9, 9)  # shape (9,9)
        return

    # ---- Helper Functions ----
    def get_thrust_from_pwm(self, pwml, pwmr):
        pwm_values = self.thrust_table['PWM'].values
        thrust_values = self.thrust_table['Thrust'].values

        ul = np.interp(pwml, pwm_values, thrust_values)
        ur = np.interp(pwmr, pwm_values, thrust_values)
        return ul, ur
    
    def csv_data_read(self, filename):
        pkg_share = get_package_share_directory('asv_localization')
        csv_file = os.path.join(pkg_share, 'data', filename)
        self.thrust_table = pd.read_csv(csv_file)
        return

    def init_mu_sigma(self, lla, q, vx_body, vy_body, theta_dot, b_ax, b_ay, b_wz):
        self.ref_lat = lla[0]
        self.ref_lon = lla[1]
        self.ref_alt = lla[2]
        self.ref_ecef = self.lla_to_ecef(self.ref_lat, self.ref_lon, self.ref_alt)

        ecef = self.lla_to_ecef(lla[0], lla[1], lla[2])
        ned = self.ecef_to_ned(ecef, self.ref_ecef, self.ref_lat, self.ref_lon)
        x, y = ned[0], ned[1]

        theta = R.from_quat(q).as_euler('zyx')[0]

        x_dot = vx_body * np.cos(theta) - vy_body * np.sin(theta)
        y_dot = vx_body * np.sin(theta) + vy_body * np.cos(theta)

        self.mu = np.array([x, y, theta, x_dot, y_dot, theta_dot, b_ax, b_ay, b_wz])
        self.sigma = np.diag([2.0**2, 2.0**2, np.radians(10)**2, 1.0**2, 1.0**2, np.radians(5)**2, 0.005**2, 0.005**2, np.radians(1)**2])

        return self.mu, self.sigma

    def wrap_angle(self, a):
        return np.arctan2(np.sin(a), np.cos(a))
    
    def lla_to_ecef(self, lat, lon, alt):
        lat_rad = np.radians(lat)
        lon_rad = np.radians(lon)

        N = self.EarthA / np.sqrt(1 - self.EarthE**2 * np.sin(lat_rad)**2)

        x = (N + alt) * np.cos(lat_rad) * np.cos(lon_rad)
        y = (N + alt) * np.cos(lat_rad) * np.sin(lon_rad)
        z = (N * (1 - self.EarthE**2) + alt) * np.sin(lat_rad)

        return np.array([x, y, z])
    
    def ecef_to_ned(self, ecef, ref_ecef, ref_lat, ref_lon):
        lat_rad = np.radians(ref_lat)
        lon_rad = np.radians(ref_lon)

        rot = np.array([[-np.sin(lat_rad)*np.cos(lon_rad), -np.sin(lat_rad)*np.sin(lon_rad), np.cos(lat_rad)],
                        [-np.sin(lon_rad), np.cos(lon_rad), 0],
                        [-np.cos(lat_rad)*np.cos(lon_rad), -np.cos(lat_rad)*np.sin(lon_rad), -np.sin(lat_rad)]])

        ned = rot @ (ecef - ref_ecef)
        return ned
    
    def gps_to_ned(self, lla):
        ecef = self.lla_to_ecef(lla[0], lla[1], lla[2])
        ned = self.ecef_to_ned(ecef, self.ref_ecef, self.ref_lat, self.ref_lon)
        return ned[0], ned[1]
    
    def enu_to_ned_quat(self, q_enu):
        r_enu2ned = R.from_euler('zx', [90, 180], degrees=True)
        r_mag_ned = r_enu2ned * R.from_quat(q_enu)
        r_decl = R.from_euler('z', self.mag_declination_deg, degrees=True)
        r_true_ned = r_decl * r_mag_ned
        return r_true_ned.as_quat()
    
    def quat_to_rotation_matrix(self, q):
        x, y, z, w = q
        R = np.array([
            [1 - 2*(y**2 + z**2),     2*(x*y - z*w),         2*(x*z + y*w)],
            [2*(x*y + z*w),           1 - 2*(x**2 + z**2),   2*(y*z - x*w)],
            [2*(x*z - y*w),           2*(y*z + x*w),         1 - 2*(x**2 + y**2)]
        ])
        return R
    
    def quat_normalize(self, q):
        norm = np.linalg.norm(q)
        if norm > 0:
            return q / norm
        else:
            return q
        
    def quat_multiply(self, q1, q2):
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2
        w = w1*w2 - x1*x2 - y1*y2 - z1*z2
        x = w1*x2 + x1*w2 + y1*z2 - z1*y2
        y = w1*y2 - x1*z2 + y1*w2 + z1*x2
        z = w1*z2 + x1*y2 - y1*x2 + z1*w2
        return np.array([w, x, y, z])
    
    def skew(self, v):
        return np.array([
            [ 0,    -v[2],  v[1]],
            [ v[2],  0,    -v[0]],
            [-v[1],  v[0],  0   ]
        ])
    
    def body_to_global_acceleration(self, x_ddot, y_ddot, z_ddot, q):
        rot = R.from_quat(q).as_matrix()
        acc_body = np.array([x_ddot, y_ddot, z_ddot])
        acc_global = rot @ acc_body
        return acc_global[0], acc_global[1], acc_global[2]
    
    # ---- EKF Steps ----
    def prediction_step(self, u, mu, sigma):
        # updates belief according to the motion model.
        # localization in NED frame (global frame)

        x = mu[0]
        y = mu[1]
        theta = mu[2]
        x_dot = mu[3]
        y_dot = mu[4]
        theta_dot = mu[5]
        b_ax = mu[6]
        b_ay = mu[7]
        b_wz = mu[8]

        # thrust from propellers in body frame (control input)
        ul = u[0]
        ur = u[1]

        m = self.m
        I = self.I
        d = self.d
        dt = self.dt

        # jacobian of motion model
        G = np.array([[1,0,-0.5*np.sin(theta)*(ul+ur)*(1/m)*dt**2,self.dt,0,0,-dt**2,0,0],
                [0,1,0.5*np.cos(theta)*(ul+ur)*(1/m)*dt**2,0,self.dt,0,0,-dt**2,0],
                [0,0,1,0,0,self.dt,0,0,-dt],
                [0,0,-np.sin(theta)*(ul+ur)*(1/m)*dt,1,0,0,-dt,0,0],
                [0,0,np.cos(theta)*(ul+ur)*(1/m)*dt,0,1,0,0,-dt,0],
                [0,0,0,0,0,1,0,0,-1],
                [0,0,0,0,0,0,1,0,0],
                [0,0,0,0,0,0,0,1,0],
                [0,0,0,0,0,0,0,0,1]])

        # jacobian of motion model with respect to control
        V = np.array([[0.5*np.cos(theta)*(1/m)*dt**2, 0.5*np.cos(theta)*(1/m)*dt**2],
                [0.5*np.sin(theta)*(1/m)*dt**2, 0.5*np.sin(theta)*(1/m)*dt**2],
                [0.5*(d/2)*(1/I)*dt**2, -0.5*(d/2)*(1/I)*dt**2],
                [np.cos(theta)*(1/m)*dt, np.cos(theta)*(1/m)*dt],
                [np.sin(theta)*(1/m)*dt, np.sin(theta)*(1/m)*dt],
                [(d/2)*(1/I)*dt, -(d/2)*(1/I)*dt],
                [0, 0],
                [0, 0],
                [0, 0]])
        
        # noise based on actuation characteristics
        Q_ctrl = np.diag([0.1, 0.1])
        Q_bias = np.diag([0.005, 0.005, np.radians(1)**2])
        Q = np.zeros((9, 9))
        Q[0:6, 0:6] = V @ Q_ctrl @ np.transpose(V)
        Q[6:9, 6:9] = Q_bias

        # update mean based on motion model
        x = x + x_dot*self.dt + (0.5*(np.cos(theta)*(ul+ur)*(1/m)) - b_ax)*dt**2
        y = y + y_dot*self.dt + (0.5*(np.sin(theta)*(ul+ur)*(1/m)) - b_ay)*dt**2
        x_dot = x_dot + ((np.cos(theta)*(ul+ur)*(1/m)) - b_ax)*dt
        y_dot = y_dot + ((np.sin(theta)*(ul+ur)*(1/m)) - b_ay)*dt
        theta = theta + (theta_dot - b_wz)*dt + 0.5*(d/2)*(ul-ur)*(1/I)*dt**2
        theta_dot = theta_dot + (d/2)*(ul-ur)*(1/I)*dt
        
        # covariance update
        sigma = G@sigma@np.transpose(G) + Q
        mu = np.array([x, y, theta, x_dot, y_dot, theta_dot, b_ax, b_ay, b_wz])

        return mu, sigma
    
    def correction_step(self, z, u, mu, sigma):
        x = mu[0]
        y = mu[1]
        theta = mu[2]
        x_dot = mu[3]
        y_dot = mu[4]
        theta_dot = mu[5]
        b_ax = mu[6]
        b_ay = mu[7]
        b_wz = mu[8]

        ul = u[0]
        ur = u[1]

        x_meas = z[0]
        y_meas = z[1]
        theta_meas = z[2]
        x_ddot_meas = z[3]
        y_ddot_meas = z[4]
        theta_dot_meas = z[5]

        m = self.m
        I = self.I
        d = self.d

        # measurement innovation
        z_ = np.array([x_meas - x,
                        y_meas - y,
                        self.wrap_angle(theta_meas - theta),
                        x_ddot_meas - np.cos(theta)*(ul+ur)*(1/m) + b_ax,
                        y_ddot_meas - np.sin(theta)*(ul+ur)*(1/m) + b_ay,
                        theta_dot_meas - theta_dot + b_wz])
        
        # jacobian of sensor model
        H = np.array([[1,0,0,0,0,0,0,0,0],
                            [0,1,0,0,0,0,0,0,0],
                            [0,0,1,0,0,0,0,0,0],
                            [0,0,-(np.sin(theta)*(ul+ur)*(1/m)),0,0,0,-1,0,0],
                            [0,0,(np.cos(theta)*(ul+ur)*(1/m)),0,0,0,0,-1,0],
                            [0,0,0,0,0,1,0,0,-1]])

        # noise based on sensor characteristics
        R = np.diag([2.0**2, 2.0**2, 0.01, 0.5, 0.5, 0.05])

        # Innocation Covariance Matrix
        S = H@sigma@np.transpose(H) + R

        # Kalman Gain
        K = sigma@np.transpose(H)@np.linalg.inv(S)

        # Update mean
        mu = mu + K@z_
        mu[2] = self.wrap_angle(mu[2])

        # update covariance using Joseph form
        I_KH = np.eye(9) - K@H
        sigma = I_KH@sigma@np.transpose(I_KH) + K@R@np.transpose(K)

        return mu, sigma
    
    def ekf_callback(self, imu_msg: Imu, gnss_msg: NavSatFix):
        t = imu_msg.header.stamp.sec + imu_msg.header.stamp.nanosec * 1e-9
        if hasattr(self, '_last_t') and self._last_t is not None:
            self.dt = t - self._last_t
            if self.dt <= 0 or self.dt > 1.0:   # guard against bad dt
                self.get_logger().warn(f"Skipping EKF: abnormal dt={self.dt:.3f}s")
                self._last_t = t
                return
        else:
            self.dt = 0.1  # fallback on first message
        self._last_t = t

        q_mag_enu = [imu_msg.orientation.x, imu_msg.orientation.y, imu_msg.orientation.z, imu_msg.orientation.w]
        q = self.enu_to_ned_quat(q_mag_enu)
        theta = R.from_quat(q).as_euler('zyx')[0]
        x_ddot = imu_msg.linear_acceleration.x
        y_ddot = imu_msg.linear_acceleration.y
        z_ddot = imu_msg.linear_acceleration.z
        theta_dot = imu_msg.angular_velocity.z
        lla = [gnss_msg.latitude, gnss_msg.longitude, gnss_msg.altitude]
        self.data['imu'][:4] = q
        self.data['imu'][4:7] = [imu_msg.angular_velocity.x, imu_msg.angular_velocity.y, imu_msg.angular_velocity.z]
        self.data['imu'][7:] = [imu_msg.linear_acceleration.x, imu_msg.linear_acceleration.y, imu_msg.linear_acceleration.z]
        self.data['gnss'] = lla
        x_ddot_global, y_ddot_global, z_ddot_global = self.body_to_global_acceleration(x_ddot, y_ddot, z_ddot, q)

        if not self.initialize:
            self.init_mu_sigma(lla, q, 0.0, 0.0, theta_dot, 0.0, 0.0, 0.0)
            self.initialize = True
            self.get_logger().info("Received first GNSS and IMU measurement. Initializing state estimate.")
            return
        
        with self.pwm_lock:
            pwml = self.pwml
            pwmr = self.pwmr
        
        x,y = self.gps_to_ned(lla)
        z = np.array([x,y,theta,x_ddot_global,y_ddot_global,theta_dot])
        u = self.get_thrust_from_pwm(pwml, pwmr)

        # EKF prediction and correction steps
        self.mu, self.sigma = self.prediction_step(u, self.mu, self.sigma)
        self.mu, self.sigma = self.correction_step(z, u, self.mu, self.sigma)

        if np.any(np.diag(self.sigma) < 0):
            self.get_logger().error("Covariance diverged! Reinitializing...")
            self.initialize = False

        # publish state estimate at a fixed frequency
        # self.publish_state_estimate()

def main(args=None):
    rclpy.init(args=args)
    node  = BiasStateEstimation2D()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down State Estimate node...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()