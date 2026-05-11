from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node

import os
from ament_index_python.packages import get_package_share_path

def generate_launch_description():
    description = 'robot_description'
    bringup = 'robot_bringup'

    robot_description = os.path.join(get_package_share_path(description))

    robot_brignup = os.path.join(get_package_share_path(bringup))
    robot_launch = os.path.join(robot_description, 'launch', 'robot_description.launch.py')
    ptl_config = os.path.join(robot_brignup, 'config', 'pointCloud_to_laserScan_config.yaml')
    ekf_config = os.path.join(robot_brignup, 'config', 'ekf.yaml')

    teleop_config = os.path.join(robot_brignup, 'config', 'teleop_config.yaml')
    print(teleop_config)
    robot_description_launch = IncludeLaunchDescription(launch_description_source = robot_launch)

    joy = Node(
        package='joy',
        executable='joy_node',
        name='joy_node'
    )

    teleop_joy = Node(
        package = "teleop_twist_joy",
        executable = "teleop_node",
        name = "teleop_twist_joy",
        parameters=[teleop_config,{'use_stamped': True}],
        remappings=[
        ('/cmd_vel', '/joy_cmd_vel')
    ],
        output = "screen"
    )

    nav2 = IncludeLaunchDescription(
        launch_description_source = os.path.join(robot_brignup,"launch","bringup_launch.py"),
    )

    twist_mux = Node(
        package = "twist_mux_py",
        executable = "mux",
        name = "twist_mux_py",
        output = "screen",
    )

    pointCloud_to_laserScan = Node(
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            name='pointcloud_to_laserscan',
            output='screen',
            parameters=[ptl_config],
            remappings=[
                ('cloud_in', '/unilidar/cloud'),  
                ('scan', '/scan') 
            ]
        )

    slam = IncludeLaunchDescription(
        launch_description_source = os.path.join(get_package_share_path("slam_toolbox"),"launch","online_async_launch.py"),
    )

    odrive = Node(
        package='odrive_driver',
        executable='control_odrive_and_odom_pub',
        name='odrive_odom_pub',
        output='screen',
    )

    unilidar = Node(
        package="unitree_lidar_ros2",
        executable="unitree_lidar_ros2_node",
        name = "unitree_lidar_ros2",
        output = "screen"
    )

    ekf_node =  Node(
            package="robot_localization",
            executable="ekf_node",
            name="ekf_filter_node",
            output="screen",
            parameters=[ekf_config],
        )

    return LaunchDescription([
        joy,
        robot_description_launch,
        pointCloud_to_laserScan,
        teleop_joy,
        slam,
        twist_mux,
        nav2,
        ekf_node,
        unilidar,
        odrive,
    ])
