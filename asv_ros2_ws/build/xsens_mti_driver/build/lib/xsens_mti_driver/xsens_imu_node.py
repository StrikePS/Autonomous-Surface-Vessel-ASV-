import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3
from std_msgs.msg import Float32, UInt32, Header

import time
from datetime import datetime

from xsens_mti_driver.SerialHandler import SerialHandler
from xsens_mti_driver.XbusPacket import XbusPacket
from xsens_mti_driver.DataPacketParser import DataPacketParser, XsDataPacket
from xsens_mti_driver.SetOutput import set_output_conf
from xsens_mti_driver.data_logging import save_data_to_csv


class XSENSImuNode(Node):

    def __init__(self):
        super().__init__('xsens_imu_node')

        # ---- Publishers ----
        self.imu_pub = self.create_publisher(Imu, 'xsens/imu/data', 11)
        self.eu_angle_pub = self.create_publisher(Vector3, 'xsens/imu/eu_angle', 10)
        self.mag_pub = self.create_publisher(Vector3, 'xsens/imu/mag', 10)
        self.delta_v_pub = self.create_publisher(Vector3, 'xsens/imu/delta_v', 10)
        self.delta_q_pub = self.create_publisher(Imu, 'xsens/imu/delta_q', 10)
        self.free_acc_pub = self.create_publisher(Vector3, 'xsens/imu/free_acc', 10)
        self.baro_pub = self.create_publisher(Float32, 'xsens/imu/baro', 10)
        self.temp_pub = self.create_publisher(Float32, 'xsens/imu/temperature', 10)
        self.status_pub = self.create_publisher(UInt32, 'xsens/imu/status', 10)
        self.dt_pub = self.create_publisher(Float32, 'xsens/imu/dt', 10)

        # ---- Time tracking ----
        self.last_timestamp = None
        self.dt = 0.0
        self.velocity = [0.0, 0.0, 0.0]

        # ---- Serial params ----
        self.port = '/dev/ttyUSB0'
        self.baudrate = 115200

        self.get_logger().info('Opening XSENS serial port...')
        self.serial = SerialHandler(self.port, self.baudrate)

        go_to_config = bytes.fromhex('FA FF 30 00')
        go_to_measurement = bytes.fromhex('FA FF 10 00')

        self.serial.send_with_checksum(go_to_config)
        time.sleep(0.1)

        set_output_conf(self.serial)
        time.sleep(0.1)

        self.serial.send_with_checksum(go_to_measurement)

        # ---- Packet handler ----
        self.packet = XbusPacket(on_data_available=self.on_data_available)

        # ---- Timer ----
        self.timer = self.create_timer(0.01, self.read_serial)

        self.get_logger().info('XSENS ROS2 node started')

    # def read_serial(self):
    #     try:
    #         # byte = self.serial.read_byte()
    #         # self.packet.feed_byte(byte)
    #         data_bytes = self.serial.read_bytes(256)  # read a chunk
    #         for byte in data_bytes:
    #             self.packet.feed_byte(byte)
    #     except Exception as e:
    #         self.get_logger().warn(f"Serial error: {e}")

    def read_serial(self):
        try:
            data_bytes = self.serial.read_bytes(256)  # read a chunk
            for byte in data_bytes:
                self.packet.feed_byte(bytes([byte]))  # convert int -> bytes
        except Exception as e:
            self.get_logger().warn(f"Serial error: {e}")


    def on_data_available(self, packet):
        data = XsDataPacket()
        DataPacketParser.parse_data_packet(packet, data)

        # ---- Calculate dt ----
        current_timestamp = self.get_clock().now().to_msg()
        if self.last_timestamp is not None:
            self.dt = (current_timestamp.sec - self.last_timestamp.sec) + \
                    (current_timestamp.nanosec - self.last_timestamp.nanosec) / 1e9
            
            #  Publish dt
            self.dt_pub.publish(Float32(data=float(self.dt)))
            
        self.last_timestamp = current_timestamp

        imu_msg = Imu()
        imu_msg.header = Header()
        imu_msg.header.stamp = self.get_clock().now().to_msg()
        imu_msg.header.frame_id = 'xsens_link'

        # ---- Orientation (Quaternion) ----
        if data.quaternionAvailable:
            imu_msg.orientation.w = data.quat[0]
            imu_msg.orientation.x = data.quat[1]
            imu_msg.orientation.y = data.quat[2]
            imu_msg.orientation.z = data.quat[3]

        # ---- Angular velocity (rad/s) ----
        if data.rotAvailable:
            imu_msg.angular_velocity.x = data.rot[0]
            imu_msg.angular_velocity.y = data.rot[1]
            imu_msg.angular_velocity.z = data.rot[2]

        # ---- Linear acceleration (m/s²) ----
        if data.accAvailable:
            imu_msg.linear_acceleration.x = data.acc[0]
            imu_msg.linear_acceleration.y = data.acc[1]
            imu_msg.linear_acceleration.z = data.acc[2]

        self.imu_pub.publish(imu_msg)

        # ---- Euler angles ----
        if data.eulerAvailable:
            rpy = Vector3()
            rpy.x = data.euler[0]
            rpy.y = data.euler[1]
            rpy.z = data.euler[2]
            self.eu_angle_pub.publish(rpy)

        # ---- Magnetic field ----
        if data.magAvailable:
            mag = Vector3()
            mag.x = data.mag[0]
            mag.y = data.mag[1]
            mag.z = data.mag[2]
            self.mag_pub.publish(mag)

        # ---- Delta V ----
        if data.deltaVAvailable:
            delta_v = Vector3()
            delta_v.x = data.deltaV[0]
            delta_v.y = data.deltaV[1]
            delta_v.z = data.deltaV[2]
            self.delta_v_pub.publish(delta_v)

        # ---- Delta Q ----
        if data.deltaQAvailable:
            delta_q = Imu()
            delta_q.header = imu_msg.header
            delta_q.orientation.w = data.deltaQ[0]
            delta_q.orientation.x = data.deltaQ[1]
            delta_q.orientation.y = data.deltaQ[2]
            delta_q.orientation.z = data.deltaQ[3]
            self.delta_q_pub.publish(delta_q)

        # ---- Free acceleration ----
        if data.freeAccAvailable:
            free_acc = Vector3()
            free_acc.x = data.freeAcc[0]
            free_acc.y = data.freeAcc[1]
            free_acc.z = data.freeAcc[2]
            self.free_acc_pub.publish(free_acc)

        # ---- Barometric pressure ----
        if data.baropressureAvailable:
            self.baro_pub.publish(Float32(data=float(data.baropressure)))

        # ---- Temperature ----
        if data.temperatureAvailable:
            self.temp_pub.publish(Float32(data=float(data.temperature)))

        # ---- Status word ----
        if data.statusWordAvailable:
            self.status_pub.publish(UInt32(data=int(data.statusWord)))


