# AI Enabled mobile robot with a 5 DOF robotic manipulator for medical emergency and search and rescue operations. 

---

## Project Overview

The **AI-Enabled Mobile Robot with Robotic Manipulator (AIMR)** is an intelligent mobile manipulation platform designed for:

- Medical emergency response
- Search and rescue (SAR)
- Disaster management
- Industrial safety inspection
- Hazardous environment monitoring

Natural disasters such as earthquakes, floods, landslides, industrial accidents, fires, and structural collapses often create environments where human intervention becomes dangerous and time-critical. AIMR provides a scalable and cost-effective robotic solution capable of:

- Autonomous navigation
- Real-time object detection
- Environmental hazard monitoring
- Remote teleoperation
- Mobile manipulation
- Victim assistance

This project directly addresses the **Smart India Hackathon (SIH-1533)** problem statement.

---

## Key Highlights

✅ Autonomous navigation using **ROS 2 Jazzy + Nav2**

✅ Real-world localization using:

- Unitree L1 LiDAR
- Encoder odometry
- IMU fusion
- Extended Kalman Filter

✅ Gazebo simulation environment

✅ 5-DoF robotic manipulator integrated with **MoveIt 2**

✅ Edge-AI object detection using **YOLOv8**

✅ Wireless teleoperation using **nRF24L01**

✅ Environmental monitoring with IoT dashboard

✅ Raspberry Pi based embedded deployment

---

# System Modes

## 1. Autonomous Mode

Powered by ROS 2.

Capabilities:

- SLAM
- Localization
- Path planning
- Obstacle avoidance
- Waypoint navigation
- Mobile manipulation

---

## 2. Manual Teleoperation Mode

Powered by nRF24L01 wireless communication.

Capabilities:

- Chassis control
- Arm control
- Gripper control
- Emergency stop

---

# Hardware Components

## Computing

- Raspberry Pi 5
- Arduino Uno

## Sensors

- Unitree L1 LiDAR
- IMU
- Wheel encoders
- Raspberry Pi Camera

## Environmental Sensors

- MQ2 (Smoke/LPG)
- MQ7 (Carbon monoxide)
- MQ135 (Air quality)
- Flame sensor

## Communication

- nRF24L01
- WiFi

## Actuators

### Mobile Base

- ODrive motor controller
- Differential drive motors

### Manipulator

- 5-DoF robotic arm
- MG996R servo motors
- SG90 servo motors

Payload:

- 100–150 g

---

# Software Stack

## Core Framework

- ROS 2 Jazzy

## Navigation

- Nav2
- Robot Localization
- EKF

## Manipulation

- MoveIt 2
- ros2_control
- JointTrajectoryController

## Simulation

- Gazebo
- RViz

## AI

- YOLOv8 Nano
- OpenCV

## IoT

- Blynk

---

# Features

# Navigation Stack

- Autonomous navigation
- Goal-based navigation
- SLAM
- Sensor fusion
- Differential drive control

---

# Manipulation Stack

- Motion planning
- Collision-aware trajectory planning
- Interactive RViz control
- Mobile manipulation

Applications:

- Medicine delivery
- First-aid delivery
- Object handling
- Lightweight debris removal

---

# AI Object Detection

Real-time object detection using **YOLOv8 Nano**

Detected classes:

- Person
- Fire
- Smoke
- Debris
- Obstacles
- Safety hazards

Features:

- Bounding-box visualization
- Confidence scoring
- Live video streaming
- Edge inference

Performance:

- 4–6 FPS on Raspberry Pi

---

# Environmental Monitoring

Monitored parameters:

- Smoke
- Carbon monoxide
- Toxic gases
- Fire

Features:

- Real-time monitoring
- Remote alerts
- IoT visualization

---

# System Architecture

```text
                     ROS 2 Jazzy
┌──────────────────────────────────────────────┐
│                                              │
│  Nav2                  MoveIt 2              │
│  EKF                   ros2_control          │
│  SLAM                  Arm Controller        │
│  YOLO Detection        Sensor Monitoring     │
│  IoT Communication                             │
│                                              │
└──────────────────────────────────────────────┘
              ↓                      ↓

        Mobile Base          5-DoF Arm
```

---

# TF Architecture

```text
world
 └── map
      └── odom
           └── base_link
                └── arm_base_link
                     └── link1
                          └── link2
                               └── link3
                                    └── link4
                                         └── link5
                                              └── ee_link
```

---

# Project Structure

```text
AI-Enabled-mobile-robot/
│
├── robot_bringup/
├── robot_description/
├── robot_navigation/
├── robot_localization/
├── mobile_robot_arm_description/
├── mobile_robot_arm_control/
├── mobile_robot_moveit_config/
├── mobile_robot_gazebo/
├── mobile_robot_bringup/
└── ai_detection/
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/alfredpaul7/AI-Enabled-mobile-robot-.git
cd AI-Enabled-mobile-robot
```

---

## Source ROS 2

```bash
source /opt/ros/jazzy/setup.bash
```

---

## Install Dependencies

### Navigation Dependencies

```bash
sudo apt install \
ros-jazzy-navigation2 \
ros-jazzy-nav2-bringup \
ros-jazzy-robot-localization \
ros-jazzy-gazebo-ros-pkgs
```

### MoveIt 2 Dependencies

```bash
sudo apt install \
ros-jazzy-moveit \
ros-jazzy-moveit-setup-assistant \
ros-jazzy-ros2-control \
ros-jazzy-ros2-controllers \
ros-jazzy-gazebo-ros2-control \
ros-jazzy-joint-trajectory-controller
```

---

# Build Workspace

```bash
colcon build --symlink-install
```

```bash
source install/setup.bash
```

---

# Running the Project

# 1. Gazebo Simulation

```bash
ros2 launch robot_bringup robot_gazebo_launch.py
```

Launches:

- Gazebo
- Robot State Publisher
- Nav2
- Sensor pipeline

---

# 2. MoveIt 2 Simulation

```bash
ros2 launch mobile_robot_moveit_config move_group.launch.py
```

RViz:

```bash
ros2 launch mobile_robot_moveit_config moveit_rviz.launch.py
```

---

# 3. Full Mobile Manipulation System

```bash
ros2 launch mobile_robot_bringup full_system.launch.py
```

Launches:

- Gazebo
- Nav2
- MoveIt 2
- ros2_control
- RViz

---

# 4. Real Robot Deployment

## Main Computer

```bash
ros2 launch robot_bringup robot_computer_launch.py
```

## Raspberry Pi

```bash
ros2 launch robot_bringup robot_rpi_launch.py
```

---

# Robot Control

## Joystick

Supports PS4 controller.

---

## Autonomous Navigation

Set goal pose through RViz.

---

## Manipulator Control

Interactive planning using MoveIt 2.

Capabilities:

- Joint-space planning
- Cartesian planning
- Collision-aware planning

---

# Useful Commands

## View TF Tree

```bash
ros2 run tf2_tools view_frames
```

## View Controllers

```bash
ros2 control list_controllers
```

## View Joint States

```bash
ros2 topic echo /joint_states
```

## Open RViz

```bash
rviz2
```

---

# Future Scope

- Multi-robot collaboration
- Autonomous victim detection
- Thermal imaging
- Voice interaction
- Autonomous grasping
- Visual servoing
- Digital twin integration

---

# Author

## Alfred Paul

Mechatronics Engineer | Robotics Researcher | Embedded Systems Engineer

Areas of Interest:

- Mobile Robotics
- Manipulation
- Embedded AI
- Computer Vision
- Human Robot Interaction

---

# License

This project is licensed under the MIT License.
