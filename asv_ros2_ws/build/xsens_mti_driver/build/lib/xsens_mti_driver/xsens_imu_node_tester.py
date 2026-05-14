import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3
from std_msgs.msg import Float32, UInt32
import numpy as np

class XSENSETester(Node):
    def __init__(self):
        super().__init__('xsense_imu_node_tester')

        # Subscribers
        self.create_subscription(Imu, 'xsens/imu/data', self.imu_callback, 10)
        self.create_subscription(Vector3, 'xsens/imu/eu_angle', self.eu_angle_callback, 10)
        self.create_subscription(Vector3, 'xsens/imu/mag', self.mag_callback, 10)
        self.create_subscription(Vector3, 'xsens/imu/delta_v', self.delta_v_callback, 10)
        self.create_subscription(Imu, 'xsens/imu/delta_q', self.delta_q_callback, 10)
        self.create_subscription(Vector3, 'xsens/imu/free_acc', self.free_acc_callback, 10)
        self.create_subscription(Float32, 'xsens/imu/baro', self.baro_callback, 10)
        self.create_subscription(Float32, 'xsens/imu/temperature', self.temp_callback, 10)
        self.create_subscription(UInt32, 'xsens/imu/status', self.status_callback, 10)
        self.create_subscription(Float32, 'xsens/imu/dt', self.imu_dt_callback, 10)

        # Store latest values
        self.data = {
            'imu': np.zeros(10),
            'eu': np.zeros(3),
            'mag': np.zeros(3),
            'delta_v': np.zeros(3),
            'delta_q': np.zeros(4),
            'free_acc': np.zeros(3),
            'baro': 0.0,
            'temp': 0.0,
            'status': 0
        }

        # Timer to print data once per loop
        self.create_timer(0.05, self.print_data)  # 20 Hz

    # ---- Callbacks ----
    def imu_callback(self, msg: Imu):
        self.data['imu'][:4] = [msg.orientation.w, msg.orientation.x, msg.orientation.y, msg.orientation.z]
        self.data['imu'][4:7] = [msg.angular_velocity.x, msg.angular_velocity.y, msg.angular_velocity.z]
        self.data['imu'][7:] = [msg.linear_acceleration.x, msg.linear_acceleration.y, msg.linear_acceleration.z]

    def eu_angle_callback(self, msg: Vector3):
        self.data['eu'] = [msg.x, msg.y, msg.z]

    def mag_callback(self, msg: Vector3):
        self.data['mag'] = [msg.x, msg.y, msg.z]

    def delta_v_callback(self, msg: Vector3):
        self.data['delta_v'] = [msg.x, msg.y, msg.z]

    def delta_q_callback(self, msg: Imu):
        self.data['delta_q'] = [msg.orientation.w, msg.orientation.x, msg.orientation.y, msg.orientation.z]

    def free_acc_callback(self, msg: Vector3):
        self.data['free_acc'] = [msg.x, msg.y, msg.z]

    def baro_callback(self, msg: Float32):
        self.data['baro'] = msg.data

    def temp_callback(self, msg: Float32):
        self.data['temp'] = msg.data

    def status_callback(self, msg: UInt32):
        self.data['status'] = msg.data

    def imu_dt_callback(self, msg: Float32):
        self.data['imu_dt'] = msg.data

    # ---- Print in single line ----
    def print_data(self):
        row = np.concatenate([
            self.data['imu'],        # 10 values
            self.data['eu'],         # 3 values
            self.data['mag'],        # 3
            self.data['delta_v'],    # 3
            self.data['delta_q'],    # 4
            self.data['free_acc'],   # 3
            [self.data['baro']],     # 1
            [self.data['temp']],     # 1
            [self.data['status']],   # 1
            [self.data['imu_dt']]    # 1
        ])
        n = len(row)
        print(f"\rdata: {row[10:13]}", end="", flush=True)

def main(args=None):
    rclpy.init(args=args)
    node = XSENSETester()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nShutting down tester...")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