def main(args=None):
    rclpy.init(args=args)
    node = XSENSImuNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()




'''
def on_live_data_available(packet, filename):
    xbus_data = XsDataPacket() 
    DataPacketParser.parse_data_packet(packet, xbus_data)

    # if xbus_data.packetCounterAvailable:
    #     print(f"\npacketCounter: {xbus_data.packetCounter}, ", end='')

    # if xbus_data.sampleTimeFineAvailable:
    #     print(f"sampleTimeFine: {xbus_data.sampleTimeFine}, ", end='')

    # if xbus_data.utcTimeAvailable:
    #     print(f"utctime epochSeconds: {xbus_data.utcTime:.9f}")

    # if xbus_data.eulerAvailable:
    #     print(f"\nRoll, Pitch, Yaw: [{xbus_data.euler[0]:.2f}, {xbus_data.euler[1]:.2f}, {xbus_data.euler[2]:.2f}], ", end='')

    # if xbus_data.quaternionAvailable:
    #     print(f"q0, q1, q2, q3: [{xbus_data.quat[0]:.4f}, {xbus_data.quat[1]:.4f}, {xbus_data.quat[2]:.4f}, {xbus_data.quat[3]:.4f}], ", end='')

    # if xbus_data.rotAvailable:
    #     rate_of_turn_degree = [
    #         xbus_data.rad2deg * xbus_data.rot[0],
    #         xbus_data.rad2deg * xbus_data.rot[1],
    #         xbus_data.rad2deg * xbus_data.rot[2]
    #     ]
    #     print(f"\nRateOfTurn: [{rate_of_turn_degree[0]:.2f}, {rate_of_turn_degree[1]:.2f}, {rate_of_turn_degree[2]:.2f}], ", end='')

    # if xbus_data.accAvailable:
    #     print(f"Acceleration: [{xbus_data.acc[0]:.2f}, {xbus_data.acc[1]:.2f}, {xbus_data.acc[2]:.2f}], ", end='')

    # if xbus_data.magAvailable:
    #     print(f"Magnetic Field: [{xbus_data.mag[0]:.2f}, {xbus_data.mag[1]:.2f}, {xbus_data.mag[2]:.2f}]")

    # if xbus_data.latlonAvailable and xbus_data.altitudeAvailable:
    #     print(f"\nLat, Lon, Alt: [{xbus_data.latlon[0]:.9f}, {xbus_data.latlon[1]:.9f}, {xbus_data.altitude:.9f}]")

    # if xbus_data.velocityAvailable:
    #     print(f"Vel E, N, U: [{xbus_data.vel[0]:.9f}, {xbus_data.vel[1]:.9f}, {xbus_data.vel[2]:.9f}]")
    
    # if xbus_data.temperatureAvailable:
    #     print(f"Temperature: {xbus_data.temperature:.2f}")
    
    # if xbus_data.baropressureAvailable:
    #     print(f"Barometric Pressure: {xbus_data.baropressure} Pa")
    
    # if xbus_data.deltaVAvailable:
    #     print(f"Delta V: [{xbus_data.deltaV[0]:.2f}, {xbus_data.deltaV[1]:.2f}, {xbus_data.deltaV[2]:.2f}]")
    
    # if xbus_data.deltaQAvailable:
    #     print(f"Delta Q: [{xbus_data.deltaQ[0]:.4f}, {xbus_data.deltaQ[1]:.4f}, {xbus_data.deltaQ[2]:.4f}, {xbus_data.deltaQ[3]:.4f}]")
    
    # save_data_to_csv(xbus_data, filename, log_position_velocity=False)
    data = xbus_data
    row = [
            data.packetCounter if data.packetCounterAvailable else '',
            data.sampleTimeFine if data.sampleTimeFineAvailable else '',
            data.utcTime if data.utcTimeAvailable else '',
            data.euler[0] if data.eulerAvailable else '',
            data.euler[1] if data.eulerAvailable else '',
            data.euler[2] if data.eulerAvailable else '',
            data.quat[0] if data.quaternionAvailable else '',
            data.quat[1] if data.quaternionAvailable else '',
            data.quat[2] if data.quaternionAvailable else '',
            data.quat[3] if data.quaternionAvailable else '',
            data.rot[0] * data.rad2deg if data.rotAvailable else '',
            data.rot[1] * data.rad2deg if data.rotAvailable else '',
            data.rot[2] * data.rad2deg if data.rotAvailable else '',
            data.acc[0] if data.accAvailable else '',
            data.acc[1] if data.accAvailable else '',
            data.acc[2] if data.accAvailable else '',
            data.mag[0] if data.magAvailable else '',
            data.mag[1] if data.magAvailable else '',
            data.mag[2] if data.magAvailable else '',
            data.deltaV[0] if data.deltaVAvailable else '',
            data.deltaV[1] if data.deltaVAvailable else '',
            data.deltaV[2] if data.deltaVAvailable else '',
            data.deltaQ[0] if data.deltaQAvailable else '',
            data.deltaQ[1] if data.deltaQAvailable else '',
            data.deltaQ[2] if data.deltaQAvailable else '',
            data.deltaQ[3] if data.deltaQAvailable else '',
            data.freeAcc[0] if data.freeAccAvailable else '',
            data.freeAcc[1] if data.freeAccAvailable else '',
            data.freeAcc[2] if data.freeAccAvailable else '',
            data.baropressure if data.baropressureAvailable else '',
            data.temperature if data.temperatureAvailable else '',
            data.statusWord if data.statusWordAvailable else ''
        ]
    print(f"\rdata: {row[3:6]}", end="", flush=True)

    
def main():
    try:
        serial = SerialHandler("/dev/ttyUSB0", 115200) ##change the port and baudrate to your own MTi's baudrate.

        go_to_config = bytes.fromhex('FA FF 30 00')
        go_to_measurement = bytes.fromhex('FA FF 10 00')

        serial.send_with_checksum(go_to_config)
        ###if you want to configure your sensor's output, check the set_output_conf function.
        ##set_output_conf(serial)
        time.sleep(0.1)  # Sleep for 0.1 sec

        set_output_conf(serial)
        time.sleep(0.1)

        serial.send_with_checksum(go_to_measurement)
        
        packet = XbusPacket(on_data_available=lambda p: on_live_data_available(p, filename))
        
        # Generate a timestamp-based filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{timestamp}.csv'
        
        serial.send_with_checksum(go_to_measurement)
        print("Listening for packets...")

        while True:
            try:
                byte = serial.read_byte()
                packet.feed_byte(byte)
            except RuntimeError as e:
                print(f"Error reading byte: {e}")
                continue  # Skip to the next byte

    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == '__main__':
    main()
'''