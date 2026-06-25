#!/bin/bash
# Wrapper script for custom Gazebo-ROS bridge

export GZ_PARTITION=ros_gz_example
python3 "$(dirname "$0")/gazebo_ros_bridge.py"
