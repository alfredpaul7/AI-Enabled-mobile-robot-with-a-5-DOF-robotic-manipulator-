from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from ament_index_python.packages import get_package_share_directory

import os

def generate_launch_description():

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('your_nav2_package'),
                'launch',
                'navigation.launch.py'
            )
        )
    )

    moveit = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('mobile_robot_moveit_config'),
                'launch',
                'move_group.launch.py'
            )
        )
    )

    return LaunchDescription([
        nav2,
        moveit
    ])