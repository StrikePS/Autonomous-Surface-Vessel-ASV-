import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import pigpio

class ESC_Driver(Node):
    def __init__(self):
        super().__init__('esc_driver')
        self.pi = pigpio.pi()

        if not self.pi.connected:
            self.get_logger().error("Could not connect to pigpio daemon. Did you run 'sudo systemctl start pigpiod'?")
            raise RuntimeError("pigpio not connected")

        self.esc1_gpio = 12  # GPIO12 = physical pin 32
        self.esc2_gpio = 13  # GPIO13 = physical pin 33

        self.create_subscription(Float32, 'esc1_cmd', self.esc1_callback, 10)
        self.create_subscription(Float32, 'esc2_cmd', self.esc2_callback, 10)

        self.get_logger().info("ESC Driver Node started")

    def esc1_callback(self, msg):
        pwm = float(msg.data)
        self.get_logger().info(f'Setting ESC1 (GPIO12) to {pwm} µs')
        self.pi.set_servo_pulsewidth(self.esc1_gpio, pwm) # set to left propeller

    def esc2_callback(self, msg):
        pwm = float(msg.data)
        self.get_logger().info(f'Setting ESC2 (GPIO13) to {pwm} µs')
        self.pi.set_servo_pulsewidth(self.esc2_gpio, pwm) # set to right propellers

    def stop(self):
        self.pi.set_servo_pulsewidth(self.esc1_gpio, 0)
        self.pi.set_servo_pulsewidth(self.esc2_gpio, 0)
        self.pi.stop()

def main(args=None):
    rclpy.init(args=args)
    node = ESC_Driver()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down ESC driver node...")
    finally:
        node.stop()
        node.destroy_node()
        rclpy.shutdown()