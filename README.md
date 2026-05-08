# AI-Enabled Mobile Robot with Robotic Manipulator for Medical Emergencies and Search & Rescue Operations (AIMR)

## Intelligent Mobile Manipulation Platform using ROS 2, YOLOv8, Sensor Fusion, IoT Monitoring, Wireless Teleoperation, and Embedded AI

---

# Project Overview

The **AI-Enabled Mobile Robot with Robotic Manipulator (AIMR)** is an intelligent robotic platform developed for **medical emergency response, disaster management, industrial safety inspection, and search-and-rescue (SAR) operations in hazardous environments**.

Natural disasters such as earthquakes, floods, landslides, industrial accidents, and structural collapses often create environments where human intervention becomes dangerous, time-consuming, and inefficient. This project addresses these challenges by developing a cost-effective, edge-AI-powered robotic system capable of autonomous navigation, hazard detection, environmental monitoring, and physical assistance.

The system integrates:

- Autonomous Mobile Robotics
- Robotic Manipulation
- Embedded Artificial Intelligence
- Computer Vision
- Sensor Fusion
- IoT Monitoring
- Wireless Communication
- Edge Computing

The robot combines:

- Raspberry Pi 5
- Arduino Uno
- ROS 2
- YOLOv8
- Wheel Encoders
- IMU
- nRF24L01
- MQ Gas Sensors
- Blynk IoT Platform
- Custom 5-DoF Robotic Manipulator

to perform intelligent monitoring, navigation, hazard detection, and manipulation tasks in complex environments.

This project directly addresses **Smart India Hackathon (SIH-1533)** problem statement.

---

# Abstract

This project presents the design and development of an AI-enabled mobile robot integrated with a 5-DoF robotic manipulator for medical emergency response and search-and-rescue operations. The system operates in two modes: **remote operation** using nRF wireless communication and **autonomous operation** using ROS 2, where wheel encoders and IMU-based sensor fusion enable localization and navigation without LiDAR. YOLOv8 performs real-time object detection with bounding-box visualization and live video streaming, while environmental conditions are monitored using gas and fire sensors, with sensor data transmitted and remotely monitored through Blynk IoT. The robotic manipulator enables medicine delivery, object handling, and lightweight debris removal, providing a scalable and cost-effective robotic solution for hazardous environments.

---

# Project Highlights

✅ Designed and developed a fully integrated AI-enabled rescue robot.

✅ Implemented **dual-mode operation**:

- Autonomous ROS 2 Mode
- Manual Wireless nRF Mode

✅ Developed localization without LiDAR using:

- Wheel Encoders
- IMU
- Extended Kalman Filter

✅ Implemented YOLOv8-based real-time object detection.

✅ Designed and fabricated a custom 5-DoF robotic arm.

✅ Integrated environmental hazard monitoring.

✅ Implemented live remote monitoring using Blynk.

✅ Developed edge-AI deployment on Raspberry Pi.

---

# Objectives

The main objectives of this project are:

- To design and develop an intelligent mobile robot for hazardous environments.
- To enable autonomous navigation using encoder and IMU-based sensor fusion.
- To implement real-time hazard and victim detection.
- To monitor environmental conditions.
- To enable wireless teleoperation.
- To develop a robotic manipulator for medicine delivery and object handling.
- To provide remote monitoring and control.

---

# Features

# 1. Dual Mode Operation

## Autonomous Mode

Powered by ROS 2.

Capabilities:

- Autonomous navigation
- Localization
- Waypoint following
- Sensor fusion
- Mobile manipulation
- Mission execution

## Remote Operation Mode

Powered by nRF24L01.

Capabilities:

- Real-time manual control
- Chassis movement
- Arm manipulation
- Gripper control
- Emergency stop

---

# 2. AI-Based Object Detection

Real-time object detection using:

- YOLOv8 Nano
- Raspberry Pi Camera

Detected classes:

- Person
- Fire
- Smoke
- No Helmet
- No Safety Vest
- Debris
- Obstacles
- Hazard Signs

Features:

- Bounding-box visualization
- Confidence scoring
- Live video streaming
- Edge inference

Performance:

- 4–6 FPS on Raspberry Pi

---

# 3. Environmental Monitoring

Integrated sensors:

- MQ2 → Smoke / LPG
- MQ7 → Carbon Monoxide
- MQ135 → Air Quality
- Flame Sensor

Monitored parameters:

- Smoke
- CO
- Toxic gases
- Fire

Data transmission:

- Blynk IoT Dashboard

Features:

- Real-time alerts
- Remote monitoring
- Sensor visualization

---

# 4. Robotic Manipulator

Custom-designed 5-DoF robotic arm.

Applications:

- Medicine delivery
- First-aid delivery
- Object handling
- Lightweight debris removal

Actuators:

- MG996R Servo Motors
- SG90 Servo Motors

Payload:

100–150 g

---

# System Architecture

```text
                         Raspberry Pi 5
┌───────────────────────────────────────────────────────┐
│                                                       │
│ ROS 2 Nodes                                           │
│                                                       │
│ Encoder Node                                          │
│ IMU Node                                              │
│ EKF Localization                                      │
│ Navigation Controller                                 │
│ YOLO Detection Node                                   │
│ MoveIt 2 Motion Planner                               │
│ Arm Controller                                        │
│ Sensor Monitoring Node                                │
│ IoT Communication Node                                │
│                                                       │
└───────────────────────────────────────────────────────┘
            ↓                                ↓
       Mobile Base                     Robotic Arm
