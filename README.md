# AI-Enabled Mobile Robot with a 5-DOF Robotic Manipulator for Medical Emergency and Search-and-Rescue Operations
---

# Project Overview

The **AI-Enabled Mobile Robot with a 5-DOF Robotic Manipulator for Medical Emergency and Search-and-Rescue Operations**, shortly termed as the **AI Mobile Rescue Manipulator System (AI-MRMS)**, is an intelligent robotic platform designed for hazardous environment exploration, emergency medical response, remote manipulation, and disaster rescue operations.

The platform integrates:

- Embedded systems
- Artificial intelligence
- Computer vision
- Autonomous robotics
- Sensor fusion
- IoT monitoring
- Robotic manipulation

The robot supports **two modes of operation**:

## 1. Manual Long-Range Remote Control Mode

Using:

- Arduino Nano transmitter
- nRF24L01 wireless communication
- Dual joystick interface

## 2. Autonomous ROS2 Mode

Using:

- ROS2 middleware
- Nav2 navigation stack
- LiDAR-based obstacle avoidance
- Sensor fusion with EKF
- Autonomous path planning

The robot uses:

- Raspberry Pi 4 for AI inference
- Arduino Uno for low-level motor control
- 5-DOF robotic manipulator
- Tracked mobile chassis
- Hazard sensing modules

The robot can:

- Detect humans and hazards
- Monitor environmental gases
- Stream live video
- Deliver medicines
- Manipulate emergency objects
- Navigate autonomously

---

# Remarks

- Designing the complete mechanical system using SolidWorks
- Programming embedded controllers in C++ using Visual Studio Code
- Implementing long-range wireless communication using nRF24L01
- Developing an AI-based object detection pipeline using Roboflow and YOLOv8
- Deploying real-time inference on Raspberry Pi 4
- Integrating Blynk IoT visualization
- Implementing ROS2-based modular communication for autonomous operation

This project demonstrates successful integration of embedded systems, AI, computer vision, IoT, and autonomous robotics.

---

# Project Highlights

- Designed tracked mobile rescue robot using SolidWorks
- Fabricated mild steel chassis
- Designed 5-DOF robotic manipulator
- 3D printed arm using PLA
- Implemented wireless control using nRF24L01
- Developed YOLOv8 object detection system
- Trained using Roboflow + Google Colab
- Optimized using NCNN for Raspberry Pi
- Integrated ROS2 autonomous navigation
- Implemented MoveIt2 manipulation
- Added IoT monitoring using Blynk
- Integrated gas and fire sensing

---

# Features

## Autonomous Navigation

- ROS2
- Nav2
- SLAM
- Obstacle avoidance

## AI Hazard Detection

YOLOv8 detects:

- Person
- Fire
- Smoke
- Debris
- Hazard signs
- No helmet
- No safety vest

## Hazard Monitoring

Sensors:

- MQ-2
- MQ-7
- MQ-135
- Fire sensor

## Vision-Based Manipulation

- MoveIt2
- 5-DOF arm

## Live Video Streaming

- Raspberry Pi Connect

## IoT Monitoring

- Blynk dashboard

## Long-Range Remote Control

- nRF24L01

---

# System Architecture

```text
Environment
      ↓
Sensors + Pi Camera
      ↓
Raspberry Pi 4
      ↓
YOLOv8 Inference
      ↓
ROS2 Middleware
      ↓
Nav2 + EKF
      ↓
Motion Planning
      ↓
Arduino Controller
      ↓
Mobile Chassis + Robotic Arm
      ↓
Mission Execution
```

---

# Hardware Components

| Component | Purpose |
|-----------|---------|
| Raspberry Pi 4 | AI inference |
| Arduino Uno | Motor control |
| Arduino Nano | Transmitter |
| nRF24L01 | Wireless communication |
| 2D LiDAR | Obstacle detection |
| IMU | Orientation |
| Wheel Encoders | Odometry |
| Pi Camera | Vision |
| MG996R | High torque joints |
| SG90 | Wrist + gripper |
| MQ-2 | Smoke |
| MQ-7 | CO |
| MQ-135 | Air quality |
| Fire Sensor | Flame detection |

