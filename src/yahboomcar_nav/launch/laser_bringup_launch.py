from launch import LaunchDescription
from launch_ros.actions import Node
import os
from launch.actions import IncludeLaunchDescription
from launch.conditions import LaunchConfigurationEquals
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory, PackageNotFoundError
from launch.actions import DeclareLaunchArgument


def generate_launch_description():
    ROBOT_TYPE = os.getenv('ROBOT_TYPE')
    RPLIDAR_TYPE = os.getenv('RPLIDAR_TYPE')
    print("\n-------- robot_type = {}, rplidar_type = {} --------\n".format(ROBOT_TYPE, RPLIDAR_TYPE))

    robot_type_arg = DeclareLaunchArgument(
        name='robot_type', default_value=ROBOT_TYPE,
        choices=['x1', 'x3', 'r2'],
        description='The type of robot')
    rplidar_type_arg = DeclareLaunchArgument(
        name='rplidar_type', default_value=RPLIDAR_TYPE,
        choices=['a1', 's2', '4ROS'],
        description='The type of lidar')

    bringup_x1_launch = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        [os.path.join(get_package_share_directory('yahboomcar_bringup'), 'launch'),
         '/yahboomcar_bringup_X1_launch.py']),
        condition=LaunchConfigurationEquals('robot_type', 'x1'))
    bringup_x3_launch = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        [os.path.join(get_package_share_directory('yahboomcar_bringup'), 'launch'),
         '/yahboomcar_bringup_X3_launch.py']),
        condition=LaunchConfigurationEquals('robot_type', 'x3'))
    bringup_r2_launch = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        [os.path.join(get_package_share_directory('yahboomcar_bringup'), 'launch'),
         '/yahboomcar_bringup_R2_launch.py']),
        condition=LaunchConfigurationEquals('robot_type', 'r2'))

    lidar_a1_launch = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        [os.path.join(get_package_share_directory('sllidar_ros2'), 'launch'),
         '/sllidar_a1_launch.py']),
        condition=LaunchConfigurationEquals('rplidar_type', 'a1'))
    lidar_s2_launch = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        [os.path.join(get_package_share_directory('sllidar_ros2'), 'launch'),
         '/sllidar_s2_launch.py']),
        condition=LaunchConfigurationEquals('rplidar_type', 's2'))

    tf_base_link_to_laser = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0.0435', '5.258E-05', '0.11', '3.14', '0', '0', 'base_link', 'laser'])

    launch_list = [
        robot_type_arg,
        bringup_x1_launch,
        bringup_x3_launch,
        bringup_r2_launch,
        rplidar_type_arg,
        lidar_a1_launch,
        lidar_s2_launch,
        tf_base_link_to_laser,
    ]

    try:
        ydlidar_share = get_package_share_directory('ydlidar_ros2_driver')
        launch_list.append(IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [os.path.join(ydlidar_share, 'launch'), '/ydlidar_raw_launch.py']),
            condition=LaunchConfigurationEquals('rplidar_type', '4ROS')))
    except PackageNotFoundError:
        pass

    return LaunchDescription(launch_list)
