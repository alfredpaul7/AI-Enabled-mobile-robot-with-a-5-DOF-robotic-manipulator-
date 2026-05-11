#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped, PoseStamped
from std_msgs.msg import String
from nav_msgs.msg import Odometry, Path

import tf_transformations
import tf2_ros
from builtin_interfaces.msg import Time

import sys
import time
import odrive
from odrive.enums import AXIS_STATE_IDLE, AXIS_STATE_CLOSED_LOOP_CONTROL

import math
import fibre

class OdriveMotorControl(Node):
    def __init__(self):
        super().__init__('odrive_twist_driver')

        self.find_odrive()
        
        # setup parameter
        self.tire_tread= 0.425                                         
        self.target_linear_vel= 0.0                                          
        self.target_angular_vel= 0.0                                          
        self.tire_diameter= 0.2                                          
        self.right_wheel_radius= self.tire_diameter                           
        self.left_wheel_radius= self.tire_diameter                           
        self.encoder_cpr = 90.0                                         
        self.tire_circumference = math.pi * self.tire_diameter                 
        self.m_t_to_value= 1.0 / (self.tire_circumference)              
        self.m_s_to_value= self.encoder_cpr / (self.tire_circumference) 
        self.vel_l = 0.0     
        self.vel_r = 0.0     
        self.new_pos_l = 0.0 
        self.new_pos_r = 0.0 
        self.old_pos_l = 0.0 
        self.old_pos_r = 0.0 
 
        self.x = 0.0     
        self.y = 0.0     
        self.theta = 0.0 

        
        self.poses_list = []

        self.odom_frame = "map"
        self.base_frame = "base_footprint"

        self.odom_msg = Odometry()
        self.odom_msg.header.frame_id = self.odom_frame
        self.odom_msg.child_frame_id  = self.base_frame
        self.odom_msg.pose.pose.position.x = 0.0
        self.odom_msg.pose.pose.position.y = 0.0
        self.odom_msg.pose.pose.position.z = 0.0    
        self.odom_msg.pose.pose.orientation.x = 0.0 
        self.odom_msg.pose.pose.orientation.y = 0.0 
        self.odom_msg.pose.pose.orientation.z = 0.0
        self.odom_msg.pose.pose.orientation.w = 1.0
        self.odom_msg.twist.twist.linear.x = 0.0
        self.odom_msg.twist.twist.linear.y = 0.0  
        self.odom_msg.twist.twist.linear.z = 0.0  
        self.odom_msg.twist.twist.angular.x = 0.0 
        self.odom_msg.twist.twist.angular.y = 0.0 
        self.odom_msg.twist.twist.angular.z = 0.0

        self.map_broadcaster  = tf2_ros.TransformBroadcaster(self)
        self.odom_broadcaster = tf2_ros.TransformBroadcaster(self)

        self.map_to_odom_msg = TransformStamped()
        self.map_to_odom_msg.header.frame_id = "map"
        self.map_to_odom_msg.child_frame_id  = "odom"
        self.map_to_odom_msg.transform.translation.x = 0.0
        self.map_to_odom_msg.transform.translation.y = 0.0
        self.map_to_odom_msg.transform.translation.z = 0.0
        self.map_to_odom_msg.transform.rotation.x = 0.0
        self.map_to_odom_msg.transform.rotation.y = 0.0
        self.map_to_odom_msg.transform.rotation.z = 0.0
        self.map_to_odom_msg.transform.rotation.w = 1.0

        self.odom_to_baselink_msg = TransformStamped()
        self.odom_to_baselink_msg.header.frame_id = "map"
        self.odom_to_baselink_msg.child_frame_id  = "base_footprint"
        self.odom_to_baselink_msg.transform.translation.x = 0.0
        self.odom_to_baselink_msg.transform.translation.y = 0.0
        self.odom_to_baselink_msg.transform.translation.z = 0.0
        self.odom_to_baselink_msg.transform.rotation.x = 0.0
        self.odom_to_baselink_msg.transform.rotation.y = 0.0
        self.odom_to_baselink_msg.transform.rotation.z = 0.0
        self.odom_to_baselink_msg.transform.rotation.w = 1.0

        # subscriber cmd_vel
        self.create_subscription(Twist, '/cmd_vel', self.callback_vel, 50)

        self.timer = self.create_timer(0.05, self.update) 

        # publish odom
        self.odom_publisher = self.create_publisher(Odometry, "odom", 100)

        # publish odom_path
        self.odom_path_publisher = self.create_publisher(Path, "odom_path", 100)

    def callback_vel(self, msg):
        self.get_logger().info('Callback received a velocity message.')
        self.get_logger().info('I heard: "%s"' % msg.linear.x)
        self.target_linear_vel = msg.linear.x
        self.target_angular_vel = msg.angular.z

    def find_odrive(self):
        while True:
            self.get_logger().info("Connect to Odrive...")
            self.odrv0 = odrive.find_any()
            if self.odrv0 is not None:
                self.get_logger().info("Connect to Odrive Success!!!")
                break
            else:
                self.get_logger().info("Disconnect to Odrive...")

    def odrive_setup(self):
        self.get_logger().info("start setup...")
        self.get_logger().info("%s" % self.odrv0.vbus_voltage)
        # In __init__
        self.initial_pos_r = 0.0
        self.initial_pos_l = 0.0

        # In odrive_setup or update, after connecting to Odrive:
        self.odrv0.axis0.encoder.set_linear_count(self.initial_pos_r)

        self.odrv0.axis1.encoder.set_linear_count(self.initial_pos_l)

        self.get_logger().info("self.odrv0.axis0.encoder.pos_estimate : %s" % self.odrv0.axis0.encoder.pos_estimate)
        self.get_logger().info("self.odrv0.axis1.encoder.pos_estimate : %s" % self.odrv0.axis1.encoder.pos_estimate)

        self.odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.odrv0.axis0.controller.input_vel = 0
        self.odrv0.axis1.controller.input_vel = 0
    
    def update(self):
        current_time = self.get_clock().now().to_msg()
        right_vel, left_vel = self.calc_relative_vel(self.target_linear_vel, self.target_angular_vel)
        self.calcodom(current_time)
        self.odrv0.axis0.controller.input_vel = right_vel
        self.odrv0.axis1.controller.input_vel = -left_vel
        #トルクを計算
        # 各軸のモーター電流を取得
        motor_current_0 = self.odrv0.axis0.motor.current_control.Iq_measured
        motor_current_1 = self.odrv0.axis1.motor.current_control.Iq_measured

        # トルク定数を取得
        torque_constant_0 = self.odrv0.axis0.motor.config.torque_constant
        torque_constant_1 = self.odrv0.axis1.motor.config.torque_constant

        # トルクを計算
        torque_0 = motor_current_0 * torque_constant_0
        torque_1 = motor_current_1 * torque_constant_1

        #print("軸0のトルク: {} Nm".format(torque_0))
        #print("軸1のトルク: {} Nm".format(torque_1))
        
    def calc_relative_vel(self, target_linear_vel, target_angular_vel):
        # Convert to each circumferential velocity
        circumferential_right_vel = target_linear_vel + (self.tire_tread / 2.0) * target_angular_vel #[m/s]
        circumferential_left_vel  = target_linear_vel - (self.tire_tread / 2.0) * target_angular_vel #[m/s]

        # Convert to each rotational velocity
        right_vel = circumferential_right_vel / self.tire_circumference #[turn/s]
        left_vel  = circumferential_left_vel / self.tire_circumference  #[turn/s]

        return right_vel, left_vel
    
    def calcodom(self, current_time):

        self.new_pos_r = self.encoder_cpr * self.odrv0.axis0.encoder.pos_estimate #[count]
        self.new_pos_l = self.encoder_cpr * self.odrv0.axis1.encoder.pos_estimate #[count]
        

        delta_pos_r = self.new_pos_r - self.old_pos_r #[count]
        delta_pos_l = self.new_pos_l - self.old_pos_l #[count]
        
        self.old_pos_r = self.new_pos_r #[count]
        self.old_pos_l = self.new_pos_l #[count]
        
        # Check for overflow. Assume we can't move more than half a circumference in a single timestep. 
        half_cpr = self.encoder_cpr / 2.0
        if delta_pos_r >  half_cpr: 
            delta_pos_r = delta_pos_r - self.encoder_cpr
        elif delta_pos_r < -half_cpr: 
            delta_pos_r = delta_pos_r + self.encoder_cpr
        if delta_pos_l >  half_cpr: 
            delta_pos_l = delta_pos_l - self.encoder_cpr
        elif delta_pos_l < -half_cpr: 
            delta_pos_l = delta_pos_l + self.encoder_cpr
        
        # convert [turns] into [m]
        delta_pos_r_m = delta_pos_r / self.m_s_to_value
        delta_pos_l_m = delta_pos_l / self.m_s_to_value * (-1)
        
        # Distance travelled
        d = (delta_pos_r_m + delta_pos_l_m) / 2.0  # delta_ps
        th = (delta_pos_r_m - delta_pos_l_m) / self.tire_tread # works for small angles
    
        xd = math.cos(th)*d
        yd = -math.sin(th)*d

        # Pose: updated from previous pose + position delta
        self.x += math.cos(self.theta)*xd - math.sin(self.theta)*yd
        self.y += math.sin(self.theta)*xd + math.cos(self.theta)*yd
        self.theta = (self.theta + th) % (2*math.pi)

        self.vel_r = self.encoder_cpr * self.odrv0.axis0.encoder.vel_estimate
        self.vel_l = self.encoder_cpr * self.odrv0.axis1.encoder.vel_estimate * (-1)
        v = self.tire_circumference * (self.vel_r + self.vel_l) / (2.0*self.encoder_cpr)
        w = self.tire_circumference * (self.vel_r - self.vel_l) / (self.tire_tread * self.encoder_cpr) # angle: vel_r*tyre_radius - vel_l*tyre_radius

        self.odom_msg.header.stamp = current_time
        self.odom_msg.pose.pose.position.x = self.x
        self.odom_msg.pose.pose.position.y = self.y
        q = tf_transformations.quaternion_from_euler(0.0, 0.0, self.theta)
        self.odom_msg.pose.pose.orientation.z = q[2] # math.sin(self.theta)/2
        self.odom_msg.pose.pose.orientation.w = q[3] # math.cos(self.theta)/2
        self.odom_msg.twist.twist.linear.x  = v
        self.odom_msg.twist.twist.angular.z = w
        self.odom_publisher.publish(self.odom_msg)

        self.map_to_odom_msg.header.stamp = current_time

        self.map_to_odom_msg.transform.translation.x = 0.0
        self.map_to_odom_msg.transform.translation.y = 0.0
        self.map_to_odom_msg.transform.translation.z = 0.0

        odom_quat = tf_transformations.quaternion_from_euler(0.0, 0.0, 0.0)
        self.map_to_odom_msg.transform.rotation.x = odom_quat[0]
        self.map_to_odom_msg.transform.rotation.y = odom_quat[1]
        self.map_to_odom_msg.transform.rotation.z = odom_quat[2]
        self.map_to_odom_msg.transform.rotation.w = odom_quat[3]

        self.map_broadcaster.sendTransform(self.map_to_odom_msg)

        
        self.odom_to_baselink_msg.transform.translation.x = self.x
        self.odom_to_baselink_msg.transform.translation.y = self.y
        self.odom_to_baselink_msg.transform.rotation.z = q[2]
        self.odom_to_baselink_msg.transform.rotation.w = q[3]
        self.odom_broadcaster.sendTransform(self.odom_to_baselink_msg)
        
        #########################
        # Publish Odometry Path #
        #########################
        temp_pose = PoseStamped()
        temp_pose.header.stamp = current_time
        temp_pose.header.frame_id = "map"
        temp_pose.pose.position.x = self.x
        temp_pose.pose.position.y = self.y
        temp_pose.pose.orientation.z = q[2]
        temp_pose.pose.orientation.w = q[3]

        self.poses_list.append(temp_pose)

        # creat path data
        self.path = Path()
        self.path.header.stamp = current_time
        self.path.header.frame_id = "map"
        self.path.poses = self.poses_list

        self.odom_path_publisher.publish(self.path)
    
    def fini(self):
        self.get_logger().info("shutdown...")
        self.odrv0.axis0.controller.input_vel = 0
        self.odrv0.axis1.controller.input_vel = 0
        self.odrv0.axis0.requested_state = AXIS_STATE_IDLE
        self.odrv0.axis1.requested_state = AXIS_STATE_IDLE

def main(args=None):
    rclpy.init(args=args)
    Odrive_motor_control = OdriveMotorControl()
    Odrive_motor_control.odrive_setup()
    try:
        rclpy.spin(Odrive_motor_control)
    finally:
        Odrive_motor_control.fini()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
