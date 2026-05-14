import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/strikeps/Desktop/IITKGP/Summer/asv_ros2_ws/install/esc_driver'
