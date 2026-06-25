from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction, DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import os

def generate_launch_description():

    pkg = get_package_share_directory('wave_sim_bridgeup')

    lat_arg = DeclareLaunchArgument('lat', default_value='22.317677')
    lon_arg = DeclareLaunchArgument('lon', default_value='87.301955')
    alt_arg = DeclareLaunchArgument('alt', default_value='0.0')
    hdg_arg = DeclareLaunchArgument('hdg', default_value='0')

    sim_vehicle = ExecuteProcess(
        cmd=[
            'bash',
            os.path.join(pkg, 'scripts', 'start_sitl.sh'),
            LaunchConfiguration('lat'),
            LaunchConfiguration('lon'),
            LaunchConfiguration('alt'),
            LaunchConfiguration('hdg'),
        ],
        output='screen'
    )

    set_coords = ExecuteProcess(
        cmd=[
            'bash',
            os.path.join(pkg, 'scripts', 'set_spherical_coords.sh'),
            LaunchConfiguration('lat'),
            LaunchConfiguration('lon'),
            LaunchConfiguration('alt'),
        ],
        output='screen'
    )

    # gazebo_ros_bridge = ExecuteProcess(
    #     cmd=[
    #         'bash',
    #         os.path.join(pkg, 'scripts', 'gazebo_ros_bridge.sh'),
    #     ],
    #     output='screen'
    # )

    gazebo_ros_bridge_node = Node(
        package='wave_sim_bridgeup',
        executable='custom_gazebo_bridge',
        name='custom_gazebo_bridge',
        output='screen'
    )

    return LaunchDescription([
        lat_arg,
        lon_arg,
        alt_arg,
        hdg_arg,
        sim_vehicle,
        TimerAction(period=5.0, actions=[set_coords]),
        TimerAction(period=10.0, actions=[gazebo_ros_bridge_node]),
    ]) 