---

# AI Vision Pipeline

## Dataset Preparation

Annotated using Roboflow.

Classes:

- fire
- smoke
- person
- no_helmet
- no_vest
- debris
- obstacle
- hazard_sign

---

## Training

Framework:

Ultralytics YOLOv8

Training platform:

Google Colab GPU

Configuration:

- Epochs: 100
- Batch size: 16
- Resolution: 640x640

Validation:

mAP@0.5 ≈ 85%

---

## Deployment

Export:

NCNN optimized model

Inference:

4–6 FPS on Raspberry Pi 4

---

# ROS2 Autonomous Operation

## Why ROS2?

ROS2 enables modular communication between:

- Sensors
- Localization
- Navigation
- Manipulation
- Vision

---

# ROS2 Interface Workflow

```text
LiDAR
   +
IMU
   +
Wheel Encoder
      ↓
robot_localization
(EKF)
      ↓
/odom
      ↓
SLAM / Nav2
      ↓
/cmd_vel
      ↓
Arduino Motor Controller
```

---

# Step-by-Step ROS2 Integration

## Step 1 — Install ROS2

Recommended:

Ubuntu 22.04 + ROS2 Humble

Install:

```bash
sudo apt install ros-humble-desktop
```

---

## Step 2 — Create Workspace

```bash
mkdir -p ~/robot_ws/src
cd ~/robot_ws
colcon build
```

---

## Step 3 — Sensor Drivers

Install:

### LiDAR

```bash
sudo apt install ros-humble-rplidar-ros
```

### IMU

Publish:

```text
/imu/data
```

### Encoders

Publish:

```text
/wheel/odom
```

---

## Step 4 — Sensor Fusion

Use:

robot_localization package

```bash
sudo apt install ros-humble-robot-localization
```

Outputs:

```text
/odometry/filtered
```

---

## Step 5 — Navigation

Install Nav2:

```bash
sudo apt install ros-humble-navigation2
```

Launch:

```bash
ros2 launch nav2_bringup navigation_launch.py
```

---

## Step 6 — Arduino Communication

Use:

rosserial or micro-ROS

Topics:

Subscribe:

```text
/cmd_vel
```

Arduino converts:

```text
linear velocity
angular velocity
```

to:

- Left motor PWM
- Right motor PWM

---

## Step 7 — Manipulator

MoveIt2 receives:

```text
target_pose
```

Outputs:

```text
joint trajectories
```

---

# How It Works

## Manual Mode

Joystick → nRF24L01 → Arduino → Motors + Arm

## Autonomous Mode

Sensors → ROS2 → EKF → Nav2 → Arduino → Chassis

## Vision Mode

Pi Camera → YOLOv8 → Detection → MoveIt2 → Manipulator

## Monitoring

Sensors → Raspberry Pi → Blynk

---

# Applications

- Search and Rescue
- Disaster Response
- Medical Supply Delivery
- Hazardous Inspection
- Defense Robotics
- Industrial Safety

---

# Future Enhancements

- Thermal camera
- Victim detection
- GPS navigation
- Drone collaboration
- Voice commands
- Reinforcement learning

---

# Conclusion

The **AI Mobile Rescue Manipulator System (AI-MRMS)** successfully demonstrates the integration of embedded systems, artificial intelligence, ROS2 autonomous navigation, YOLOv8 vision, sensor fusion, IoT monitoring, and robotic manipulation into a functional emergency response platform.

By integrating Raspberry Pi 4, Arduino controllers, nRF24L01 wireless communication, LiDAR, IMU, YOLOv8, MoveIt2, Nav2, and Blynk IoT, the robot performs hazard detection, environmental monitoring, autonomous navigation, and precise manipulation with minimal human intervention.

This project establishes a strong foundation for next-generation autonomous medical emergency and search-and-rescue robotics.

---
