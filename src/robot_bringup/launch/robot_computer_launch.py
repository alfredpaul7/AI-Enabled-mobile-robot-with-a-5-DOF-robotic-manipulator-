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
    gazebo_description = os.path.join(get_package_share_path('ros_gz_sim'))
    # rviz_config_path = os.path.join(get_package_share_path(description),
    #                                 'rviz', 'urdf_config.rviz')
    
    robot_brignup = os.path.join(get_package_share_path(bringup))
    robot_launch = os.path.join(robot_description, 'launch', 'robot_description.launch.py')
    gz_launch = os.path.join(gazebo_description, 'launch', 'gz_sim.launch.py')
    world = os.path.join(robot_brignup,'config', 'test_world.sdf')
    ptl_config = os.path.join(robot_brignup, 'config', 'pointCloud_to_laserScan_config.yaml')
    ekf_config = os.path.join(robot_brignup, 'config', 'ekf.yaml')

    rviz2_config_path = os.path.join(robot_brignup,"config","rviz_config.rviz")
    teleop_config = os.path.join(robot_brignup, 'config', 'teleop_config.yaml')
    print(teleop_config)
    robot_controllers = os.path.join(get_package_share_path(description),'config','controller_config.yaml',)
    robot_description_launch = IncludeLaunchDescription(launch_description_source = robot_launch)

    start_gazebo = IncludeLaunchDescription(launch_description_source = gz_launch,launch_arguments= {'gz_args': f"{world} -r",}.items())
    parameter_bridge_config = os.path.join(robot_brignup, 'config', 'gz_ros_topic_bridge.yaml')
    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
            arguments=[
                "-topic", "/robot_description",
        ],
        parameters=[{"/use_sim_time":True}]
    )
    
    ros_gz_bridge = Node(
        package=  'ros_gz_bridge',
        executable="parameter_bridge",
        parameters=[
            {"config_file":parameter_bridge_config}]
    )
   
    rviz2_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', rviz2_config_path]
    )

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
                ('cloud_in', '/lidar_points'),  
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
            parameters=[ekf_config,{"use_sim_time":True}],
        )

    return LaunchDescription([
        # joy,
        # robot_description_launch,
        # start_gazebo,
        # ros_gz_bridge,
        # spawn_robot,
        # pointCloud_to_laserScan,
        # teleop_joy,
        # slam,
        # twist_mux,
        # nav2,
        # ekf_node,
        # unilidar,
        rviz2_node,
        # odrive,
    ])