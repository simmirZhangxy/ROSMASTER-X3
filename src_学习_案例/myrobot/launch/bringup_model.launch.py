import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    pkg_share = FindPackageShare('myrobot').find('myrobot')
    urdf_path = os.path.join(pkg_share, 'urdf/demo01_base.urdf')

    start_gazebo_server = ExecuteProcess(
        cmd=['gzserver', '-s', 'libgazebo_ros_init.so',
             '-s', 'libgazebo_ros_factory.so'],
        output='screen')

    start_gazebo_client = ExecuteProcess(
        cmd=['gzclient'],
        output='screen')

    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'myrobot', '-file', urdf_path],
        output='screen')

    return LaunchDescription([
        start_gazebo_server,
        TimerAction(period=5.0, actions=[spawn_entity]),
        TimerAction(period=8.0, actions=[start_gazebo_client]),
    ])