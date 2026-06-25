#!/usr/bin/env python3
"""
Gazebo to ROS bridge for topics without converter support.
Subscribes to Gazebo topics using gz CLI and publishes to ROS.
"""

import subprocess
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, NavSatFix
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64
from geometry_msgs.msg import Quaternion, Vector3, Point, Pose, Twist
import threading
import time
import re


class GazeboROSBridge(Node):
    def __init__(self):
        super().__init__('gazebo_ros_bridge')
        
        # Create publishers
        self.imu_pub = self.create_publisher(Imu, '/imu/data', 10)
        self.odom_pub = self.create_publisher(Odometry, '/odometry', 10)
        self.gps_pub = self.create_publisher(NavSatFix, '/gps/fix', 10)
        
        self.get_logger().info('Gazebo ROS Bridge initialized')
    
    def start_bridges(self):
        """Start background threads for each bridge"""
        threading.Thread(target=self._imu_bridge, daemon=True).start()
        threading.Thread(target=self._odometry_bridge, daemon=True).start()
        threading.Thread(target=self._gps_bridge, daemon=True).start()
        self.get_logger().info('Bridge threads started')
    
    def _imu_bridge(self):
        """Bridge IMU data from Gazebo to ROS"""
        gz_topic = '/world/waves/model/blueboat/link/imu_link/sensor/imu_sensor/imu'
        
        while rclpy.ok():
            try:
                result = subprocess.run(
                    ['gz', 'topic', '-e', '-t', gz_topic],
                    capture_output=True,
                    text=True,
                    timeout=2,
                    env={**subprocess.os.environ, 'GZ_PARTITION': 'ros_gz_example'}
                )
                
                if result.returncode == 0 and result.stdout:
                    msg = self._parse_imu(result.stdout)
                    if msg:
                        self.imu_pub.publish(msg)
                
                time.sleep(0.01)
            except subprocess.TimeoutExpired:
                pass
            except Exception as e:
                self.get_logger().debug(f'IMU bridge error: {e}')
                time.sleep(0.1) 
    
    def _odometry_bridge(self):
        """Bridge Odometry data from Gazebo to ROS"""
        gz_topic = '/model/blueboat/odometry'
        
        while rclpy.ok():
            try:
                result = subprocess.run(
                    ['gz', 'topic', '-e', '-t', gz_topic],
                    capture_output=True,
                    text=True,
                    timeout=2,
                    env={**subprocess.os.environ, 'GZ_PARTITION': 'ros_gz_example'}
                )
                
                if result.returncode == 0 and result.stdout:
                    msg = self._parse_odometry(result.stdout)
                    if msg:
                        self.odom_pub.publish(msg)
                
                time.sleep(0.01)
            except subprocess.TimeoutExpired:
                pass
            except Exception as e:
                self.get_logger().debug(f'Odometry bridge error: {e}')
                time.sleep(0.1)
    
    def _gps_bridge(self):
        gz_topic = '/world/waves/model/blueboat/link/gps_link/sensor/navsat_sensor/navsat'
        
        while rclpy.ok():
            try:
                result = subprocess.run(
                    ['gz', 'topic', '-e', '-n', '1', '-t', gz_topic],  # -n 1 = one message then exit
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if result.returncode == 0 and result.stdout:
                    msg = self._parse_gps(result.stdout)
                    if msg:
                        self.gps_pub.publish(msg)
            except subprocess.TimeoutExpired:
                self.get_logger().debug('GPS topic timeout')
            except Exception as e:
                self.get_logger().debug(f'GPS bridge error: {e}')
            time.sleep(0.1)
        
    def _parse_imu(self, data_str):
        """Parse Gazebo IMU message"""
        try:
            msg = Imu()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = 'imu_link'
            
            lines = data_str.split('\n')
            
            # Parse orientation quaternion
            quat = {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 1.0}
            for i, line in enumerate(lines):
                if 'orientation' in line:
                    # Look for x, y, z, w in following lines
                    for j in range(i, min(i+10, len(lines))):
                        if 'x:' in lines[j]:
                            try:
                                quat['x'] = float(lines[j].split('x:')[1].split()[0])
                            except:
                                pass
                        if 'y:' in lines[j]:
                            try:
                                quat['y'] = float(lines[j].split('y:')[1].split()[0])
                            except:
                                pass
                        if 'z:' in lines[j]:
                            try:
                                quat['z'] = float(lines[j].split('z:')[1].split()[0])
                            except:
                                pass
                        if 'w:' in lines[j]:
                            try:
                                quat['w'] = float(lines[j].split('w:')[1].split()[0])
                            except:
                                pass
                    break
            
            msg.orientation.x = quat['x']
            msg.orientation.y = quat['y']
            msg.orientation.z = quat['z']
            msg.orientation.w = quat['w']
            
            # Set covariances
            msg.orientation_covariance[0] = 0.0025
            msg.angular_velocity_covariance[0] = 0.0025
            msg.linear_acceleration_covariance[0] = 0.0025
            
            return msg
        except Exception as e:
            self.get_logger().debug(f'IMU parse error: {e}')
            return None
    
    def _parse_odometry(self, data_str):
        """Parse Gazebo Odometry message"""
        try:
            msg = Odometry()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = 'odom'
            msg.child_frame_id = 'base_link'
            
            lines = data_str.split('\n')
            
            # Parse pose position
            pos = {'x': 0.0, 'y': 0.0, 'z': 0.0}
            for i, line in enumerate(lines):
                if 'position' in line:
                    for j in range(i, min(i+5, len(lines))):
                        if 'x:' in lines[j]:
                            try:
                                pos['x'] = float(lines[j].split('x:')[1].split()[0])
                            except:
                                pass
                        if 'y:' in lines[j]:
                            try:
                                pos['y'] = float(lines[j].split('y:')[1].split()[0])
                            except:
                                pass
                        if 'z:' in lines[j]:
                            try:
                                pos['z'] = float(lines[j].split('z:')[1].split()[0])
                            except:
                                pass
                    break
            
            msg.pose.pose.position.x = pos['x']
            msg.pose.pose.position.y = pos['y']
            msg.pose.pose.position.z = pos['z']
            
            # Default orientation
            msg.pose.pose.orientation.w = 1.0
            
            # Set covariances
            msg.pose.covariance[0] = 0.1
            msg.twist.covariance[0] = 0.1
            
            return msg
        except Exception as e:
            self.get_logger().debug(f'Odometry parse error: {e}')
            return None
    
    def _parse_gps(self, data_str):
        try:
            msg = NavSatFix()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = 'gps_link'

            for line in data_str.split('\n'):
                stripped = line.strip()
                # Exact field name match to avoid 'translation', 'flatten', etc.
                if re.match(r'^latitude_deg\s*:', stripped):
                    msg.latitude = float(stripped.split(':')[1].strip())
                elif re.match(r'^longitude_deg\s*:', stripped):
                    msg.longitude = float(stripped.split(':')[1].strip())
                elif re.match(r'^altitude\s*:', stripped):
                    msg.altitude = float(stripped.split(':')[1].strip())

            msg.status.status = 0  # STATUS_FIX
            msg.status.service = 1  # SERVICE_GPS
            msg.position_covariance[0] = 2.25   # 1.5^2 horizontal
            msg.position_covariance[4] = 2.25
            msg.position_covariance[8] = 9.0    # 3.0^2 vertical
            msg.position_covariance_type = NavSatFix.COVARIANCE_TYPE_DIAGONAL_KNOWN

            return msg
        except Exception as e:
            self.get_logger().debug(f'GPS parse error: {e}')
            return None


def main(args=None):
    rclpy.init(args=args)
    bridge = GazeboROSBridge()
    bridge.start_bridges()
    
    try:
        rclpy.spin(bridge)
    except KeyboardInterrupt:
        pass
    finally:
        bridge.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
