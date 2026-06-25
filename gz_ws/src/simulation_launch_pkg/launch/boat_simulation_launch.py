from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction, DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import os

def generate_launch_description():

    state_estimate_pkg = get_package_share_directory('asv_localization')

    sim_bridge_pkg = get_package_share_directory('wave_sim_bridgeup')

    sim_launch_pkg = get_package_share_directory('simulation_launch_pkg')

    lat_arg = DeclareLaunchArgument('lat', default_value='22.317677')
    lon_arg = DeclareLaunchArgument('lon', default_value='87.301955')
    alt_arg = DeclareLaunchArgument('alt', default_value='0.0')
    hdg_arg = DeclareLaunchArgument('hdg', default_value='0')

    sim_vehicle = ExecuteProcess(
        cmd=[
            'bash',
            os.path.join(sim_launch_pkg, 'scripts', 'start_sitl.sh'),
            LaunchConfiguration('lat'),
            LaunchConfiguration('lon'),
            LaunchConfiguration('alt'),
            LaunchConfiguration('hdg'),
        ],
        output='screen'
    )

    gz_sim_asv_localization = Node(
            package='asv_localization',
            executable='GzSim_StateEstimate',
            name='GzSim_StateEstimate',
            output='screen'
    )

    start_gazebo_sim = ExecuteProcess(
        cmd=[
            'bash',
            os.path.join(sim_launch_pkg, 'scripts', 'start_gazebo_wave_sim.sh'),
        ],
        output='screen'
    )

    # gazebo_ros_bridge = ExecuteProcess(
    #     cmd=[
    #         'bash',
    #         os.path.join(sim_bridge_pkg, 'scripts', 'gazebo_ros_bridge.sh'),
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
        start_gazebo_sim,
        sim_vehicle,
        TimerAction(period=8.0, actions=[gz_sim_asv_localization]),
        TimerAction(period=10.0, actions=[gazebo_ros_bridge_node]),
    ])