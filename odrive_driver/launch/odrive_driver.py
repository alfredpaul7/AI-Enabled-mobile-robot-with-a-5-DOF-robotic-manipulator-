#!/usr/bin/env python3
import os
import launch
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    package_dir = get_package_share_directory('odrive_driver')

    return LaunchDescription([

        Node(
            package='odrive_driver',
            executable='control_odrive_and_odom_pub',
            name='odrive_odom_pub',
            output='screen'
        ),
        Node(
            package='odrive_driver',
            executable='mock_pub',
            name = "mock_pub",
            output = "screen",
        ),
    ])

if __name__ == '__main__':
    generate_launch_description()
